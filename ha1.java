String username = "YOUR_USER";
String password = "YOUR_PASSWORD";

String credentials = username + ":" + password;
String encoded = Base64.getEncoder().encodeToString(credentials.getBytes());

MutableCapabilities caps = new MutableCapabilities();
caps.setCapability("sauce:options", Map.of(
    "proxy", Map.of(
        "protocol", "http",
        "host", "your-proxy-host",
        "port", 8080,
        "headers", Map.of(
            "Authorization", "Basic " + encoded
        )
    )
));
