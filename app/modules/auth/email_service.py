import random
import smtplib
from tkinter import *


class EmailService():
    def __init__(self, sender, password, code):
        self.sender = sender
        self.password = password
        self.code = code

    def sending_mail(self, receiver, server):
        msg = 'Hello! \n This is your OTP: ' + self.code + "."
        
        server.sendmail(self.sender, receiver, msg)
        server.quit()


    def connecting_sender(self, receiver):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        EmailService.sending_mail(self, receiver, server)


    def check_otp(self, code_entry):
        if self.code == code_entry.get():
            print("OKKKKKKKKKKKKKKKKKKKKKKKK")
        else:
            print("NOOOOOOOOOOOOOOOOOOOOOOOO")


def generate_otp():
        randomCode = ''.join(str(random.randint(0, 9)) for i in range(6))
        return str(randomCode)