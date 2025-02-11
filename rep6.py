import pytest
import os

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Modify Allure report styling after test execution."""
    allure_report_dir = "allure-report"  # Adjust if needed
    custom_css = """
    body { background-color: #f4f4f4 !important; font-family: Arial, sans-serif !important; }
    .pane__title { background-color: #007BFF !important; color: white !important; }
    .tag { background-color: #28a745 !important; color: white !important; }
    .status { font-size: 16px !important; font-weight: bold !important; }
    """
    
    css_path = os.path.join(allure_report_dir, "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "a") as css_file:
            css_file.write(custom_css)
        print("✅ Custom CSS applied to Allure Report!")
    else:
        print("⚠ Allure report not found. Run `allure generate` first.")
