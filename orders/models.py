from django.db import models
from store_app.models import MobilePouch
from registration.models import Account


# Create your models here.
class Order(models.Model):
    ORDER_STATUS_PENDING = 'PENDING'
    ORDER_STATUS_ACCEPTED = 'ACCEPTED'
    ORDER_STATUS_PACKED = 'PACKED'
    ORDER_STATUS_DELIVERED = 'DELIVERED'
    ORDER_STATUS_CHOICES = [

        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_ACCEPTED, 'Accepted'),
        (ORDER_STATUS_PACKED, 'Packed'),
        (ORDER_STATUS_DELIVERED, 'Delivered')
    ]
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone=models.CharField(max_length=12)
    address = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    provider_order_id = models.CharField(max_length=200, null=True, blank=True)
    payment_id =models.CharField(max_length=200, null=True, blank=True)
    signature_id =models.CharField(max_length=200, null=True, blank=True)
    payment_status =models.CharField(max_length=200, null=True, blank=True)
    payment_method=models.CharField(max_length=200, null=True, blank=True)
    upi_transaction_id =models.CharField(max_length=200, null=True, blank=True)

    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_ACCEPTED) 
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(MobilePouch, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f' {self.id}'

    def get_cost(self):
        return self.price * self.quantity
