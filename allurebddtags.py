
@epic:Authentication
@feature:Login Feature
@story:Valid Login
@description:This scenario verifies login with valid credentials.
@critical
Scenario: Login with valid credentials
    Given the user is on the login page
    When the user enters valid credentials
    Then the user is redirected to the dashboard


# conftest.py
import allure
from pytest_bdd import hooks

@hooks.hookimpl
def pytest_bdd_before_scenario(request, feature, scenario):
    tag_map = {
        'blocker': allure.severity_level.BLOCKER,
        'critical': allure.severity_level.CRITICAL,
        'normal': allure.severity_level.NORMAL,
        'minor': allure.severity_level.MINOR,
        'trivial': allure.severity_level.TRIVIAL,
    }

    for tag in scenario.tags:
        if ':' in tag:
            key, value = tag.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            if key == 'epic':
                allure.dynamic.epic(value)
            elif key == 'feature':
                allure.dynamic.feature(value)
            elif key == 'story':
                allure.dynamic.story(value)
            elif key == 'description':
                allure.dynamic.description(value)
        elif tag in tag_map:
            allure.dynamic.severity(tag_map[tag])
