import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium import webdriver

@pytest.fixture(scope="function")
def mobile_driver(request):
    platform = request.config.getoption("--platform")  # CLI arg for platform

    command_executor = "https://your.perfecto.cloud/wd/hub"

    if platform == "mobile_web":
        capabilities = {
            "platformName": "Android",
            "browserName": "Chrome",
            "platformVersion": "14.0",
            "deviceName": "Samsung Galaxy",
            "perfecto:options": {
                "securityToken": "your_token"
            }
        }
        driver = webdriver.Remote(command_executor=command_executor, options=webdriver.ChromeOptions().from_capabilities(capabilities))

    elif platform == "android_app":
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "Samsung Galaxy"
        options.app = "PUBLIC:your_app.apk"
        options.automation_name = "UiAutomator2"
        options.set_capability("perfecto:options", {"securityToken": "your_token"})

        driver = webdriver.Remote(command_executor=command_executor, options=options)

    elif platform == "ios_app":
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.device_name = "iPhone 14"
        options.app = "PUBLIC:your_app.ipa"
        options.automation_name = "XCUITest"
        options.set_capability("perfecto:options", {"securityToken": "your_token"})

        driver = webdriver.Remote(command_executor=command_executor, options=options)

    else:
        raise ValueError("Unsupported platform")

    yield driver
    driver.quit()
