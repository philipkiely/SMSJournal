from django.db import models
from django.contrib.auth.models import User
import random
from django.conf import settings
import boto3
from django.utils import timezone
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Model of a user.
# Phone: phone number of a user. Format: +1xxxxxxxxxx
# Verif_code: code sent from us to user's phone to verify phone number
# Phone_verified: boolean, self-explanatory
class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=150)
    verif_code = models.IntegerField(blank=True,null=True)
    phone_verified = models.BooleanField(default=False)
    active = models.BooleanField(default=False) #Is the subscription active?
    total_entries = models.IntegerField(default=0)
    last_entry = models.DateTimeField(default=timezone.now)
    stripe_customer_id = models.CharField(max_length = 150, blank = True, null=True)

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

    def __str__(self):
        return self.user.username





    def subscribe(self, token):
        customer = stripe.Customer.create(
        source=token,
        description=self.phone
        )
        print(customer.id)
        self.stripe_customer_id = customer.id
        self.save()
        stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                "plan": settings.STRIPE_PLAN_ID,
                "quantity": 1,
                },
            ]
        )




    def delete_customer(self):
        cust = stripe.Customer.retrieve(self.stripe_customer_id)
        cust.delete()

    def change_card(self, new_token):
        stripe.Customer.modify(self.stripe_customer_id,
        source=new_token)

    def give_discount(self, percent):
        stripe.Customer.modify(self.stripe_customer_id, coupon = "small_discount" )
