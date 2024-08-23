from django.urls import path
from packngoapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import booking_view
from .views import order_history
from .views import booking_confirmation
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.user_register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('book/',views.book),
    path('booking_view/<int:booking_id>/', booking_view, name='booking_view'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('forgot_password', views.forgot_password),
    path('otp_verification', views.otp_verification),
    path('new_password', views.new_password),       
    
    # path('book/', booking_view, name='book'),
    path('read_book',views.read_book),
    path('order_history/',order_history, name='order_history')
     
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)