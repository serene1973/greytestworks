Set<Cookie> seleniumCookies = driver.manage().getCookies();


String cookieHeader = seleniumCookies.stream()
        .map(c -> c.getName() + "=" + c.getValue())
        .collect(Collectors.joining("; "));

HttpClient client = HttpClient.newHttpClient();

HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://your-app/download/report.pdf"))
        .header("Cookie", cookieHeader)
        .build();

HttpResponse<Path> response =
        client.send(request, HttpResponse.BodyHandlers.ofFile(
                Paths.get("target/report.pdf")));


PDDocument doc = PDDocument.load(new File("target/report.pdf"));
PDFTextStripper stripper = new PDFTextStripper();
String text = stripper.getText(doc);
doc.close();

assertTrue(text.contains("Invoice Number"));
