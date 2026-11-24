from django.shortcuts import render, redirect
from . models import order,orderedItem
from products.models import product as Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_cart(request):
    user = request.user
    customer = user.customer_profile
    cart_obj,created = order.objects.get_or_create(
        owner=customer,
        order_status=order.CART_STAGE
    )
    context= {'cart':cart_obj}
    return render(request,'cart.html',context)

def remove_item_from_cart(request,pk):
    item = orderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

def checkout_cart(request):
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            total=request.POST.get('total')
            order_obj=order.objects.get(
                owner=customer,
                order_status=order.CART_STAGE
            )
            order_obj.order_status=order.ORDER_CONFIRMED
            order_obj.total_price=total
            order_obj.save()
            if order_obj:
                status_message='your order is confirmed. your order will be delivered within few days!'
                messages.success(request,status_message)
            else:
                status_message='unable to process. No items in cart'
                messages.error(request,status_message)
        except Exception as e:
            status_message='unable to process. NO items in cart'
            messages.error(request,status_message)
    return redirect('cart')

@login_required(login_url='account')
def show_order(request):
   user=request.user
   customer=user.customer_profile
   all_orders=order.objects.filter(owner=customer).exclude(order_status=order.CART_STAGE)
   context={'orders':all_orders}
   return render(request, 'order.html', context)

@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')

        cart_obj, created= order.objects.get_or_create(
            owner=customer,
            order_status=order.CART_STAGE
        )
        product =Product.objects.get(pk=product_id)
        ordered_item, created =orderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
            quantity=quantity
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()

    return redirect('cart')