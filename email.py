from email.message import EmailMessage
import ssl
import smtplib 
import os



class EmailSender():

    def __init__(self) -> None:
        pass 

    def set_sender(self, sender_email):
        self.email_sender = sender_email

    def set_reciepient(self, reciepient):
        self.email_reciever = reciepient

    def set_message(self, message , subject='',):
        self.body = message
        self.subject = subject

    def set_authentication(self, password): 
        self.password = password


    def message_wrapper(self, sender= '', recipient = '', password = '' , message='', subject=''): 
        self.email_reciever = recipient 
        self.email_sender = sender
        self.email_password = password 
        self.subject = subject
        self.body = message


    def send_email(self): 
        status = ''
        if '' in [self.sender , self.recipient, self.message]: 
            status = 'details not provided'
        else: 
            em = EmailMessage()
            em['From']  = self.email_sender
            em['To'] = self.email_reciever
            em['Subject'] = self.subject
            em.set_content(self.body)


            # security layer 
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
                smtp.login(self.email_sender , self.email_password)
                smtp.sendmail(self.email_sender, self.email_reciever, em.as_string())
            
            status = "Email Sent Successfully"
            print('Email Sent Successfully')
        
        return status




eml = EmailSender()

eml.set_sender("binarysamplemail.@gmail.com")
eml.set_reciepient('binarycode1995@gmail.com')
eml.set_authentication(os.environ.get('EMAIL_PASSWORD'))
st = eml.set_message('this is a new message ' , 'Review')
print(st)




# email_sender = 'binarysamplemail.@gmail.com'
# # email_password = 'gqes elop rmtw vkqp'
# email_password = os.environ.get('EMAIL_PASSWORD')
# print(email_password)
# # email_password = 'binary1995'
# email_reciever = 'binarycode1995@gmail.com '

# # body of meial 
# subject = 'customer review'
# body = 'the customer as sturdy the reoveolotion and found the service is good '

# em = EmailMessage()
# em['From']  = email_sender
# em['To'] = email_reciever
# em['Subject'] = subject
# em.set_content(body)


# # security layer 
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
#     smtp.login(email_sender , email_password)
#     smtp.sendmail(email_sender, email_reciever, em.as_string())
    
# print('Email sent')