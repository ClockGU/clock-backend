from ..utils import format_message


def test_format_message():
    output = format_message(
        "http://example.com/feedback",
        "Max Mustermann",
        "max@example.com",
        "Das ist eine Nachricht.",
    )

    expected_one_line = "Name: Max MustermannE-Mail: max@example.comNachricht:Das ist eine Nachricht.---------Das ist eine automatisch generierte Nachricht von Clock (System URL: http://example.com/feedback)"

    output_one_line = "".join([line.replace("\n", "") for line in output.rstrip()])

    assert output_one_line == expected_one_line
