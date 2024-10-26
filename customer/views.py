import profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import razorpay
from restaurent_manager.models import Category, Product
from django.db.models import Q  
from customer.models import Cart, Order, OrderItem,Profile,Reservation
from django.contrib import messages 
from django.core.mail import send_mail

# Initialize an empty QuerySet for the products variable globally
products=Product.objects.none()
def home(request):
    # Initialize an empty dictionary to store data to be passed to the template
   data={}
     
    # Declare the global variable 'products' to modify its value within the function
   global products
    # Declare the global variable 'products' to modify its value within the function
   global filtered_products
   # Fetch all Product objects from the database and assign them to the global 'products' variable
   products= Product.objects.all()
    # Set 'filtered_products' to the same as 'products' (this could be used later for filtering)
   filtered_products = products
    # Add the 'products' QuerySet to the 'data' dictionary to pass to the template
   data["products"]=products
    # Check if the user is authenticated (logged in)
   if(request.user.is_authenticated):
      # Get the current user's ID and store it in 'user_id'
      user_id = request.user.id
          # Print the user ID to the console (for debugging purposes)
      print(user_id)
      user=User.objects.get(id=user_id)
     # Retrieve the User object based on the 'user_id'
      if(user.is_staff==True):
         return redirect("/restaurent_manager")
    # Count the number of Cart items associated with the current user (using their ID) and store in 'cart_count'
      cart_count= Cart.objects.filter(customer_id=request.user.id).count()
       # Print the cart count to the console (for debugging purposes)
      data["cart_count"]=cart_count
      print(cart_count)

    # Add all Category objects to the 'data' dictionary to be passed to the template

   data['categories']=Category.objects.all()

      

   return render(request,'customer/base.html',context=data)






