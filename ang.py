class AngularAwareDriver:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_angular(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return window.angular !== undefined && "
                                       "angular.element(document.body).injector().get('$http').pendingRequests.length === 0"))

    def click(self, element):
        self.wait_for_angular()
        element.click()

    def send_keys(self, element, text):
        self.wait_for_angular()
        element.send_keys(text)
