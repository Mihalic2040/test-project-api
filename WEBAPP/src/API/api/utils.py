from django.core.mail import EmailMessage
from random import randint
from .models import User

class Utils():
    @staticmethod
    def send_mail(data):

        # generating mail activation code and sending mail
        
        otp = randint(1000, 99999)
        email = EmailMessage(
            subject=data['email_subject'], body="Your activetion code is: " + str(otp), to=[data['to_email']]
        )        
        email.send()

        # updating user profile

        user_obj = User.objects.get(email = data['to_email'])
        user_obj.otp = otp
        user_obj.save()

        return True

        