def user_register(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect("/")

    # Initialize data dictionary for passing to the template
    data = {}
    is_staff = False

    # Check if a restaurent_manager already exists

         # Disable the restaurent_manager option

    # If the method is POST, handle the registration
        # If the request method is POST (i.e., the form has been submitted)
    if request.method == "POST":
         # Retrieve the submitted username, password, confirmed password, and user type (from the POST request)
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        ucpass = request.POST.get("cpassword")
        utype = request.POST.get("type")

        # Check if someone tries to register as a restaurent_manager after one already exists
        if utype == "restaurent_manager":
             # If a restaurent_manager (staff member) already exists, show an error message
            if User.objects.filter(is_staff=True).exists():
                data["error_msg"] = "A restaurent manager is already registered. No more registrations allowed."
            else:
            # If no restaurant manager exists, set 'is_staff' to True to register the new user as one
                is_staff = True

        # Check for form errors
        if uname == "" or upass == "" or ucpass == "":
            data["error_msg"] = "Fields can't be empty"
        # Check if the password and confirm password do not match
        elif upass != ucpass:
            data["error_msg"] = "Passwords do not match"
        elif User.objects.filter(username=uname).exists():
            data["error_msg"] = f"{uname} already exists"
        elif not data.get("error_msg"):  # Ensure no prior errors
            # Create the user with appropriate is_staff flag
            user = User.objects.create(username=uname, is_staff=is_staff)
            user.set_password(upass)
            user.save()
            return redirect("/login")

    return render(request, 'customer/register.html', context=data)


def user_login(request):
    if(request.user.is_authenticated):
        return redirect("/")
    data = {}
    if(request.method == "POST"):
        uname = request.POST.get("username")
        upass = request.POST.get("password")
        if(uname == "" or upass == ""):
            data["error_msg"] = "Fields can't be empty"
        elif(not User.objects.filter(username=uname).exists()):
            data["error_msg"] = uname + " does not exist"
        else:
            authenticated_user = authenticate(username=uname, password=upass)
            if(authenticated_user is None):
                data["error_msg"] = "Incorrect password"
            else:
                login(request, authenticated_user)
                if(authenticated_user.is_staff):
                   return redirect("/restaurent_manager")
                else:
                    return redirect('/')
    return render(request, "customer/login.html", context=data)

def user_logout(request):
     logout(request)
     return redirect("/")




def make_reservation(request):
    if request.method == 'POST':
        # Get data directly from request.POST
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests')

        # Create and save the reservation
        reservation = Reservation(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            special_requests=special_requests
        )
        reservation.save()
        messages.success(request, "Your reservation has been made successfully!")
        return redirect('/')  # Redirect to a success page or home page

    return render(request, 'customer/make_reservation.html')


def add_to_cart(request,product_id):
      # if customer is authenticated then only add products to cart
   
    if request.user.is_authenticated: 
        
        # from django.db.models import Q  
        # from customer.models import Cart  
        # from django.contrib import messages  
        # Import Q for complex query filtering (already commented out for later use)
        # from django.db.models import Q

        # Import the Cart model (already commented out for later use)
        # from customer.models import Cart

        # Import messages for displaying success/error messages to the user (already commented out for later use)
        # from django.contrib import messages

        # Create two query conditions: 
        # q1 checks if the current customer (user) matches the customer ID in the cart
        # q2 checks if the product ID matches the product in the cart

        q1 = Q(customer_id=request.user.id)  
        q2 = Q(product_id=product_id)  
        cart_items = Cart.objects.filter(q1 & q2) 
       
        if(Profile.objects.filter(user_id=request.user.id).exists()):
           
          if cart_items.count() > 0:  
            messages.error(request, "Product is already in the cart")  
            return redirect("/")  
          else:  
            customer = User.objects.get(id=request.user.id)  
            product = Product.objects.get(id=product_id)  
            created_Cart = Cart.objects.create(quantity=1, customer_id=customer, product_id=product)  
            created_Cart.save()  
            messages.success(request, "Product added to the cart")  
            return redirect("/")  
          
        else:
           messages.error(request, "Plz add the profile addresss")  
           return redirect('/profile')
    else:  
        return redirect("/login")
    
    

def view_cart(request):
   data={}
   cart_items=Cart.objects.filter(customer_id=request.user.id)
   # print(cart_items)
 
   quantitiy=0
   total_price=0
   if cart_items.count() > 0:  
     for item in cart_items:
      quantitiy+=item.quantity
      # print(quantitiy)
      total_price+=(item.quantity*item.product_id.food_price)
      # print(total_price)
   else:
       messages.error(request, "plz add the food item")  
       return redirect("/")

   data['total_price'] =total_price
   data["quantity"]=quantitiy
   data['cart_count']=cart_items.count()
   data['categories']=Category.objects.all() 
   data['cart_items']=cart_items
  
   return render(request,'customer/cart.html',context=data)


def delete_cart(request,cart_id):
   cart_item=Cart.objects.get(id=cart_id)
   
   cart_item.delete()
   return redirect('/cart')


def update_cart(request,flag,cart_id):
    # Retrieve the Cart item by its ID from the Cart model and store it in 'cart_items'
   cart_items=Cart.objects.filter(id=cart_id)
    # Get the current quantity of the first item in the filtered Cart items list
   actual_qunatity=cart_items[0].quantity
     # Check if the flag is 'inc' (indicating increment operation)
   print("actual_qunatity", actual_qunatity)
  
   if(flag=='inc'):
      # Increment the quantity of the cart item by 1
      cart_items.update(quantity=actual_qunatity+1)
   else:
      if(actual_qunatity==1):
         pass
      else:
         cart_items.update(quantity=actual_qunatity-1)
   return redirect("/cart")



def filterByCategory(request,categoryId):
   data={}
   global products
   global filtered_products
   filtered_products = products.filter(category_id=categoryId)
   data['products'] = filtered_products
   data['categories'] = Category.objects.all()
   
   cart_count= Cart.objects.filter(customer_id=request.user.id).count()
   data["cart_count"]=cart_count
   return render(request,'customer/base.html',context=data)

def sortByPrice(request, flag):
    data = {}
    global products
    global filtered_products
    
    if flag == "high-to-low":
        sorted_products = filtered_products.order_by("-food_price")
        
    else:
        sorted_products = filtered_products.order_by("food_price")
    
    data['products'] = sorted_products
    data['categories'] = Category.objects.all()
    
    return render(request, 'customer/base.html', context=data)



def filterByPriceRange(request):
    data = {}
    global products
    global filtered_products
    if request.method == "POST":
        min = request.POST.get("min")
        max = request.POST.get("max")
        q1 = Q(food_price__gte=min)
        q2 = Q(food_price__lte=max)
        filtered_by_price_range = filtered_products.filter(q1 & q2)
        data['products'] = filtered_by_price_range
        data['categories'] = Category.objects.all()
        return render(request, 'customer/base.html', context=data)
    return redirect("/")

def searchByName(request):
    data = {}
    global filtered_products
    
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        print(product_name)

        # Ensure filtered_products is defined somewhere in your code
        searched_products = filtered_products.filter(food_name__icontains=product_name)
        data['products'] = searched_products
        data['categories'] = Category.objects.all()
        
        return render(request, 'customer/base.html', context=data)
    
    return redirect("/")



def updateProfile(request):
    data = {}
    user = User.objects.filter(id=request.user.id)
    if(request.method == "POST"):
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        
        # Updating firstname, lastname and email into User model i.e auth_user
        user.update(first_name=firstname, last_name=lastname, email=email)
        
        if(Profile.objects.filter(user_id=request.user.id).exists()):
            existing_profile = Profile.objects.filter(user_id=request.user.id)
            existing_profile.update(contact=contact, street=street, city=city, state=state, pincode=pincode)
        else:
            user_object = User.objects.get(id=request.user.id)
            new_profile = Profile.objects.create(contact=contact, street=street, city=city, state=state, pincode=pincode, user_id=user_object)
            new_profile.save()
        
        return redirect("/profile")
    
    cart_count = Cart.objects.filter(customer_id=request.user.id).count()
    data['cart_count'] = cart_count
    userx = User.objects.get(id=request.user.id)
    profilex = Profile.objects.filter(user_id=userx)
    
    if(not userx.first_name and profilex.count() == 0):
        print("data does not exist")
    else:
        data['user'] = userx
        data['address'] = profilex[0]
    
    return render(request, 'customer/profile.html', context=data)


from .models import Address, Profile, Reservation

def add_address(request):
    if request.method == 'POST':
        # Get the address details from the POST request
        full_address = request.POST.get('full_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')

        # Get the user's profile (ensure the user is logged in)
        profile = Profile.objects.get(user_id=request.user.id)

        # Create a new address associated with the user's profile
        new_address = Address(
            profile=profile,
            full_address=full_address,
            city=city,
            state=state,
            pincode=pincode,
            contact=contact
        )
        new_address.save()

        # Redirect after saving (change 'checkout_page' to your actual redirect URL)
        return redirect('/checkout')
        client = razorpay.Client(auth=("rzp_test_93atKPgF1eLJ4M", "ZighzyBxP2GddO81jA8fXqCy"))

    
      
    # If GET, render the form for adding an address
    return render(request, 'customer/add_address.html')


def order_summary(request):
    # Initialize data dictionary
    data = {}
    
    # Get cart items for the current user
    cart_items = Cart.objects.filter(customer_id=request.user.id)
    
    # Initialize quantities and total price
    quantity = 0
    total_price = 0
    
    # Calculate total quantity and price
    for item in cart_items:
        quantity += item.quantity
        total_price += (item.quantity * item.product_id.food_price)
    
    # Add cart details to the context
    data['quantity'] = quantity
    data['total_price'] = total_price
    data['cart_count'] = cart_items.count()
    data['cart_items'] = cart_items
    
    # Add user details to the context
    data['user'] = request.user

    # Add address details to the context
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        data['address'] = profile
    except Profile.DoesNotExist:
        data['address'] = None
    
   
    # Render the template with context data
    return render(request, 'customer/ordersumary.html', data)

def checkout(request):
    cart_items = Cart.objects.filter(customer_id=request.user.id)
    
    # Retrieve the user's profile
    profile = Profile.objects.get(user_id=request.user.id)
    address=Address.objects.filter(profile=profile)

    quantity = 0
    total_price = 0
    order_image = None  # Initialize a variable for the order image

    for item in cart_items:
        quantity += item.quantity
        total_price += (item.quantity * item.product_id.food_price)
        
        # Get the image from the first item or any logic you prefer
        if order_image is None:
            order_image = item.product_id.image

    order_id = None

    # If cart has items, create an order
    
    order = Order.objects.create(
            customer=request.user,
            total_price=total_price,
            delivery_status='Order Placed',  # Corrected the spelling here
              # Use the selected image for the order
        )
       
    order_id = order.id

        # Create order items based on the cart items
    for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,  # Use the order instance instead of order_id
                product=cart_item.product_id,
                price=cart_item.product_id.food_price,
                quantity=cart_item.quantity,
                pimage=order_image,
            )
      
        # Clear the cart after creating the order
       

    # Prepare the data to render the checkout page
    data = {
        'quantity': quantity,
        'total_price': total_price,
        'cart_count': Cart.objects.filter(customer_id=request.user.id).count(),  # Update cart count after deletion
        'cart_items': cart_items,
        'user': request.user,
        'profile': profile,
        'order_id': order_id, 
        'address':address # Pass the order ID to the template
    }

    return render(request, 'customer/checkout.html', context=data)


