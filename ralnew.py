import pytest
import threading

# Thread-safe storage for test results
test_results = threading.local()
test_results.data = {}

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Extract Rally Test Case ID from test markers and store in test node.
    """
    rally_id_marker = item.get_closest_marker("rally")
    if rally_id_marker:
        item.rally_id = rally_id_marker.args[0]  # Store Rally ID in item

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Collect test case results after test execution.
    """
    outcome = yield
    report = outcome.get_result()

    if not hasattr(test_results, "data"):
        test_results.data = {}

    rally_id = getattr(item, "rally_id", None)
    test_name = item.originalname or item.name  # Base test name

    # Handle parameterized tests
    if hasattr(item, "callspec"):
        param_str = ",".join(str(v) for v in item.callspec.params.values())
        test_name = f"{test_name}({param_str})"

    # Handle retries
    if hasattr(report, "rerun"):
        test_name += f"_retry{report.rerun + 1}"

    # Store results
    if rally_id:
        test_results.data[test_name] = {"rally_id": rally_id, "status": report.outcome}

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Send collected test results to the Rally operation class.
    """
    if hasattr(test_results, "data") and test_results.data:
        rally_operation = RallyOperation()
        rally_operation.update_results(test_results.data)
