import pytest
import os
import shutil
import json

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    allure_results_dir = "allure-results"
    allure_reports_dir = "allure-report"

    if not os.path.exists(allure_results_dir):
        return

    # Read all test result files
    test_cases = {}
    for file in os.listdir(allure_results_dir):
        if file.endswith(".json"):
            file_path = os.path.join(allure_results_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    content = json.load(f)
                    test_name = content.get("name")
                    if test_name:
                        if test_name not in test_cases:
                            test_cases[test_name] = []
                        test_cases[test_name].append(file_path)
                except json.JSONDecodeError:
                    continue

    # Create separate reports for each test
    for test_name, files in test_cases.items():
        test_results_dir = f"{allure_results_dir}/{test_name}"
        test_report_dir = f"{allure_reports_dir}/{test_name}"

        os.makedirs(test_results_dir, exist_ok=True)

        # Copy the relevant test files
        for file_path in files:
            shutil.copy(file_path, os.path.join(test_results_dir, os.path.basename(file_path)))

        # Generate a separate report for this test
        os.system(f"allure generate {test_results_dir} -o {test_report_dir}")
