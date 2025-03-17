from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import random
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import SMSSerializer, VerifySmsSerializer
from django.conf import settings
User = get_user_model()
SMS_KEY = settings.SMS_KEY

class SmsLoginViewSet(viewsets.ModelViewSet):
    def send_sms(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = str(random.randint(100000, 999999))
            url= 'https://43vvd1.api.infobip.com/sms/2/text/advanced'
            headers = {
                'Authorization': SMS_KEY,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            payload = {
                'messages': [
                    {
                        'from': 'Abror433',
                        'destinations': [
                            {
                                'to': phone_number,
                            }
                        ],
                        'text': f'Your verification code is {verification_code}',
                    }
                ]
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == status.HTTP_200_OK:
                cache.set(phone_number, verification_code, 300)
                return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Failed to send SMS"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def verify_sms(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = cache.get(phone_number)
            if verification_code==cached_code:
                user, created= User.objects.get_or_create(phone_number=phone_number)
                if created:
                    user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh_token),
                    'access': str(refresh_token.access_token),
                })
            return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)