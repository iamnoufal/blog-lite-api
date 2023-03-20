from flask_mail import Mail, Message
from flask import current_app as app

mail = Mail(app)
app.app_context().push()

def send_notification(sub, body, recipients):
  msg = Message(sub, recipients=recipients)
  msg.body = 'etet'
  mail.send(msg)