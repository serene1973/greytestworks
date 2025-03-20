import pytest

# List to store Rally Test Case IDs and Results
rally_test_results = []

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Collect test case IDs before execution."""
    global rally_test_results
    for item in items:
        marker = item.get_closest_marker("rally_testcase_id")
        if marker:
            testcase_id = marker.args[0]
            rally_test_results.append({"testcase_id": testcase_id, "result": "Not Executed"})

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result after execution"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":  # Only capture the final outcome
        result = "Passed" if report.passed else "Failed" if report.failed else "Skipped"
        
        # Update the corresponding test case result
        marker = item.get_closest_marker("rally_testcase_id")
        if marker:
            testcase_id = marker.args[0]
            for test in rally_test_results:
                if test["testcase_id"] == testcase_id:
                    test["result"] = result
                    break

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Send all collected results to Rally at the end of execution"""
    rally_ops = RallyOperations()
    rally_ops.send_results_to_rally(rally_test_results)


class RallyOperations:
    def send_results_to_rally(self, test_results):
        """Send test results to Rally API"""
        for test in test_results:
            testcase_id = test["testcase_id"]
            result = test["result"]
            print(f"Updating Rally: TestCase {testcase_id} -> Result: {result}")
            # Replace print with actual Rally API call logic
