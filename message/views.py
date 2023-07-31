"""
Clock - Master your timesheets
Copyright (C) 2023  Johann Wolfgang Goethe-Universität Frankfurt am Main

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU Affero General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://github.com/ClockGU/clock-backend/blob/master/licenses/>.
"""
from datetime import date

from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Message
from .serializers import MessageSerializer


class MessageEndpoint(ReadOnlyModelViewSet):
    """
    Provide database table of currently valid messages.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    name = "message"

    def get_queryset(self):
        qs = super(MessageEndpoint, self).get_queryset()
        return qs.filter(
            Q(valid_from__lte=date.today(), valid_to__gte=date.today())
            | Q(valid_from__lte=date.today(), valid_to__isnull=True)
        )
