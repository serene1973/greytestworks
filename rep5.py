import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """Set a custom title for the HTML report."""
    report.title = "My Custom Pytest Report"

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Add a custom summary and inject CSS for styling."""
    prefix.append("<p><strong>Summary:</strong> All tests executed.</p>")

    # Inject custom CSS to override default styles
    prefix.append(
        '<style>'
        'body { font-family: Arial, sans-serif; background-color: #f8f9fa; }'
        'table { border-collapse: collapse; width: 100%; }'
        'th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }'
        'th { background-color: #007BFF; color: white; font-size: 14px; }'
        'td { font-size: 13px; }'
        '.col-md-4, .col-md-6 { width: 100% !important; }'  /* Expands Environment section */
        '.pytest-html-header { background-color: #343a40; color: white; padding: 10px; }'
        '.pytest-html-log { background-color: #282c34; color: #61dafb; font-size: 14px; }'
        '.pytest-html-summary { background-color: #e9ecef; padding: 10px; font-size: 14px; }'
        '.pytest-html-environment { background-color: #ffffff; color: #333; padding: 10px; font-size: 14px; }'
        '</style>'
    )

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_html(report, data):
    """Customize test result details."""
    if report.passed:
        data.append("<div class='custom-pass'>✔ Test Passed</div>")
    elif report.failed:
        data.append("<div class='custom-fail'>✘ Test Failed</div>")
