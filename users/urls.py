from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('email_activate/<uidb64>/<token>/', ActivateEmailView.as_view(), name='activate_email'),
    path('email_success/', ActivateEmailSuccessView.as_view(), name='email_success'),
    path('email_error/', ActivateEmailErrorView.as_view(), name='email_error'),
    path('email_send/', ActivateEmailSendView.as_view(), name='email_send'),
    path('detail/<pk>/', UserDetailView.as_view(), name='user_detail'),
]