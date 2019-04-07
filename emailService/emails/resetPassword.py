from .send_html_email import sendEmail

def urlResetPassword(email, data):
    subject = 'Nueva contraseña'
    to_list = [email]
    template_name = 'emailService/resetPasswordTemplate.html'
    context = data
    sendEmail(to_list,subject,template_name,context)