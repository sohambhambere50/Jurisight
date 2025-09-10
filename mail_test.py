from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Same config you have in .env
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "sohambhambere55@gmail.com"
app.config['MAIL_PASSWORD'] = "lxjeokzbxrleefcf"  # no spaces
app.config['MAIL_DEFAULT_SENDER'] = "sohambhambere55@gmail.com"

mail = Mail(app)

with app.app_context():
    msg = Message(
        subject="Test Email from Flask",
        recipients=["sohambhambere5050@gmail.com"],  # try another email
        sender=("JuriSight", "sohambhambere55@gmail.com"),
        body="This is a test email sent using Flask-Mail + Gmail."
    )
    mail.send(msg)
    print(" Test email sent")
