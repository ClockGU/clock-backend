from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import DurationField, F, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from more_itertools import pairwise
from pdfkit import from_string as pdf_from_string
from pytz import datetime, timezone
from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.filters import ShiftFilterSet
from api.models import ClockedInShift, Contract, Report, Shift, User
from api.serializers import (
    ClockedInShiftSerializer,
    ContractSerializer,
    ReportSerializer,
    ShiftSerializer,
    UserSerializer,
)
from api.utilities import relativedelta_to_string, timedelta_to_string
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
        return queryset.filter(user__id=self.request.user.id).order_by("-last_used")

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

    def lock_shifts(self, request, month=None, year=None, *args, **kwargs):

        instance = self.get_object()
        Shift.objects.filter(
            contract=instance, started__month=month, started__year=year
        ).update(locked=True)

        return Response()


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    filterset_class = ShiftFilterSet
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


class ClockedInShiftViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ClockedInShift.objects.all()
    serializer_class = ClockedInShiftSerializer
    name = "clockedinshift"

    def list(self, request, *args, **kwargs):
        """
        Override the list method to utilize the url matching.
        Since there will only be one or no ClockedInShift object we want a
        method to retrieve it without a pk.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = get_object_or_404(self.get_queryset(), user__id=self.request.user.id)
        serializer = self.get_serializer(instance)
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

    @action(
        detail=False,
        url_name="get_current",
        url_path="get_current/(?P<contract_id>[^/.]+)",
    )
    def get_current(self, request, contract_id, *args, **kwargs):
        """
        Custom endpoint which retrieves the Report of the current month.
        :param contract_id:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        now = datetime.datetime.now()
        queryset = self.get_queryset()
        instance = get_object_or_404(
            queryset,
            month_year__month=now.month,
            month_year__year=now.year,
            contract__id=contract_id,
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
        # We have to use DateTime objects since Date objects ignore timezones.
        # This causes problems with DateTimes which change the day on Localtime -> UTC conversion
        # Only works for servertime
        dates = [_datetime.date() for _datetime in shifts.datetimes("started", "day")]
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

            started = shifts_of_date.first().started.astimezone(
                timezone(settings.TIME_ZONE)
            )
            stopped = shifts_of_date.last().stopped.astimezone(
                timezone(settings.TIME_ZONE)
            )

            content[date.strftime("%d.%m.%Y")] = {
                "started": started.time().strftime("%H:%M"),
                "stopped": stopped.time().strftime("%H:%M"),
                "type": vacation_or_sick_type,
                "work_time": timedelta_to_string(stopped - started),
                "net_work_time": timedelta_to_string(worked_time),
                "break_time": timedelta_to_string(
                    stopped - started - worked_time - sick_or_vacation_time
                ),
                "sick_or_vac_time": timedelta_to_string(sick_or_vacation_time),
            }
        return content

    def calculate_carryover_worktime(self, report_object, next_month=True):
        # Calculate carryover from last month
        report_to_carry = report_object
        if not next_month:
            try:
                report_to_carry = Report.objects.get(
                    contract=report_object.contract,
                    month_year=report_object.month_year - relativedelta(months=1),
                )
            except Report.DoesNotExist:
                # We are looking at the first report of a contract. Return the
                # initial_carryover_minutes as relativedelta.
                return relativedelta(
                    minutes=report_object.contract.initial_carryover_minutes
                )

        td = report_to_carry.worktime - datetime.timedelta(
            minutes=report_object.contract.minutes
        )
        return relativedelta(seconds=td.total_seconds())

    def check_for_overlapping_shifts(self, shift_queryset):
        """
        Check the given Queryset for possible overlapping shifts and raise a Validation error
        with pairs of overlapping shifts.
        :param shift_queryset:
        :return:
        """
        e = []

        for early_shift, late_shift in pairwise(shift_queryset.order_by("started")):

            if late_shift.started < early_shift.stopped:
                e.append(
                    [
                        ShiftSerializer(early_shift).data,
                        ShiftSerializer(late_shift).data,
                    ]
                )

        if e:
            raise serializers.ValidationError(
                {
                    "message": _(
                        "An export of the worktime-sheet is not possible due to overlapping shifts."
                    ),
                    "shifts": e,
                }
            )

    def aggregate_general_content(self, report_object, shifts):
        """
        Aggregate Data for Tablefooter and User info of the Stundenzettel.
        :param report_object:
        :param shifts:
        :return:
        """
        month_names = {
            1: "Januar",
            2: "Februar",
            3: "März",
            4: "April",
            5: "Mai",
            6: "Juni",
            7: "Juli",
            8: "August",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Dezember",
        }
        content = {}
        user = report_object.user

        # User data
        content["user_name"] = "{lastname}, {firstname}".format(
            lastname=user.last_name, firstname=user.first_name
        )
        content["personal_number"] = user.personal_number
        content["contract_name"] = report_object.contract.name
        content["month"] = report_object.month_year.month
        content["year"] = report_object.month_year.year
        content["long_month_name"] = month_names[report_object.month_year.month]

        # Working time account (AZK)
        content["debit_work_time"] = relativedelta_to_string(
            relativedelta(minutes=report_object.contract.minutes)
        )
        time_worked = relativedelta(seconds=report_object.worktime.total_seconds())
        content["total_worked_time"] = relativedelta_to_string(time_worked)

        carryover = {
            "previous_month": self.calculate_carryover_worktime(
                report_object, next_month=False
            ),
            "next_month": self.calculate_carryover_worktime(report_object),
        }
        content["last_month_carry_over"] = relativedelta_to_string(
            carryover["previous_month"]
        )
        content["next_month_carry_over"] = relativedelta_to_string(
            carryover["next_month"]
        )
        content["net_worktime"] = relativedelta_to_string(
            time_worked - carryover["previous_month"]
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

        # Check for overlapping shifts
        self.check_for_overlapping_shifts(shift_queryset)
        self.check_for_not_locked_shifts(report_object)

        # Get all dates the user has worked on
        content["shift_content"] = self.aggregate_shift_content(shift_queryset)
        content["general"] = self.aggregate_general_content(
            report_object, shift_queryset
        )

        return content

    def check_for_not_locked_shifts(self, report_object):
        """
        Validate wether the creation of a Worktimesheet from a Report is allowed.
        The criteria for this check to pass is, that there is no shift in the previous month which doesn't have
        locked=False.
        :param report_object:
        :return:
        """
        previous_report_month_year = report_object.month_year - relativedelta(months=1)

        # Check if there is a not-planned shift which hasn't been locked.
        if Shift.objects.filter(
            contract=report_object.contract,
            started__year=previous_report_month_year.year,
            started__month=previous_report_month_year.month,
            user=report_object.user,
            was_reviewed=True,
            locked=False,
        ).exists():
            raise serializers.ValidationError(
                _(
                    "All Shifts of the previous month need to be locked before this Worktimesheet can be created."
                )
            )


@swagger_auto_schema(content_type="text/json")
class GDPRExportView(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to download all saved Data associated with the requesting User.

        The Response contains a JSON file as attachment!
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user
        json_object = self.construct_json_object(user)
        rendered = self.render_json_object(json_object)
        response = HttpResponse(rendered, content_type="text/json")
        date = datetime.datetime.now().strftime("%d_%m_%Y")
        response[
            "Content-Disposition"
        ] = "attachment; filename={0}_{1}_gdpr-export_{2}.json".format(
            user.first_name, user.last_name, date
        )
        return response

    def construct_json_object(self, user):
        user_data = UserSerializer(user).data
        contract_data = ContractSerializer(
            Contract.objects.filter(user=user), many=True
        ).data
        shift_data = ShiftSerializer(Shift.objects.filter(user=user), many=True).data
        report_data = ReportSerializer(Report.objects.filter(user=user), many=True).data

        return {
            "user_data": user_data,
            "contracts_data": contract_data,
            "shifts_data": shift_data,
            "reports_data": report_data,
        }

    def render_json_object(self, json_object):
        return JSONRenderer().render(
            json_object, accepted_media_type="application/json; indent=4"
        )
