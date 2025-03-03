import os
import time

class BasePage:
    """Base class for all page classes, with common utility methods"""

    def __init__(self, driver):
        self.driver = driver
        self.logs = []  # Store logs for the current test execution
        self.screenshot_dir = "reports/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)  # Ensure screenshot directory exists

    def logReport(self, message, status="INFO", screenshot=False):
        """
        Logs a message with a status and optional screenshot.
        
        :param message: Log message
        :param status: Log type (INFO, PASS, FAIL)
        :param screenshot: Boolean, whether to capture a screenshot
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        screenshot_path = ""

        if screenshot:
            screenshot_path = os.path.join(self.screenshot_dir, f"screenshot_{timestamp.replace(':', '-')}.png")
            self.driver.save_screenshot(screenshot_path)  # Capture screenshot using Selenium

        log_entry = {
            "status": status.upper(),  # Convert to uppercase (INFO, PASS, FAIL)
            "timestamp": timestamp,
            "message": message,
            "screenshot": screenshot_path if screenshot else None
        }
        self.logs.append(log_entry)  # Store log for current test

    def get_logs(self):
        """Returns stored logs for report generation"""
        return self.logs
