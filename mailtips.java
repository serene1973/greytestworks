//construction
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
               xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        <t:RequestServerVersion Version="Exchange2013" 
            xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"/>
    </soap:Header>
    <soap:Body>
        <GetMailTips xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
            <SendingAs>
                <t:EmailAddress>your-email@example.com</t:EmailAddress>
            </SendingAs>
            <Recipients>
                <t:EmailAddress>test@example.com</t:EmailAddress>
            </Recipients>
            <MailTipsRequested>All</MailTipsRequested>
        </GetMailTips>
    </soap:Body>
</soap:Envelope>


//send

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;

public class GetMailTipsExample {
    public static void main(String[] args) {
        try {
            // Exchange Web Services (EWS) URL
            String ewsUrl = "https://your.exchange.server/EWS/Exchange.asmx"; // Update this

            // Credentials
            String username = "your-username";
            String password = "your-password";
            String auth = Base64.getEncoder().encodeToString((username + ":" + password).getBytes());

            // SOAP Request Body
            String soapRequest =
                    "<?xml version='1.0' encoding='utf-8'?>"
                    + "<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
                    + "xmlns:xsd='http://www.w3.org/2001/XMLSchema' "
                    + "xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'>"
                    + "<soap:Header>"
                    + "<t:RequestServerVersion Version='Exchange2013' "
                    + "xmlns:t='http://schemas.microsoft.com/exchange/services/2006/types'/>"
                    + "</soap:Header>"
                    + "<soap:Body>"
                    + "<GetMailTips xmlns='http://schemas.microsoft.com/exchange/services/2006/messages'>"
                    + "<SendingAs>"
                    + "<t:EmailAddress>your-email@example.com</t:EmailAddress>"
                    + "</SendingAs>"
                    + "<Recipients>"
                    + "<t:EmailAddress>test@example.com</t:EmailAddress>"
                    + "</Recipients>"
                    + "<MailTipsRequested>All</MailTipsRequested>"
                    + "</GetMailTips>"
                    + "</soap:Body>"
                    + "</soap:Envelope>";

            // Create connection
            URL url = new URL(ewsUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setRequestProperty("Content-Type", "text/xml; charset=utf-8");
            connection.setRequestProperty("SOAPAction", "http://schemas.microsoft.com/exchange/services/2006/messages/GetMailTips");
            connection.setRequestProperty("Authorization", "Basic " + auth);

            // Send request
            try (OutputStream os = connection.getOutputStream()) {
                os.write(soapRequest.getBytes());
                os.flush();
            }

            // Read response
            int responseCode = connection.getResponseCode();
            if (responseCode == 200) {
                try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        response.append(line);
                    }
                    System.out.println("Response:\n" + response);
                    parseResponse(response.toString()); // Parse response to check if email exists
                }
            } else {
                System.out.println("Error: Response Code " + responseCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void parseResponse(String response) {
        if (response.contains("<InvalidRecipient>true</InvalidRecipient>")) {
            System.out.println("❌ Email does NOT exist.");
        } else if (response.contains("<InvalidRecipient>false</InvalidRecipient>")) {
            System.out.println("✅ Email exists.");
        } else {
            System.out.println("⚠ Unknown response format.");
        }
    }
}


