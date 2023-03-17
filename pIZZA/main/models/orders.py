from base.models.basemodel import BaseModel
from django.db import models
from accounts.models.user import User
from main.models.product import Product


class Orders(BaseModel):
    ORDER_PROCESSING = 'processing'
    ORDER_CANCELLED = 'cancelled'
    OUT_OF_DELIVERY = 'out_of_delivery'

    ORDER_STATUS_CHOICES = [
        (ORDER_PROCESSING, 'Order Processing'),
        (ORDER_CANCELLED, 'Order Cancelled'),
        (OUT_OF_DELIVERY, 'Out of Delivery'),
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_PROCESSING)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    quantity = models.IntegerField()
    price = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=100,blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True, null=True)
    razorpay_payment_signature = models.CharField(max_length=100,blank=True, null=True)


