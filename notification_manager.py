import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv()

class NotificationManager:
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    def send_sms(self, message_body):
        """
        Sends an SMS message through the Twilio API.
        :param message_body: (str) The text content of the message to be sent.
        :return: None
        """
        message = self.client.messages.create(
            from_=os.getenv("TWILIO_NUMBER"),
            body=message_body,
            to=os.getenv("MY_NUMBER")
        )
        print(message.sid)

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )