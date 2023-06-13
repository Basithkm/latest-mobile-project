from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields =['order','product','price','quantity']
    raw_id_fields = ['product']




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name','order_status','get_total_cost','paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated',]
    inlines = [OrderItemInline,]
