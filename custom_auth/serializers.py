from rest_framework import serializers

class SMSSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
class VerifySmsSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    verfication_code = serializers.CharField()