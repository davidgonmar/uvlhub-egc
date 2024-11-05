
import random
import smtplib
from tkinter import *


#ESTAS VARIABLES HAY QUE HACER ALGO CON ELLAS

class EmailService():
    def __init__(self, sender, password, code):
        self.sender = sender
        self.password = password
        self.code = code

    def sendingMail(self, receiver, server):
        msg = 'Hello! \n This is your OTP is ' + self.code
        server.sendmail(self.sender, receiver, msg)
        server.quit()


    def connectingSender(self, receiver):
        #receiver = receiverMail.get()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        EmailService.sendingMail(self, receiver, server)


    def checkOTP(self, codeEntry):
        if self.code == codeEntry.get():
            print("OKKKKKKKKKKKKKKKKKKKKKKKK")
        else:
            print("NOOOOOOOOOOOOOOOOOOOOOOOO")


