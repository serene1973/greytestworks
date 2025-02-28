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

    # Dictionary to store test name and related files
    test_cases = {}

    # Collect all test result files
    for file in os.listdir(allure_results_dir):
        file_path = os.path.join(allure_results_dir, file)

        # Read JSON files to associate results with test names
        if file.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    content = json.load(f)
                    test_name = content.get("name")  # Get test name
                    if test_name:
                        if test_name not in test_cases:
                            test_cases[test_name] = []
                        test_cases[test_name].append(file_path)
                except json.JSONDecodeError:
                    continue
        
        # Include other Allure-related files (attachments, XML, etc.)
        else:
            for test_name in test_cases.keys():
                test_cases[test_name].append(file_path)

    # Create separate reports for each test
    for test_name, files in test_cases.items():
        test_results_dir = f"{allure_results_dir}/{test_name}"
        test_report_dir = f"{allure_reports_dir}/{test_name}"

        os.makedirs(test_results_dir, exist_ok=True)

        # Copy all relevant files for the test
        for file_path in files:
            shutil.copy(file_path, os.path.join(test_results_dir, os.path.basename(file_path)))

        # Generate a separate Allure report for each test
        os.system(f"allure generate {test_results_dir} -o {test_report_dir} --clean")

        # Verify if the report was created
        if os.path.exists(test_report_dir):
            print(f"Allure report generated for {test_name} at {test_report_dir}")
        else:
            print(f"Failed to generate Allure report for {test_name}")
