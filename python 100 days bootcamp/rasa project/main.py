import smtplib
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

def send_email(subject, msg, to_email):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('YOUR_EMAIL@gmail.com', 'YOUR_PASSWORD')
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail('YOUR_EMAIL@gmail.com', to_email, message)
        server.quit()
        print("Email sent!")
    except Exception as e:
        print("Email failed:", e)


class ActionSendEmail(Action):
    def name(self) -> str:
        return "action_send_email"

    def run(self, dispatcher, tracker, domain):
        to_email = tracker.get_slot('email')  # assuming you have an email slot
        send_email("Test from Rasa", "This is a test email from Rasa!", to_email)
        dispatcher.utter_message(text="Mail Sent")
        return [SlotSet("email", None)]  # reset the email slot
