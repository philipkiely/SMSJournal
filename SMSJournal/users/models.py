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
    verif_code = models.IntegerField()
    phone_verified = models.BooleanField(default=False)
    active = models.BooleanField(default=False) #Is the subscription active?
    total_entries = models.IntegerField(default=0)
    last_entry = models.DateTimeField(default=timezone.now)
    #ToDo: Timezone

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




    '''
    stripe.Product.create(
    name='Weekly Car Wash Service',
    type='service',
    )
    first, create our product for sms journal: one time thing
    stripe.Plan.create(
    nickname="Standard Monthly",
    product="{{CAR_WASH_PRODUCT_ID}}",
    amount=2000,
    currency="usd",
    interval="month",
    usage_type="licensed",
    ) then create the plan, one time thing

    '''


    def subscribe(self, token):
        customer = stripe.Customer.create(
        source=token, #seems that's just a way to refer to payment method
        description=self.phone
        )
        self.stripe_customer_id = customer.id

        # subscribe customer to our thing
        stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                "plan": settings.STRIPE_PLAN_ID,
                "quantity": 1,
                },
            ]
        )

        # charge the first time
        charge = stripe.Charge.create(
        amount=149, # $15.00 this time
        currency='usd',
        description='SMS Journal Charge',
        customer=customer.id, # Previously stored, then retrieved
        )



    def delete_subscription(self):
        # string is subscription_id
        subscription = stripe.Subscription.retrieve('sub_49ty4767H20z6a')
        subscription.delete()

    def change_card(self):
        # do the front-end pop up, it will store the card and then do that
        stripe.Customer.modify('cus_V9T7vofUbZMqpv',
        source='tok_visa',
        )