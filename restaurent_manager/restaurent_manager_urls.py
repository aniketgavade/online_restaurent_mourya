from django.contrib import admin
from django.urls import include, path

from restaurent_manager import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.dashboard),
    path('view-orders',views.orders_view, name='orders_view'),
    path('categories/',views. add_category),
    path('categories/delete/<category_id>/', views.delete_category),
    path('categories/add-product/<category_id>/', views.add_product),
    path('categories/view-product/', views.view_product),
    path('products/delete/<product_id>', views.delete_product),
    path('products/update-product/<product_id>/', views.update_product),
    path('admin/orders/', views.admin_order_list),
    path('order/<int:order_id>/',views.order_detail),
    path('order/<int:order_id>/update-status/', views.update_order_status),
    path('customers/', views.customer_list_view),
    path('reservations/', views.reservation_list_view), 
   
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)