def format_message(url, name, email, message):
    text = (
        f"Name: {name}",
        f"E-Mail: {email}",
        "Nachricht:",
        "",
        message,
        "",
        "---------",
        "",
        f"Das ist eine automatisch generierte Nachricht von Clock (System URL: {url})",
    )

    return "\n".join(text)
