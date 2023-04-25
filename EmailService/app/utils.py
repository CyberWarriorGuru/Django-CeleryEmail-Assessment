import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Django-allauth and Google API libraries
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialApp

# Django-allauth and Microsoft Graph API libraries
from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

def send_email(email, subject, message, recipient_list, attachments=None):
    if email.provider_name.lower() in ['google', 'outlook']:
                # OAuth2 setup
        social_app = SocialApp.objects.get(provider=email.provider_name)
        access_token = email.get_access_token()
        if not access_token:
            access_token = social_app.get_access_token(email.refresh_token)
            email.set_access_token(access_token)
        provider = social_app.get_provider()
        provider.client_id = email.get_client_id()
        provider.secret = email.get_secret_key()
        provider.access_token = access_token
        provider.refresh_token = email.get_refresh_token()
        provider.extra_data['access_token'] = access_token
        provider.save()
    if email.provider_name.lower() == 'other':
        # Get the SMTP settings from the EmailProvider model
        smtp_settings = email.provider.smtp_settings
        smtp_host = smtp_settings.host
        smtp_port = smtp_settings.port
        smtp_username = email.address
        smtp_password = email.provider.get_decrypted_password()

        # Create the email message
        email_message = MIMEMultipart()
        email_message['to'] = email.address
        email_message['subject'] = subject
        email_message.attach(MIMEText(message))

        # Attach any files
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=attachment)
                    email_message.attach(img)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, [email.address], email_message.as_string())
    from django.core.mail import EmailMessage
    email = EmailMessage(subject=subject, body=message, to=recipient_list)
    email.send()

def read_emails(email, max_results=10):
    if email.provider_name.lower() in ['google', 'outlook']:
                # OAuth2 setup
        social_app = SocialApp.objects.get(provider=email.provider_name)
        access_token = email.get_access_token()
        if not access_token:
            access_token = social_app.get_access_token(email.refresh_token)
            email.set_access_token(access_token)
        provider = social_app.get_provider()
        provider.client_id = email.get_client_id()
        provider.secret = email.get_secret_key()
        provider.access_token = access_token
        provider.refresh_token = email.get_refresh_token()
        provider.extra_data['access_token'] = access_token
        provider.save()
    if email.provider_name.lower() == 'other':
        # Get the IMAP settings from the EmailProvider model
        imap_settings = email.provider.imap_settings
        imap_host = imap_settings.host
        imap_port = imap_settings.port
        imap_username = email.address
        imap_password = email.provider.get_decrypted_password()

    # Connect to the IMAP server and select the inbox
    with imaplib.IMAP4_SSL(imap_host, imap_port) as server:
        server.login(imap_username, imap_password)
        server.select('inbox')

        # Search for the latest emails
        result, data = server.search(None, "ALL")
        email_list = []
        for num in data[0].split()[::-1][:max_results]:
            result, msg_data = server.fetch(num, "(RFC822)")
            msg_str = msg_data[0][1].decode('utf-8')
            message = email.message_from_string(msg_str)
            subject = message['Subject']
            sender = message['From']
            date_sent = message['Date']
            body = message.get_payload()[0].get_payload()
            email_list.append({'subject': subject, 'sender': sender, 'date_sent': date_sent, 'body': body})
        return email_list