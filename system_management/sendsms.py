from twilio.rest import Client
from django.conf import settings

def new_account_sms(to_number, message_body):
    """
    Sends an SMS message using Twilio.
    
    :param to_number: The recipient's phone number in E.164 format (e.g., '+1234567890').
    :param message_body: The content of the SMS message.
    :return: Message SID if the message is sent successfully, None otherwise.
    """
    try:
        # Initialize the Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send the SMS message
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
            to=to_number
        )

        # Return the message SID as confirmation
        return message.sid

    except Exception as e:
        # Handle exceptions (e.g., network issues, invalid numbers)
        print(f"Failed to send SMS: {e}")
        return None

def send_status_sms(user_email, user_first_name, status, url):
    message_body = f"Dear {user_first_name}, your application status has been updated to {status}. Please login to check the details. {url}"
    new_account_sms(user_email, message_body)

