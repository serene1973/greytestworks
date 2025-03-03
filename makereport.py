import pytest
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test execution results and generate an HTML report for each execution"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        test_name = item.name
        nodeid = item.nodeid
        outcome = report.outcome  # passed, failed, skipped
        duration = round(report.duration, 2)
        retry_count = getattr(report, "rerun", 0)  # Capture retries
        suffix = f"_retry{retry_count}" if retry_count > 0 else ""

        # Handle parameterized tests
        param_suffix = ""
        if hasattr(item, "callspec"):
            param_suffix = "_" + "_".join(str(v) for v in item.callspec.params.values())

        # Generate unique report filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"report_{test_name}{param_suffix}{suffix}_{timestamp}.html"

        # Retrieve logs from BasePage instance
        base_page = getattr(item.instance, "base_page", None)
        logs = base_page.get_logs() if base_page else []



import json
import os

def generate_html_report(filename, test_name, outcome, duration, nodeid, retry_count, logs):
    """Generate and save an enhanced HTML report with collapsible logs and JSON export"""

    # Define report directory
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    file_path = os.path.join(report_dir, filename)
    json_file_path = file_path.replace(".html", ".json")

    # Save logs to JSON file
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(logs, json_file, indent=4)

    # HTML content with collapsible logs
    html_content = f"""
    <html>
    <head>
        <title>Test Report - {test_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid black; padding: 10px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .pass {{ background-color: #c8e6c9; }}
            .fail {{ background-color: #ffcdd2; }}
            .skip {{ background-color: #ffeb3b; }}
            .log-container {{ margin-top: 20px; display: none; }}
            .toggle-button {{ cursor: pointer; color: blue; text-decoration: underline; }}
            .screenshot img {{ max-width: 300px; margin-top: 5px; }}
            .status-info {{ color: blue; }}
            .status-pass {{ color: green; font-weight: bold; }}
            .status-fail {{ color: red; font-weight: bold; }}
        </style>
        <script>
            function toggleLogs() {{
                var logContainer = document.getElementById("log-container");
                if (logContainer.style.display === "none") {{
                    logContainer.style.display = "block";
                }} else {{
                    logContainer.style.display = "none";
                }}
            }}
        </script>
    </head>
    <body>
        <h2>Test Execution Report</h2>
        <table>
            <tr><th>Test Name</th><td>{test_name}</td></tr>
            <tr><th>Status</th><td class="{outcome}">{outcome.capitalize()}</td></tr>
            <tr><th>Total Time Taken</th><td>{duration} seconds</td></tr>
            <tr><th>Node ID</th><td>{nodeid}</td></tr>
            <tr><th>Retry Count</th><td>{retry_count}</td></tr>
        </table>

        <p class="toggle-button" onclick="toggleLogs()">Click to View/Hide Logs</p>

        <div id="log-container" class="log-container">
            <h3>Test Logs</h3>
            <table>
                <tr>
                    <th>Status</th>
                    <th>Timestamp</th>
                    <th>Message</th>
                    <th>Screenshot</th>
                </tr>
    """

    for log in logs:
        status_class = f"status-{log['status'].lower()}"
        html_content += f"""
        <tr>
            <td class="{status_class}">{log["status"]}</td>
            <td>{log["timestamp"]}</td>
            <td>{log["message"]}</td>
        """
        if log["screenshot"]:
            html_content += f'<td class="screenshot"><img src="{log["screenshot"]}" alt="Screenshot"></td>'
        else:
            html_content += "<td></td>"

        html_content += "</tr>"

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """

    # Save the HTML report
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated report: {file_path}")
    print(f"JSON log file: {json_file_path}")
