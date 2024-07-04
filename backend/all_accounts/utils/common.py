from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta


class BaseTimestampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def send_verification_email(user, verification_link: str):
    subject = "Verify your email"
    html_message = render_to_string(
        "emails/email_verification.html",
        {"verification_link": verification_link, "user": user},
    )
    plain_message = strip_tags(html_message)
    from_email = settings.FROM_EMAIL

    send_mail(
        subject, plain_message, from_email, [user.email], html_message=html_message
    )


def encode_token(user):
    expiration = datetime.now() + timedelta(minutes=30)
    payload = {'user_id': user.id, 'email': user.email, 'exp': expiration}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return token


# decode/decrypt token
def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def password_reset_email(user, reset_link: str):
    subject = "Password reset email"
    html_message = render_to_string(
        "emails/password_reset_email.html",
        {"reset_link": reset_link, "user": user},
    )
    plain_message = strip_tags(html_message)
    from_email = settings.FROM_EMAIL

    send_mail(
        subject, plain_message, from_email, [user.email], html_message=html_message
    )
