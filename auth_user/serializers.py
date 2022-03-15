from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'birth_date', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField()
    email = serializers.EmailField()

    def validate_birth_date(self, date):
        if date > datetime.today().date() - relativedelta(years=9):
            raise serializers.ValidationError("You must be above 9 years age.")
        return date

    def validate_email(self, email):
        if 'rambler' in email.split('@')[1]:
            raise serializers.ValidationError("Sorry. No register within 'rambler' host.")
        return email

    class Meta:
        model = User
        fields = ['username', 'password', 'birth_date', 'email', 'first_name', 'last_name']
        # fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
