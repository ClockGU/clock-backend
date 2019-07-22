from django.http import HttpResponse
from django.template.loader import get_template
from pytz import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from pdfkit import from_string as pdf_from_string

from api.models import Contract, Report, Shift
from api.serializers import ContractSerializer, ReportSerializer, ShiftSerializer
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
    template = get_template("api/stundenzettel.html")
    html = template.render({"blargh": "Something to render."})
    pdf = pdf_from_string(html, False)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename='test.pdf'"
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
