from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class GoetheUniAccount(ProviderAccount):
    def to_str(self):
        dflt = super(GoetheUniAccount, self).to_str()
        return next(
            value
            for value in (
                self.account.extra_data.get("name", None),
                self.account.extra_data.get("login", None),
                dflt,
            )
            if value is not None
        )


class GoetheUniProvider(OAuth2Provider):
    id = "goetheuni"
    name = "GoetheUni"
    account_class = GoetheUniAccount

    def get_default_scope(self):
        scope = []
        if app_settings.QUERY_EMAIL:
            scope.append("user:email")
        return scope

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
