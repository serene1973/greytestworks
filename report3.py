import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Clear logs at the start of each test."""
    clear_logs()

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    """Generate an HTML report after each test."""
    from generate_html import generate_html_report  # Import your HTML report function

    test_name = item.name
    outcome = "PASS"  # Assume pass, will override on failure
    duration = 0  # Add actual duration tracking if needed

    if hasattr(item, "report_status"):
        outcome = item.report_status

    generate_html_report(
        filename=f"report_{test_name}.html",
        test_name=test_name,
        outcome=outcome,
        duration=duration,
        nodeid=item.nodeid,
        retry_count=getattr(item, "execution_count", 0),
        logs=get_logs()
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test status (PASS/FAIL) for reporting."""
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        item.report_status = "FAIL"
    elif report.skipped:
        item.report_status = "SKIP"
    else:
        item.report_status = "PASS"
