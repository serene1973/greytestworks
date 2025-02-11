import pytest
from pytest_html import extras

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """Set a custom title for the HTML report."""
    report.title = "My Custom Pytest Report"

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Add a custom summary section at the end of the report."""
    prefix.append("<p><strong>Summary:</strong> All tests executed.</p>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_header(cells):
    """Modify table headers (e.g., add a new column)."""
    cells.insert(2, "<th>Custom Column</th>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    """Modify table rows (e.g., add a new column value)."""
    cells.insert(2, "<td>Custom Data</td>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_html(report, data):
    """Customize the test result details."""
    if report.passed:
        data.append("<div class='custom-pass'>✔ Test Passed</div>")
    elif report.failed:
        data.append("<div class='custom-fail'>✘ Test Failed</div>")

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Inject CSS and JS using extra HTML."""
    prefix.append(
        '<style>'
        'body { font-family: Arial, sans-serif; }'
        '.custom-pass { color: green; font-weight: bold; }'
        '.custom-fail { color: red; font-weight: bold; }'
        '</style>'
    )
    prefix.append(
        '<script>'
        'document.addEventListener("DOMContentLoaded", function() {'
        '    console.log("Custom JS Loaded!");'
        '});'
        '</script>'
    )
