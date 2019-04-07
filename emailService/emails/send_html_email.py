from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def sendEmail(to_list, subject, template_name, context, sender=settings.EMAIL_HOST_USER):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype = "html"
    return msg.send()
