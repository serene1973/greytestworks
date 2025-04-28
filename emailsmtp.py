import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email details
smtp_server = 'smtp.yourserver.com'   # Example: smtp.gmail.com
smtp_port = 587                       # Example: 587 for TLS
smtp_username = 'your_email@example.com'
smtp_password = 'your_password'
from_email = 'your_email@example.com'
to_email = 'recipient@example.com'

# Create the email message
msg = MIMEMultipart()
msg['Subject'] = 'Subject here'
msg['From'] = from_email
msg['To'] = to_email

# Attach the HTML body
html_body = """\
<html>
  <body>
    <h1>Hello!</h1>
    <p>This is an email with an HTML body and a ZIP attachment.</p>
  </body>
</html>
"""
msg.attach(MIMEText(html_body, 'html'))

# Attach the ZIP file
zip_path = 'path/to/your_file.zip'

with open(zip_path, 'rb') as file:
    zip_part = MIMEApplication(file.read(), Name='your_file.zip')
    zip_part['Content-Disposition'] = 'attachment; filename="your_file.zip"'
    msg.attach(zip_part)

# Send the email
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Secure the connection
    server.login(smtp_username, smtp_password)
    server.send_message(msg)

print('Email sent successfully!')
