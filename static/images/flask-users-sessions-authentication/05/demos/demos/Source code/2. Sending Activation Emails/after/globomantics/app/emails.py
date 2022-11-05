from flask_mail import Message
from app import mail
from flask import render_template, url_for

def send_mail(to, subject, template, **kwargs):
    content = {
        "subject": subject,
        "sender": "Globomantics Team <noreply@globomantics.com>",
        "recipients": [to],
        "template": template,
        "kwargs": kwargs
    }

    msg = create_message(content)
    mail.send(msg)

def create_message(content):
    msg = Message(
        content["subject"],
        sender = content["sender"],
        recipients = content["recipients"]
    )
    msg.body = render_template(content["template"] + ".txt", **content["kwargs"])
    msg.html = render_template(content["template"] + ".html", **content["kwargs"])

    return msg

def send_activation_mail(user):
    send_mail(
        user.email,
        "Confirm Your Account",
        "emails/auth/confirm",
        username=user.username,
        role=user.role_id,
        activation_link=url_for(
            "auth.activate_account",
            token = user.activation_token,
            _external=True
        )
    )
