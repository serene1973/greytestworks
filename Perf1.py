import pytest
from appium import webdriver as appium_driver
from selenium import webdriver as selenium_driver

@pytest.fixture(scope="function")
def mobile_driver(request):
    platform = request.config.getoption("--platform")  # Pass platform as CLI arg
    
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
        driver = selenium_driver.Remote(command_executor="https://your.perfecto.cloud/wd/hub", options=capabilities)
    
    elif platform == "android_app":
        capabilities = {
            "platformName": "Android",
            "app": "PUBLIC:your_app.apk",
            "automationName": "UiAutomator2",
            "deviceName": "Samsung Galaxy",
            "perfecto:options": {
                "securityToken": "your_token"
            }
        }
        driver = appium_driver.Remote(command_executor="https://your.perfecto.cloud/wd/hub", options=capabilities)

    elif platform == "ios_app":
        capabilities = {
            "platformName": "iOS",
            "app": "PUBLIC:your_app.ipa",
            "automationName": "XCUITest",
            "deviceName": "iPhone 14",
            "perfecto:options": {
                "securityToken": "your_token"
            }
        }
        driver = appium_driver.Remote(command_executor="https://your.perfecto.cloud/wd/hub", options=capabilities)

    else:
        raise ValueError("Unsupported platform")

    yield driver
    driver.quit()
