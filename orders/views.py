import razorpay
from django.shortcuts import render,redirect
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,HttpResponse
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def order_create(request):
    if request.user.is_authenticated:
        user=request.user
        cart = Cart(request)
        if cart.get_total_price()!=0:
            if request.method == 'POST':
                form = OrderCreateForm(request.POST)
                
                if form.is_valid():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.save()
                    for item in cart:
                        OrderItem.objects.create(user=user,order=order, product=item['product'], price=item['price'],
                                                quantity=item['quantity'])
                    cart.clear()
                    return render(request, 'orders/order/verify.html', {'order': order})
            else:
                form = OrderCreateForm(initial={'user': request.user})
            return render(request, 'orders/order/create.html', {'form': form,'cart':cart})
        print("please order")
        messages.info(request,'PLease order  ')
        return redirect('/')
    else:
        url = reverse('signin') 
        return redirect(url)


# def payment(request):
#     return render(request, 'orders/order/payment.html')


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)
from decimal import Decimal

def payment(request,id):
    currency = 'INR'
    # amount = 20000
    order= Order.objects.get(id=id)
    decimal_amount =order.get_total_cost()
    amount_in_paisa = int(decimal_amount)
    amount =amount_in_paisa * 100
    print(amount)
    
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    #     Order id of newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('orders:paymenthandler')
    #     We need to pass these details to frontend
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'orders/order/payment.html', context)


@csrf_exempt
def paymenthandler(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                amount = 20000
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'orders/order/paymentsuccess.html')
                except:
                    return render(request, 'orders/order/paymentfail.html')
            else:
                return render(request, 'orders/order/paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



def view_orders(request):
    if request.user.is_authenticated:
        user= request.user
        get_orders=OrderItem.objects.filter(user=user).order_by('-id')

        context={
            'get_orders':get_orders
        }
        return render(request,'order/my_order.html',context)
    else:
        url = reverse('signin') 
        return redirect(url)


