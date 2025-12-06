import net.lightbody.bmp.BrowserMobProxy;
import net.lightbody.bmp.BrowserMobProxyServer;
import net.lightbody.bmp.client.ClientUtil;
import net.lightbody.bmp.filters.RequestFilter;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.net.ServerSocket;
import java.net.URL;
import java.util.Base64;

public class SauceHttpAuthDriver {
    
    private BrowserMobProxy bmp;

    // -------------------------------------------------------------
    // 1. Start BMP Proxy with dynamic port
    // -------------------------------------------------------------
    public BrowserMobProxy startBMP() throws Exception {
        System.setProperty("bmp.allowNativeDnsFallback", "true");

        bmp = new BrowserMobProxyServer();
        bmp.setTrustAllServers(true);  // Enables MITM for HTTPS

        ServerSocket ss = new ServerSocket(0);
        int port = ss.getLocalPort();
        ss.close();

        bmp.start(port);
        return bmp;
    }

    // -------------------------------------------------------------
    // 2. Add HTTP Basic Auth Header to ALL Requests
    // -------------------------------------------------------------
    public void addAuthHeader(String username, String password) {

        // Build Base64 authorization token
        String creds = username + ":" + password;
        String encoded = Base64.getEncoder().encodeToString(creds.getBytes());

        bmp.addRequestFilter((request, contents, messageInfo) -> {
            request.headers().add("Authorization", "Basic " + encoded);
            return null;
        });
    }

    // -------------------------------------------------------------
    // 3. Create Selenium Proxy that Sauce Labs can reach
    //    IMPORTANT: 127.0.0.1 will be mapped through Sauce Connect
    // -------------------------------------------------------------
    public Proxy createSeleniumProxy() {

        Proxy seleniumProxy = ClientUtil.createSeleniumProxy(bmp);

        String host = "127.0.0.1";  // Accessible via Sauce Connect

        seleniumProxy.setHttpProxy(host + ":" + bmp.getPort());
        seleniumProxy.setSslProxy(host + ":" + bmp.getPort());

        return seleniumProxy;
    }

    // -------------------------------------------------------------
    // 4. Create RemoteWebDriver using BMP Proxy
    // -------------------------------------------------------------
    public WebDriver createSauceDriver(Proxy proxy) throws Exception {

        DesiredCapabilities caps = new DesiredCapabilities();
        caps.setCapability("browserName", "chrome");
        caps.setCapability("platformName", "Windows 11");
        caps.setCapability("browserVersion", "latest");

        // Sauce settings
        caps.setCapability("sauce:options", new java.util.HashMap<String, Object>() {{
            put("build", "HTTP_AUTH_TEST");
            put("name", "HTTP Auth via BMP");
            put("seleniumVersion", "4.23.0");
        }});

        caps.setCapability("proxy", proxy);  // <-- IMPORTANT

        return new RemoteWebDriver(
                new URL("https://<SAUCE_USERNAME>:<SAUCE_ACCESS_KEY>@ondemand.us-west-1.saucelabs.com/wd/hub"),
                caps
        );
    }

    // -------------------------------------------------------------
    // 5. Usage Example
    // -------------------------------------------------------------
    public static void main(String[] args) throws Exception {

        SauceHttpAuthDriver util = new SauceHttpAuthDriver();

        // Start BrowserMob Proxy
        util.startBMP();

        // Add Authentication Header
        util.addAuthHeader("corp\\qa-test", "Pass123");

        // Create Selenium Proxy readable by Sauce
        Proxy proxy = util.createSeleniumProxy();

        // Launch driver
        WebDriver driver = util.createSauceDriver(proxy);

        driver.get("https://your-protected-url.com");

        System.out.println("Page title: " + driver.getTitle());

        driver.quit();
    }
}
