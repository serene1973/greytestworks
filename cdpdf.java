// Tab 1
DriverFactory.getdriver().get("homeUrl");

// Get existing driver (do NOT create new one)
ChromeDriver driver = (ChromeDriver) DriverFactory.getdriver();

// Attach DevTools
DevTools devTools = driver.getDevTools();
devTools.createSession();

devTools.send(Network.enable(
        Optional.empty(),
        Optional.empty(),
        Optional.empty()
));

// Register listener BEFORE PDF trigger
AtomicReference<String> pdfUrl = new AtomicReference<>();

devTools.addListener(Network.responseReceived(), response -> {
    String mime = response.getResponse().getMimeType();
    if (mime != null && mime.contains("pdf")) {
        pdfUrl.set(response.getResponse().getUrl());
        System.out.println("PDF detected: " + pdfUrl.get());
    }
});

// click → opens Tab 2
driver.findElement(By.id("link1")).click();
switchToLastTab(driver);

// click → opens Tab 3 (PDF)
driver.findElement(By.id("link2")).click();
