from exchangelib import Credentials, Account, Message, Mailbox, FileAttachment, HTMLBody, Configuration, DELEGATE

# Login credentials
username = 'your_username'     # Example: DOMAIN\\username
password = 'your_password'
exchange_url = 'https://yourcompany.com/EWS/Exchange.asmx'
email_address = 'your_email@example.com'

# Setup credentials and config once
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_url.replace('https://', '').split('/')[0],
                        credentials=credentials)
account = Account(primary_smtp_address=email_address, config=config, autodiscover=False, access_type=DELEGATE)

# Load attachment once
zip_path = 'path/to/your_file.zip'
with open(zip_path, 'rb') as f:
    zip_content = f.read()

# List of recipients
recipients = [
    'user1@example.com',
    'user2@example.com',
    'user3@example.com',
    # Add more...
]

# Now loop and send emails
for recipient_email in recipients:
    m = Message(
        account=account,
        subject=f'Hello {recipient_email}',
        body=HTMLBody("""\
            <html>
              <body>
                <h1>Hi!</h1>
                <p>This is a personalized email with ZIP attachment.</p>
              </body>
            </html>
        """),
        to_recipients=[Mailbox(email_address=recipient_email)],
    )

    attachment = FileAttachment(
        name='your_file.zip',
        content=zip_content,
    )
    m.attach(attachment)
    m.send()
    print(f'Email sent to {recipient_email}')

print('All emails sent successfully!')
