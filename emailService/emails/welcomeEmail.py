from .send_html_email import sendEmail

def welcomEmail(email, data):
    subject = 'Welcome'
    to_list = [email]
    template_name = 'emailService/welcomeTemplate.html'
    context = data
    sendEmail(to_list,subject,template_name,context)
    


   
   


    



