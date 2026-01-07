String url = "https://api.us-west-1.saucelabs.com/v1/test/files/" + sessionId;

HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(url))
        .header("Authorization", basicAuth())
        .GET()
        .build();

HttpResponse<String> response =
        HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());

System.out.println(response.body());

String downloadUrl =
  "https://api.us-west-1.saucelabs.com/v1/test/files/"
  + sessionId + "/" + fileId;

HttpRequest downloadReq = HttpRequest.newBuilder()
        .uri(URI.create(downloadUrl))
        .header("Authorization", basicAuth())
        .GET()
        .build();

HttpResponse<byte[]> pdfResponse =
        HttpClient.newHttpClient().send(downloadReq, HttpResponse.BodyHandlers.ofByteArray());

Files.write(Paths.get("downloaded.pdf"), pdfResponse.body());


private static String basicAuth() {
    String auth = SAUCE_USERNAME + ":" + SAUCE_ACCESS_KEY;
    return "Basic " + Base64.getEncoder().encodeToString(auth.getBytes());
}
