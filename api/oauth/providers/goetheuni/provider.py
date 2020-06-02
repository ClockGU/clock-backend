from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class GoetheUniProvider(OAuth2Provider):
    id = "goetheuni"
    name = "GoetheUni"
    account_class = ProviderAccount

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            username=data.get("username"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )


provider_classes = [GoetheUniProvider]
