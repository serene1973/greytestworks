import pytest
from py.xml import html

def pytest_html_report_title(report):
    """Modify the report title"""
    report.title = "Custom Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    """Add a custom message at the end of the report"""
    prefix.extend([html.p("This is a custom summary message.")])

def pytest_html_results_table_header(cells):
    """Modify table headers (e.g., add a new column)"""
    cells.insert(2, html.th("Custom Column"))

def pytest_html_results_table_row(report, cells):
    """Modify each row (e.g., add a custom column value)"""
    cells.insert(2, html.td("Custom Data"))

def pytest_html_results_table_html(report, data):
    """Modify the content inside the results table"""
    if report.passed:
        data.append(html.div("Test passed", class_="custom-pass"))

def pytest_html_report_template(template, report):
    """Inject custom CSS and JavaScript"""
    template.head.append(html.style("""
        body { font-family: Arial, sans-serif; }
        .custom-pass { color: green; font-weight: bold; }
    """))
    template.body.append(html.script("""
        document.addEventListener('DOMContentLoaded', function() {
            alert('Custom JS Loaded!');
        });
    """))
