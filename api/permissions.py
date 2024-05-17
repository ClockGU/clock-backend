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
from rest_framework.permissions import IsAuthenticated


class AccessOwnDataPermission(IsAuthenticated):
    """
    Permission class which only permits access of Objects which are owned by the
    User issueing the request.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id


class IsSupervisorPermission(IsAuthenticated):

    def has_permission(self, request, view):
        return request.user.is_supervisor