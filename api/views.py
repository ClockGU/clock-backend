from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum, F, DurationField
from django.db.models.functions import Coalesce
from pytz import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from pdfkit import from_string as pdf_from_string
from dateutil.relativedelta import relativedelta
from math import modf

from api.models import Contract, Report, Shift
from api.serializers import ContractSerializer, ReportSerializer, ShiftSerializer
from api.utilities import relativedelta_to_string
from project_celery.tasks import async_5_user_creation

# Proof of Concept that celery works


def index(request):
    """
    This function based view provides a proof of concept (for the local env) that
    the celery workers (in extern Docker Containers) work.
    :param request:
    :return:
    """
    async_5_user_creation.delay()
    return HttpResponse("A Dummy site.")


# Test view. To be deleted later.
def test_template_engine(request):
    options = {
        "page-size": "A4",
        "margin-top": "5px",
        "margin-right": "5px",
        "margin-bottom": "5px",
        "margin-left": "15px",
        "encoding": "UTF-8",
        "no-outline": None,
    }
    template = get_template("api/stundenzettel.html")
    html = template.render()
    pdf = pdf_from_string(html, False, options=options)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=test.pdf"
    return response


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    name = "contracts"

    def get_queryset(self):
        """
        Customized method to only retrieve Objects owned by the User issueing the request.
        :return:
        """
        queryset = super(ContractViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user.id)

    @action(detail=True, url_name="shifts", url_path="shifts", methods=["get"])
    def get_shifts_list(self, request, *args, **kwargs):
        """
        Custom endpoint which retrieves all shifts corresponding to the issued Contract object.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = ShiftSerializer(instance.shifts, many=True)
        return Response(serializer.data)


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    name = "shifts"

    def get_queryset(self):
        """
        Customized method to only retrieve Objects owned by the User issueing the request.
        :return:
        """
        queryset = super(ShiftViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user.id)

    def list_month_year(self, request, month=None, year=None, *args, **kwargs):
        """
        Custom endpoint which retrieves all shifts corresponding to the provided <month> and <year> url params.
        :param request:
        :param month:
        :param year:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.get_queryset().filter(started__month=month, started__year=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    name = "reports"

    def get_queryset(self):
        """
        Customized method to only retrieve Objects owned by the User issueing the request.
        :return:
        """
        queryset = super(ReportViewSet, self).get_queryset()
        return queryset.filter(user__id=self.request.user.id)

    @action(detail=False, url_name="get_current", url_path="get_current")
    def get_current(self, request, *args, **kwargs):
        """
        Custom endpoint which retrieves the Report of the current month.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        now = datetime.datetime.now()
        queryset = self.get_queryset()
        instance = get_object_or_404(
            queryset, month_year__month=now.month, month_year__year=now.year
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, url_name="export", url_path="export")
    def export(self, request, *args, **kwargs):
        """
        Endpoint to export a given Report as Stundenzettel.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        options = {
            "page-size": "Letter",
            "margin-top": "30px",
            "margin-right": "5px",
            "margin-bottom": "5px",
            "margin-left": "15px",
            "encoding": "UTF-8",
            "no-outline": None,
        }
        report = self.get_object()
        aggregated_content = self.aggregate_export_content(report_object=report)
        pdf = self.compile_pdf(
            template_name="api/stundenzettel.html",
            content_dict=aggregated_content,
            pdf_options=options,
        )
        response = HttpResponse(pdf, content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = "attachment; filename=Stundenzettel_{month:02d}_{year}.pdf".format(
            month=aggregated_content["general"]["month"],
            year=aggregated_content["general"]["year"],
        )
        self.set_shifts_as_exported(report)
        return response

    def compile_pdf(self, template_name, content_dict, pdf_options):
        """
        Compile a PDF given a Django HTML-Tmeplate name as string, a content dictionary and possible options.
        :param template_name:
        :param content_dict:
        :param pdf_options:
        :return:
        """
        template = get_template(template_name)
        html = template.render(content_dict)
        pdf = pdf_from_string(html, False, options=pdf_options)
        return pdf

    def get_shifts_to_export(self, report_object):
        """
        Methode to provide all Shift Objects for a given Report to be exported
        in a Stundenzettel ordered by started field.
        :param report_object:
        :return:
        """
        shifts = Shift.objects.filter(
            contract=report_object.contract,
            started__year=report_object.month_year.year,
            started__month=report_object.month_year.month,
            user=report_object.user,
            was_reviewed=True,
        ).order_by("started")

        return shifts

    def set_shifts_as_exported(self, report_object):

        shifts = self.get_shifts_to_export(report_object)
        shifts.update(was_exported=True)

    def aggregate_shift_content(self, shifts):
        """
        Method to aggregate a content with all dates at which a shift was worked.
        By creating this dictionary we merge all Shifts on a date to One Object with the following rule:

        Take the started value of the first Shift of the date as actual started value.
        Use the stopped value of the last Shift of the date as actual stopped value.
        Calculate the total work time as Sum of stopped - started values of each Shift at a date.
        Calculate the break time as the actual stopped - actual started - worktime.

        E.g.:

        Assume we have at a given date (1.1.1999) 3 Shifts.
        1. 10:00-11:30
        2. 13:00-15:30
        3. 16:00-18:30

        From this follow the values:
        actual started : 10:00
        actual stopped : 18:30
        work time : 6 hours 30 minutes
        break time : 2 hours

        :param report_object:
        :return:
        """
        content = {}

        dates = shifts.dates("started", "day")

        for date in dates:
            shifts_of_date = shifts.filter(started__date=date)
            worked_shifts = shifts_of_date.filter(type="st")
            vacation_or_sick_shifts = shifts_of_date.exclude(type="st")
            # calculate time worked
            worked_time = worked_shifts.aggregate(
                work_time=Coalesce(
                    Sum(F("stopped") - F("started"), output_field=DurationField()),
                    datetime.timedelta(0),
                )
            )["work_time"]
            # calculate time not present
            sick_or_vacation_time = vacation_or_sick_shifts.aggregate(
                sick_or_vac_time=Coalesce(
                    Sum(F("stopped") - F("started"), output_field=DurationField()),
                    datetime.timedelta(0),
                )
            )["sick_or_vac_time"]

            vacation_or_sick_type = ""
            if vacation_or_sick_shifts.exists():
                vacation_or_sick_type = (
                    vacation_or_sick_shifts.first().get_type_display()
                )

            started = shifts_of_date.first().started
            stopped = shifts_of_date.last().stopped

            content[date.strftime("%d.%m.%Y")] = {
                "started": started.time().isoformat(),
                "stopped": stopped.time().isoformat(),
                "type": vacation_or_sick_type,
                "work_time": str(stopped - started),
                "net_work_time": str(worked_time),
                "break_time": str(stopped - started - worked_time),
                "sick_or_vac_time": str(sick_or_vacation_time),
            }
        return content

    def calculate_carry_over_hours(self, report_object, next_month=True):

        # Calculate carry over from last month
        report_to_carry = report_object
        if not next_month:
            try:
                report_to_carry = Report.objects.get(
                    contract=report_object.contract,
                    month_year=report_object.month_year - relativedelta(months=1),
                )
            except Report.DoesNotExist:
                # If no Report Object exists we are in the case of the first Report of a Contract
                # Hence return 0:00:00 hours
                return datetime.timedelta(0)
        time_delta = report_to_carry.hours - datetime.timedelta(
            hours=report_object.contract.hours
        )
        relative_time = relativedelta(seconds=time_delta.total_seconds())

        # relativedelta will in this case maximally convert the seconds into days we use this
        # to format a string
        return relativedelta_to_string(relative_time)

    def aggregate_general_content(self, report_object, shifts):
        """
        Aggregate Data for Tablefooter and User info of the Stundenzettel.
        :param report_object:
        :param shifts:
        :return:
        """
        content = {}
        contract_hours_decimal, contract_hours = modf(report_object.contract.hours)
        user = report_object.user
        # Data for Header
        content["user_name"] = "{lastname}, {firstname}".format(
            lastname=user.last_name, firstname=user.first_name
        )
        content["personal_number"] = user.personal_number
        content["contract_name"] = report_object.contract.name
        content["month"] = report_object.month_year.month
        content["year"] = report_object.month_year.year

        # Data for Footer
        content["debit_work_time"] = "{hours:02g}:{minutes:02g}".format(
            hours=contract_hours, minutes=60 * round(contract_hours_decimal, 2)
        )
        content["total_worked_time"] = relativedelta_to_string(
            relativedelta(seconds=report_object.hours.total_seconds())
        )

        content["last_month_carry_over"] = self.calculate_carry_over_hours(
            report_object, next_month=False
        )
        content["next_month_carry_over"] = self.calculate_carry_over_hours(
            report_object
        )

        return content

    def aggregate_export_content(self, report_object):
        """
        Method which aggregates a dictionary to fill in the Stundenzettel HTML-Template.
        :param report_object:
        :return:
        """
        content = {}
        shift_queryset = self.get_shifts_to_export(report_object)
        # Check for overlapping Shifts Coming soon
        shifts_content = self.aggregate_shift_content(shift_queryset)
        general_content = self.aggregate_general_content(report_object, shift_queryset)
        # Get all Days, as Dates, on which the user worked
        content["shift_content"] = shifts_content
        content["general"] = general_content

        return content
