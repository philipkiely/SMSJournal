from django.db import models
from django.contrib.auth.models import User
import random
from django.conf import settings
import boto3


# Model of a user.
# Phone: phone number of a user. Format: +1xxxxxxxxxx
# Verif_code: code sent from us to user's phone to verify phone number
# Phone_verified: boolean, self-explanatory
class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=150)
    verif_code = models.IntegerField()
    phone_verified = models.BooleanField(default=False)

    # Send 6 digit code to the user for verification
    def send_code(self):
        client = boto3.client('pinpoint')
        pinpoint_id = settings.AWS_PINPOINT_PROJECT_ID
        code = random.randint(100000, 999999)
        self.verif_code = code
        client.send_messages(
            ApplicationId=pinpoint_id,
            MessageRequest={
                'Context': {},
                'Addresses': {
                    self.phone: {
                        "ChannelType": "SMS"
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': 'Welcome to SMS Journal! Your verification code: {}'.format(code),
                        'OriginationNumber': "+19705077992",
                        'MessageType': 'TRANSACTIONAL'
                    }
                }
            }
        )
