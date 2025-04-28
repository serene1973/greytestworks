from exchangelib import Credentials, Account, Message, Mailbox, FileAttachment, HTMLBody, Configuration, DELEGATE

# Login credentials
username = 'your_username'     # Example: DOMAIN\\username
password = 'your_password'
exchange_url = 'https://yourcompany.com/EWS/Exchange.asmx'
email_address = 'your_email@example.com'

# Setup credentials and config
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_url.replace('https://', '').split('/')[0],
                        credentials=credentials)

# Connect to your mailbox
account = Account(primary_smtp_address=email_address, config=config, autodiscover=False, access_type=DELEGATE)

# Create the email
m = Message(
    account=account,
    subject='Subject here',
    body=HTMLBody("""\
        <html>
          <body>
            <h1>Hello!</h1>
            <p>This is an HTML body email with ZIP attachment.</p>
          </body>
        </html>
    """),
    to_recipients=[Mailbox(email_address='recipient@example.com')],
)

# Attach the ZIP file
zip_path = 'path/to/your_file.zip'
with open(zip_path, 'rb') as f:
    content = f.read()

attachment = FileAttachment(
    name='your_file.zip',
    content=content,
)
m.attach(attachment)

# Send the email
m.send()

print('Email sent successfully via Exchange!')
