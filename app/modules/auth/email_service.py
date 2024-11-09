import random
import smtplib


class EmailService():
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    def sending_mail(self, receiver, server, code):
        msg = 'Hello! \n This is your OTP: ' + code + '\n'
        server.sendmail(self.sender, receiver, msg)
        server.quit()


    def connecting_sender(self, receiver, code):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        EmailService.sending_mail(self, receiver, server, code)
