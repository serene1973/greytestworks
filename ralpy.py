import pytest
import threading

# Thread-safe dictionary to store results
test_results = threading.local()
test_results.data = {}

@pytest.fixture
def rally_testcase(request):
    """
    Fixture to retrieve the Rally test case ID from the test function.
    """
    rally_id = getattr(request.node, "rally_id", None)
    return rally_id

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Assign Rally Test Case ID from test case markers.
    """
    rally_id_marker = item.get_closest_marker("rally")
    if rally_id_marker:
        item.rally_id = rally_id_marker.args[0]

    return None  # Continue with pytest execution

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Collect test case results.
    """
    outcome = yield
    report = outcome.get_result()

    if not hasattr(test_results, "data"):
        test_results.data = {}

    rally_id = getattr(item, "rally_id", None)
    test_name = item.originalname or item.name  # Get base test name

    # Handle parameterized tests with different test data
    if hasattr(item, "callspec"):
        param_str = ",".join(str(v) for v in item.callspec.params.values())
        test_name = f"{test_name}({param_str})"

    # Handle retries
    if hasattr(report, "rerun"):
        test_name += f"_retry{report.rerun + 1}"

    # Store result in dictionary
    if rally_id:
        test_results.data[test_name] = {"rally_id": rally_id, "status": report.outcome}

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Send collected test case results to Rally operation class.
    """
    if hasattr(test_results, "data") and test_results.data:
        # Call your Rally operation class method here
        rally_operation = RallyOperation()
        rally_operation.update_results(test_results.data)


import pytest

@pytest.mark.rally("TC12345")
def test_example_1(rally_testcase):
    assert True

@pytest.mark.rally("TC67890")
@pytest.mark.parametrize("data", ["data0", "data1"])
def test_example_2(rally_testcase, data):
    assert data != "data1"

@pytest.mark.rally("TC99999")
def test_example_3():
    assert False  # This will be retried



