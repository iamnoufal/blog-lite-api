from flask_mail import Mail
from flask import current_app as app

mail = Mail(app)

app.app_context().push()