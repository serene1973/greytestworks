import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """Set a custom title for the HTML report."""
    report.title = "My Custom Pytest Report"

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Add a custom summary section."""
    prefix.append("<p><strong>Summary:</strong> All tests executed successfully.</p>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_html(report, data):
    """Add custom messages for each test."""
    if report.passed:
        data.append("<div class='custom-pass'>✔ Test Passed</div>")
    elif report.failed:
        data.append("<div class='custom-fail'>✘ Test Failed</div>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_template(template, report):
    """Inject custom CSS and JavaScript into the report."""
    template.head.append(
        "<style>"
        "body { font-family: Arial, sans-serif; }"
        ".custom-pass { color: green; font-weight: bold; }"
        ".custom-fail { color: red; font-weight: bold; }"
        "</style>"
    )
    template.body.append(
        "<script>"
        "document.addEventListener('DOMContentLoaded', function() {"
        "    console.log('Custom JS Loaded!');"
        "});"
        "</script>"
    )
