from exchangelib import Credentials, Account, Message, Mailbox, FileAttachment, HTMLBody, Configuration, DELEGATE

# Login details
username = 'your_username'
password = 'your_password'
exchange_url = 'https://yourcompany.com/EWS/Exchange.asmx'
email_address = 'your_email@example.com'

# Setup
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_url.replace('https://', '').split('/')[0],
                        credentials=credentials)
account = Account(primary_smtp_address=email_address, config=config, autodiscover=False, access_type=DELEGATE)

# Recipients
to_list = ['user1@example.com', 'user2@example.com']
cc_list = ['ccuser1@example.com']
bcc_list = ['bccuser1@example.com']

# Load the attachment
zip_path = 'path/to/your_file.zip'
with open(zip_path, 'rb') as f:
    zip_content = f.read()

# Create the email
m = Message(
    account=account,
    subject='Hello Team!',
    body=HTMLBody("""\
        <html>
          <body>
            <h1>Hi All!</h1>
            <p>This email has To, CC, and BCC.</p>
          </body>
        </html>
    """),
    to_recipients=[Mailbox(email_address=addr) for addr in to_list],
    cc_recipients=[Mailbox(email_address=addr) for addr in cc_list],
    bcc_recipients=[Mailbox(email_address=addr) for addr in bcc_list],
)

# Attach ZIP
attachment = FileAttachment(
    name='your_file.zip',
    content=zip_content,
)
m.attach(attachment)

# Send
m.send()

print('Email with To, CC, and BCC sent successfully!')
