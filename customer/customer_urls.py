from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from customer import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home),
    path('register/',views.user_register),
    path('login/',views.user_login),
    path('logout/',views.user_logout),
    path('make-reservation/', views.make_reservation),
    path('add-to-cart/<product_id>',views.add_to_cart),
    path('cart/', views.view_cart),
    path('cart/delete/<cart_id>', views.delete_cart),
    path('cart/<flag>/<cart_id>', views.update_cart),
    path('category/<categoryId>',views.filterByCategory),
    path('sort-by/<flag>', views.sortByPrice),
    path('price-range/', views.filterByPriceRange),
    path('add_address/', views.add_address, name='add_address'),
    path('search-by-name/', views.searchByName),      
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='customer/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='customer/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='customer/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='customer/password_reset_complete.html'), 
         name='password_reset_complete'),


     
    path('order-summary/', views.order_summary),
    path('profile/',views.updateProfile),
    path('checkout/',views.checkout),  

    path('order-confirmation/<order_id>', views.order_confirmation),     
    path('order-history/', views.order_history),  
    path('order_detail/<order_id>', views.order_detail),  
    path('order-status/', views.orderstatus),
   



]
