import os
import json
import pytest
import datetime

# Report storage
REPORT_DIR = "reports"
REPORT_FILE = os.path.join(REPORT_DIR, "custom_report.html")
LOGS_FILE = os.path.join(REPORT_DIR, "test_logs.json")

# Ensure reports directory exists
os.makedirs(REPORT_DIR, exist_ok=True)

# Dictionary to store test execution details
test_results = []


def pytest_sessionstart(session):
    """Initialize test report at session start."""
    global test_results
    test_results = []  # Reset results
    with open(LOGS_FILE, "w") as f:
        json.dump([], f)  # Clear previous logs


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test execution details."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # Only capture final test result
        test_name = item.name
        status = "passed" if report.passed else "failed" if report.failed else "skipped"
        duration = round(report.duration, 2)

        # Handle retries
        retry_count = item.session.config.cache.get("pytest_rerunfailures", 0)
        retry_suffix = f"_retry_{retry_count}" if retry_count > 0 else ""

        # Handle parameterized test cases
        param_suffix = ""
        if hasattr(item, "callspec"):  # Check if test is parameterized
            param_suffix = f"_{item.callspec.id}"

        full_test_name = f"{test_name}{param_suffix}{retry_suffix}_{status}"

        # Save test details
        test_results.append({
            "name": full_test_name,
            "status": status,
            "duration": duration,
            "logs": []
        })

        # Save updated results to JSON
        with open(LOGS_FILE, "w") as f:
            json.dump(test_results, f, indent=4)


def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report at session end."""
    generate_html_report()


def generate_html_report():
    """Create a detailed HTML report."""
    with open(LOGS_FILE, "r") as f:
        test_data = json.load(f)

    html_content = f"""
    <html>
    <head>
        <title>Test Execution Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
            .test {{ margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; }}
            .pass {{ color: green; }}
            .fail {{ color: red; }}
            .skipped {{ color: orange; }}
            .logs {{ display: none; margin-top: 10px; }}
            .log-entry {{ font-size: 14px; }}
            .screenshot img {{ max-width: 200px; }}
        </style>
        <script>
            function toggleLogs(id) {{
                var logs = document.getElementById(id);
                logs.style.display = logs.style.display === 'none' ? 'block' : 'none';
            }}
        </script>
    </head>
    <body>
        <div class="header">Test Execution Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    """

    for i, test in enumerate(test_data):
        status_class = "pass" if test["status"] == "passed" else "fail" if test["status"] == "failed" else "skipped"
        html_content += f"""
        <div class="test {status_class}" onclick="toggleLogs('log_{i}')">
            {test['name']} - <b>{test['status'].upper()}</b> - {test['duration']}s
            <div class="logs" id="log_{i}">
        """

        for log in test["logs"]:
            html_content += f'<div class="log-entry">{log["message"]}</div>'
            if "screenshot" in log:
                html_content += f'<div class="screenshot"><img src="{log["screenshot"]}" /></div>'

        html_content += "</div></div>"

    html_content += "</body></html>"

    # Save report
    with open(REPORT_FILE, "w") as f:
        f.write(html_content)

    print(f"Custom HTML report generated: {REPORT_FILE}")



BasePage
import os
import json
from datetime import datetime

class BasePage:
    def __init__(self):
        self.logs_file = "reports/test_logs.json"
    
    def log_report(self, message, screenshot_path=None):
        """Add logs dynamically to test reports."""
        with open(self.logs_file, "r") as f:
            test_data = json.load(f)

        if test_data:
            test_data[-1]["logs"].append({"message": message})
            if screenshot_path:
                test_data[-1]["logs"].append({"screenshot": screenshot_path})

        with open(self.logs_file, "w") as f:
            json.dump(test_data, f, indent=4)

    def take_screenshot(self, driver, filename):
        """Take and store screenshot."""
        screenshot_path = f"reports/{filename}"
        driver.save_screenshot(screenshot_path)
        return screenshot_path
