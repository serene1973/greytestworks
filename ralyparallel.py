import pytest
import multiprocessing

manager = multiprocessing.Manager()
rally_test_results = manager.dict()  # Shared dictionary across processes

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
    """Update test result, ensuring only the last retry is stored"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        result = "Passed" if report.passed else "Failed" if report.failed else "Skipped"

        marker = item.get_closest_marker("rally_testcase_id")
        if marker:
            testcase_id = marker.args[0]
            test_data = getattr(item.callspec, "params", {}) if hasattr(item, "callspec") else {}

            key = (testcase_id, frozenset(test_data.items()))  # Unique key per test execution
            rally_test_results[key] = {"testcase_id": testcase_id, "test_data": test_data, "result": result}

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Send final results to Rally after parallel execution"""
    rally_ops = RallyOperations()
    final_results = list(rally_test_results.values())  # Convert shared dict to list
    rally_ops.send_results_to_rally(final_results)



//
for -n

import pytest

def pytest_configure_node(node):
    """Ensure Rally results are collected in each pytest-xdist worker"""
    node.workeroutput["rally_results"] = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test results in workeroutput for each process"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        result = "Passed" if report.passed else "Failed" if report.failed else "Skipped"
        marker = item.get_closest_marker("rally_testcase_id")

        if marker:
            testcase_id = marker.args[0]
            test_data = getattr(item.callspec, "params", {}) if hasattr(item, "callspec") else {}

            key = (testcase_id, frozenset(test_data.items()))  # Unique key per test execution
            item.config.workeroutput["rally_results"][key] = {"testcase_id": testcase_id, "test_data": test_data, "result": result}

def pytest_testnodedown(node, error):
    """Aggregate results after each worker finishes"""
    global rally_test_results
    rally_test_results.update(node.workeroutput.get("rally_results", {}))

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Send final results to Rally"""
    rally_ops = RallyOperations()
    final_results = list(rally_test_results.values())  # Convert dict to list
    rally_ops.send_results_to_rally(final_results)
