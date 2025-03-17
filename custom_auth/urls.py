from django.urls import path
from .views import SmsLoginViewSet

urlpatterns = [
    path('send-sms/', SmsLoginViewSet.as_view({'post': 'send_sms'}), name='send_sms'),
    path('verify-sms/', SmsLoginViewSet.as_view({'post': 'verify_sms'}), name='verify_sms'),
]