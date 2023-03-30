import os
from dotenv import load_dotenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

def send_simple_message(to_address, subject, body):
    message = Mail(
        from_email='sidney.park22@gmail.com',
        to_emails=to_address,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(
            os.getenv('SENDGRID_API_KEY', '')
        )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def send_user_registration_email(email, username):
    return send_simple_message(
                to_address=email,
                subject='Successfully signed up.',
                body=f'Hi {username}! You have successfully signed up to the Stores REST API.'
    )