def paymentdone(request):

    return redirect("/")


# def order_confirmation(request, order_id):
#     data = {}

#     order = Order.objects.get(id=order_id, customer=request.user.id)
#     order_items = OrderItem.objects.filter(order=order)
#     # Fetch the cart items for the current user
#     cart_items = Cart.objects.filter(customer_id=request.user.id)

#     # If there are cart items, delete them
#     if cart_items.exists():
#         cart_items.delete()

#     # Prepare the data for rendering the order confirmation page
#     data = {
#         'order': order,
#         'cart_count': Cart.objects.filter(customer_id=request.user.id).count(), 
#         'order_items': order_items, # This will now be zero after deletion
#     }

#     return render(request, 'customer/order_confirmation.html', context=data)

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def order_confirmation(request, order_id):
    # Get the order and associated items
    order = Order.objects.get(id=order_id, customer=request.user.id)
    order_items = OrderItem.objects.filter(order=order)

    # Fetch the cart items for the current user and delete them
    cart_items = Cart.objects.filter(customer_id=request.user.id)
    if cart_items.exists():
        cart_items.delete()

    # Prepare the data for rendering the order confirmation page
    data = {
        'order': order,
        'cart_count': Cart.objects.filter(customer_id=request.user.id).count(),
        'order_items': order_items,  # This will now be zero after deletion
    }

    # Prepare the email details
    subject = f"Order Confirmation - Order #{order.id}"  # Use order.id here, not order_id.id
    message = f"Dear {request.user.username},\n\nYour order #{order.id} has been confirmed. Thank you for shopping with us!"
    
    # HTML version of the email (optional, for a more styled email)
    html_message = render_to_string('customer/order_confirmation_email.html', {'order': order, 'order_items': order_items})

    # Send the email to the customer
    send_mail(
        subject,
        message,  # Plain text message (fallback if HTML email is not supported)
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],  # Send to the customer's email
        html_message=html_message,  # Optional: use HTML message
    )

    # Render the confirmation page
    return render(request, 'customer/order_confirmation.html', context=data)



