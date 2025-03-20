import pytest

# List to store Rally Test Case results
rally_test_results = {}

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Initialize test case results before execution"""
    global rally_test_results
    for item in items:
        marker = item.get_closest_marker("rally_testcase_id")
        if marker:
            testcase_id = marker.args[0]
            test_data = getattr(item.callspec, "params", {}) if hasattr(item, "callspec") else {}

            key = (testcase_id, frozenset(test_data.items()))  # Unique key per test execution
            rally_test_results[key] = {
                "testcase_id": testcase_id,
                "test_data": test_data,
                "result": "Not Executed"
            }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Update test result, but only store the latest retry outcome"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # Capture final test call result
        result = "Passed" if report.passed else "Failed" if report.failed else "Skipped"

        marker = item.get_closest_marker("rally_testcase_id")
        if marker:
            testcase_id = marker.args[0]
            test_data = getattr(item.callspec, "params", {}) if hasattr(item, "callspec") else {}

            key = (testcase_id, frozenset(test_data.items()))  # Unique key per test execution
            rally_test_results[key]["result"] = result  # Always update with the latest retry result

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Send final results to Rally at the end of execution"""
    rally_ops = RallyOperations()
    final_results = list(rally_test_results.values())  # Convert dict to list
    rally_ops.send_results_to_rally(final_results)



