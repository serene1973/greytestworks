import io.appium.java_client.ios.IOSDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.net.MalformedURLException;
import java.net.URL;

public class PerfectoIOSLaunch {
    private IOSDriver driver;

    @BeforeClass
    public void setup() throws MalformedURLException {
        String perfectoUrl = "https://your-cloud.perfectomobile.com/nexperience/perfectomobile/wd/hub";
        String securityToken = "your_perfecto_security_token";

        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("platformName", "iOS");
        capabilities.setCapability("model", "iPhone.*"); // Use a specific model if needed
        capabilities.setCapability("platformVersion", "17.*"); // Specify version if required
        capabilities.setCapability("securityToken", securityToken);
        capabilities.setCapability("bundleId", "com.example.yourapp"); // iOS app bundle ID
        capabilities.setCapability("automationName", "XCUITest");
        capabilities.setCapability("autoLaunch", true); // Launch the app automatically
        capabilities.setCapability("autoAcceptAlerts", true); // Handle popups

        driver = new IOSDriver(new URL(perfectoUrl), capabilities);
    }

    @Test
    public void testLaunchIOSApp() {
        assert driver != null : "Driver did not initialize";
        System.out.println("✅ iOS app launched successfully!");
    }

    @AfterClass
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
