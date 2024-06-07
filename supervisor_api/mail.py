def format_message(token):
    text = (
        "Sehr geherte*r Nutzer*in,",
        "",
        "Sie wurden als Vorgesetzter im Web-Dienst CLOCK eingetragen.",
        "Um Stundenzettel der Ihnen unterstellten sutdentischen Hilfskräfte einsehen zu können",
        "melden Sie sich bitte unter <HIER URL EINFÜGEN> an.",
        "Für die Erst-Registrierung benötigen Sie folgenden Authentifizierungstoken:",
        "",
        f"{token}",
        "",
        "Bitte nutzen Sie den zu dieser Email-Adresse gehörigen HRZ Account.",
        "Das ist eine automatisch generierte Nachricht von Clock (System URL: https://clock.uni-frankfurt.de)",
    )
    return "\n".join(text)