def order_history(request):
    # Fetch all orders for the current user, sorted by creation date
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
     
  
    # Check if a sorting parameter is provided in the request
    sort_by = request.GET.get('sort', 'created_at')  # Default to sorting by creation date
    if sort_by == 'total_price':
        orders = orders.order_by('-total_price')  # Sort by total price descending
    else:
        orders = orders.order_by('-created_at')  # Sort by creation date descending
    
    # Pass the orders to the template
    context = {
        'orders': orders,
        'sort_by': sort_by,  # Include the current sort parameter in context
    }

    return render(request, 'customer/orderhistory.html', context)

def order_detail(request, order_id):
    # Fetch the order based on the provided order ID and the current user
    order = Order.objects.get(id=order_id, customer=request.user)
    
    # Fetch all items related to this order
    order_items = OrderItem.objects.filter(order=order)

    # Prepare context data
    data = {
        'order': order,
        'order_items': order_items,  # Pass ordered items including product details
        'order_status': order.delivery_status,  # Include the order status
    }

    return render(request, 'customer/orderdetails.html', context=data)

from django.shortcuts import render, get_object_or_404
from .models import Order
def orderstatus(request):
    order = None
    order_status = ''
    
    if request.method == 'POST':
        # Print all POST data to debug if form is submitting correctly
        print(f"POST Data: {request.POST}")
        
        order_id = request.POST.get('order_id')
        
        # Print the order_id for debugging
        print(f"Order ID: {order_id}")
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id,customer=request.user)
                # Print more useful details about the order for debugging
             
                if order==request.user:
                  print(f"Order found: ID {order.order_id}, Total Price {order.total_price}, Status {order.delivery_status}")

                order_status = 'Order found!'
               
            except Order.DoesNotExist:
                print("Order not found")
                order_status = 'Order not found. Please check your order ID.'
        else:
            print("No Order ID provided")
            order_status = 'Please enter a valid order ID.'

    context = {
        'order': order,
        'order_status': order_status,
    }
    return render(request,'customer/orderstatus.html', context)







