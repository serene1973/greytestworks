import pytest
import shutil
import os
import base64
import requests

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    report_folder = "reports"  # Change to your folder path
    zip_file = "reports.zip"

    # Zip the folder
    shutil.make_archive("reports", "zip", report_folder)

    # Read ZIP file and convert to Base64
    with open(zip_file, "rb") as f:
        zip_base64 = base64.b64encode(f.read()).decode()

    # Email Server Details
    exchange_url = "https://mail.yourcompany.com/EWS/Exchange.asmx"
    username = "your_email@yourcompany.com"
    password = "your_password"

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://schemas.microsoft.com/exchange/services/2006/messages/CreateItem"
    }

    # XML payload for EWS email
    soap_payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
        xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" 
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
        <soap:Header>
            <t:RequestServerVersion Version="Exchange2016"/>
        </soap:Header>
        <soap:Body>
            <m:CreateItem MessageDisposition="SendAndSaveCopy">
                <m:Items>
                    <t:Message>
                        <t:Subject>Test Execution Report</t:Subject>
                        <t:Body BodyType="Text">Find the attached test execution report.</t:Body>
                        <t:ToRecipients>
                            <t:Mailbox>
                                <t:EmailAddress>recipient@example.com</t:EmailAddress>
                            </t:Mailbox>
                        </t:ToRecipients>
                        <t:Attachments>
                            <t:FileAttachment>
                                <t:Name>{zip_file}</t:Name>
                                <t:IsInline>false</t:IsInline>
                                <t:Content>{zip_base64}</t:Content>
                            </t:FileAttachment>
                        </t:Attachments>
                    </t:Message>
                </m:Items>
            </m:CreateItem>
        </soap:Body>
    </soap:Envelope>"""

    # Send the request
    response = requests.post(exchange_url, headers=headers, data=soap_payload, auth=(username, password))

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email: {response.text}")
