import datetime
from django.shortcuts import redirect, render
from customer.models import Order
from restaurent_manager.models import Category,Product
from django.contrib.auth.models import User
from restaurent_manager.forms import ImageForm
import os
from django.db.models import Sum
from django.db.models.functions import ExtractMonth



def dashboard(request):
    if request.user.is_authenticated:
       user=User.objects.get(id=request.user.id)
       if(user.is_staff==False):
         return redirect("/customer")
       

       orders=Order.objects.all()
      
       total_sum = Order.objects.aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
       total_orders_count = Order.objects.count()
       total_users = User.objects.count()
       total_products = Product.objects.count()
       context = {
        'total_sum': total_sum,
        'total_orders_count': total_orders_count,
        'total_users': total_users,
        'total_products': total_products,
        'orders':orders,
        }

        
       return render(request, "restaurent_manager/manager_dashboard.html", context)
    else:
        return redirect('/')
    




from django.shortcuts import render
from django.contrib.auth.models import User
from customer.models import Profile,Reservation
def customer_list_view(request):
    # Retrieve all customer profiles
    customers = Profile.objects.all() 
    

    data = {
        'customers': customers,
    }
    return render(request, 'restaurent_manager/customer_list.html', context=data)


def reservation_list_view(request):
    # Retrieve all customer profiles
    reservations= Reservation.objects.all() 
    

    data = {
        'reservations': reservations,
    }
    return render(request, 'restaurent_manager/reservation_list.html', context=data)


  



def orders_view(request):
    if request.user.is_authenticated:
     orders = Order.objects.all()  # Fetch all orders
    
    context = {
        'orders': orders,
    }
    return render(request, 'restaurent_manager/orders_list.html', context)



def add_category(request):
    data = {}
 
    categories = Category.objects.all()
    data['categories'] = categories
    
   
    if (request.method == 'POST'):
        category = request.POST.get('category')
        
      
        if (category == ""):
            data["error_msg"] = "Category can't be empty"
        elif Category.objects.filter(name=category).exists():
            data["error_msg"] = f"{category} already exists"
        else:
          
            new_category = Category.objects.create(name=category)
            new_category.save()
            return redirect("/restaurent_manager/categories/")  # Updated redirect URL
    
    return render(request, 'restaurent_manager/add_category.html', context=data) 
 

def delete_category(request,category_id):
    category =Category.objects.get(id=category_id)
    category.delete()
    return redirect('/restaurent_manager/categories/')






def add_product(request, category_id):
    data = {}
    category = Category.objects.get(id=category_id)
    data['category_name'] = category.name

    if request.method == "POST":
        pname = request.POST.get("food_name")
        pprice = request.POST.get("food_price")
        pdescription = request.POST.get("food_description")
       
        pimage = request.FILES.get("image")
        
        # Capture the Deliverable value, set to False if not provided
        p_deliverable = request.POST.get("Deliverable", "False")  # defaulting to "False"
        
        # Creating the product instance
        product = Product.objects.create(
            food_name=pname,
            food_price=pprice,
            food_description=pdescription,
       
            image=pimage,
            category_id=category,
            Deliverable=p_deliverable == "True",  # Convert string to boolean
            restaurent_manager_id=request.user
        )
        
        product.save()
        return redirect("/restaurent_manager")

    return render(request, 'restaurent_manager/add_product.html', context=data)





def view_product(request):
    data = {}
    products = Product.objects.filter(restaurent_manager_id=request.user.id)
    # print(products)  # Debugging: Print products to the console

    data["products"] = products
    data["total_products"] = products.count()
    return render(request, 'restaurent_manager/view_product.html', data)
 




def delete_product(request,product_id):
    product=Product.objects.filter(id=product_id)
    product.delete()
    return redirect("/restaurent_manager/categories/view-product")
    
def update_product(request, product_id):
    data = {}
    products = Product.objects.filter(id=product_id)

    if products.exists():
        # Fetch the first product in the queryset
        product = products.first()
        data['product'] = product
    else:
        # Handle case where the product is not found
        return redirect('/restaurent_manager/categories/view-product')  # or return a 404 page

    if request.method == "POST":
        pname = request.POST.get("food_name")
        pprice = request.POST.get("food_price")
        pdescription = request.POST.get("food_description")
        
        pimage = request.FILES.get("image")
        p_deliverable = request.POST.get("Deliverable") == "on"  # Handle checkbox input

        # Update the product details
        products.update(
            food_name=pname,
            food_price=pprice,
            food_description=pdescription,
          
            Deliverable=p_deliverable
        )

        # Handle image upload separately
        if pimage:
            # Fetch the updated product instance
            product = products.first()  # Retrieve the updated product instance
            if product.image and os.path.exists(product.image.path):
                os.remove(product.image.path)
            product.image = pimage
            product.save()

        return redirect("/restaurent_manager/categories/view-product")
    
    return render(request, 'restaurent_manager/update_product.html', context=data)



def admin_order_list(request):
    # Fetch all orders from the database
    orders = Order.objects.all()  # You can add ordering if needed, e.g., .order_by('-date_created')
    return render(request, 'restaurent_manager/order_list.html', {'orders': orders})
# views.py in restaurent_manager app
from django.shortcuts import render, redirect, get_object_or_404
from customer.models import Order
from django.contrib import messages

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'restaurent_manager/orderdetails.html', {'order': order})




 
from django.http import BadHeaderError, HttpResponse, JsonResponse
from customer.models import Order
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse



def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('delivery_status')
        if new_status in dict(Order.DELIVERY_STATUS_CHOICES):  # Ensure it's a valid status
            order.delivery_status = new_status
            order.save()
            return redirect('orders_view')

    return render(request, 'restaurent_manager/update_order_status.html', {'order': order})