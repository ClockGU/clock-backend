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
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from api.models import User


class GoetheUniProvider(OAuth2Provider):
    id = "goetheuni"
    name = "GoetheUni"
    account_class = ProviderAccount

    def sociallogin_from_response(self, request, response):
        try:
            user = User.objects.get(username=response["id"])
        except User.DoesNotExist:
            pass
        else:
            if user.email != response["email"]:
                user.email = response["email"]
                user.save()
        finally:
            return super(GoetheUniProvider, self).sociallogin_from_response(
                request, response
            )

    def extract_uid(self, data):
        """Grab the uid from attributes and force it to lowercase."""
        return str(data["attributes"]["uid"]).lower()

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )


provider_classes = [GoetheUniProvider]
