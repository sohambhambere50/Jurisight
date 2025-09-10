from flask_mail import Message
from extension import mail
import secrets, string


def send_verification_email(user, code):
    try:
        msg = Message("Your Verification Code",
                    recipients=[user.email],
                    sender=("JuriSight", "sohambhambere55@gmail.com"))
        msg.body = f"Hello {user.username}, \n\n Your verification code is {code}. \n\n It expires in 10 minutes."
        mail.send(msg)
        print("Verification email is send to ",user.email)
    except Exception as e:
        print("Failed to send email:", str(e))