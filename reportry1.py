conftest

import pytest
import datetime
import os
from types import SimpleNamespace

# Global storage for test logs
test_logs = SimpleNamespace()
test_logs.data = {}  # Stores logs per test
test_logs.execution_summary = []  # Stores overall execution summary

# Directory for reports
REPORTS_DIR = "custom_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def log_report(status, message, screenshot=None):
    """Logs test execution details with optional screenshot."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "status": status.upper(),  # INFO, PASS, FAIL
        "timestamp": timestamp,
        "message": message,
        "screenshot": screenshot  # Optional screenshot path
    }

    # Get current test execution name (supports retries/multiple data)
    test_name = getattr(test_logs, "current_test", "unknown_test")
    
    if test_name not in test_logs.data:
        test_logs.data[test_name] = []

    test_logs.data[test_name].append(log_entry)

    # Debugging log
    print(f"[{timestamp}] [{status.upper()}] {message}")
    if screenshot:
        print(f"Screenshot: {screenshot}")

def get_logs():
    """Returns collected logs for the current test."""
    test_name = getattr(test_logs, "current_test", "unknown_test")
    return test_logs.data.get(test_name, [])

def clear_logs():
    """Clears logs before a new test starts."""
    test_name = getattr(test_logs, "current_test", "unknown_test")
    test_logs.data[test_name] = []

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Track test start time and initialize logs."""
    test_logs.current_test = f"{item.name}_{len(test_logs.execution_summary) + 1}"
    test_logs.start_time = datetime.datetime.now()
    clear_logs()

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    """Track test end time and generate a structured execution summary."""
    end_time = datetime.datetime.now()
    duration = (end_time - test_logs.start_time).total_seconds()
    
    test_name = test_logs.current_test
    outcome = getattr(item, "report_status", "PASS")  # Default to PASS
    logs = get_logs()

    # Save execution summary
    test_logs.execution_summary.append({
        "test_name": test_name,
        "outcome": outcome,
        "duration": duration,
        "logs": logs
    })

    # Generate report after each test
    generate_html_report()

def pytest_sessionfinish(session, exitstatus):
    """Final report generation after all tests finish execution."""
    generate_html_report(final_report=True)




import os
from jinja2 import Template
from conftest import test_logs, REPORTS_DIR

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .test-container { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
        .pass { color: green; }
        .fail { color: red; }
        .skip { color: orange; }
        .details { display: none; }
        .toggle-btn { cursor: pointer; color: blue; text-decoration: underline; }
    </style>
    <script>
        function toggleDetails(id) {
            var elem = document.getElementById(id);
            if (elem.style.display === "none") {
                elem.style.display = "block";
            } else {
                elem.style.display = "none";
            }
        }
    </script>
</head>
<body>

<h1>Test Execution Report</h1>
<div class="header">
    Total Tests: {{ total_tests }} | Passed: <span class="pass">{{ passed }}</span> | Failed: <span class="fail">{{ failed }}</span> | Skipped: <span class="skip">{{ skipped }}</span>
</div>

{% for test in tests %}
    <div class="test-container">
        <strong>{{ test.test_name }}</strong> ({{ test.duration }}s) - <span class="{{ test.outcome.lower() }}">{{ test.outcome }}</span>
        <span class="toggle-btn" onclick="toggleDetails('log-{{ loop.index }}')">View Logs</span>
        <div id="log-{{ loop.index }}" class="details">
            {% for log in test.logs %}
                <p><strong>[{{ log.timestamp }}] {{ log.status }}</strong>: {{ log.message }}
                {% if log.screenshot %}
                    <br><img src="{{ log.screenshot }}" width="200">
                {% endif %}
                </p>
            {% endfor %}
        </div>
    </div>
{% endfor %}

</body>
</html>
"""

def generate_html_report(final_report=False):
    """Generate an HTML report using Jinja2 templates."""
    template = Template(HTML_TEMPLATE)

    summary = {
        "total_tests": len(test_logs.execution_summary),
        "passed": sum(1 for t in test_logs.execution_summary if t["outcome"] == "PASS"),
        "failed": sum(1 for t in test_logs.execution_summary if t["outcome"] == "FAIL"),
        "skipped": sum(1 for t in test_logs.execution_summary if t["outcome"] == "SKIPPED"),
        "tests": test_logs.execution_summary
    }

    html_content = template.render(summary)

    report_path = os.path.join(REPORTS_DIR, "test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📄 Custom HTML Report Generated: {report_path}")




@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Track test start time and initialize logs."""
    # Unique test identifier including parameters
    test_name = item.nodeid.replace("::", "_").replace("/", "_")
    
    # Append execution count for retries and multiple data
    count = len(test_logs.execution_summary) + 1
    test_logs.current_test = f"{test_name}_{count}"

    test_logs.start_time = datetime.datetime.now()
    clear_logs()
