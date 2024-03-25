from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import *
from Post.models import *


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        data['refresh'] = attrs['refresh']
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = User.objects.get(username=self.user.username)
        # data['status'] = user.status
        data['id'] = user.id
        data['gender'] = user.gender
        return data


class UserSer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'photo', 'phone',
                  'gender', 'is_direktor', 'is_tekshiruvchi', 'is_bulim', 'is_xodim')
        # read_only_fields = ['is_xodim']

    def create(self, validated_data):
        user = super().create(self.validated_data)
        user.set_password(validated_data.pop('password', None))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.status = validated_data.get('status', instance.status)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.is_tekshiruvchi = validated_data.get('is_tekshiruvchi', instance.is_tekshiruvchi)
        instance.is_bulim = validated_data.get('is_bulim', instance.is_bulim)
        instance.is_xodim = validated_data.get('is_xodim', instance.is_xodim)
        instance.is_direktor = validated_data.get('is_direktor', instance.is_direktor)
        instance.save()
        return instance
    
    def validate_username(self, value):
        value = value.lower()
        return value


class XodimSer(serializers.ModelSerializer):
    class Meta:
        model = Xodim
        fields = ('id', 'user', 'ish_turi', 'bulimi')
    
    def update(self, instance, validated_data):
        instance.bulimi = validated_data.get('bulimi', instance.bulimi)
        # instance.ish_turi = validated_data.get('ish_turi', instance.ish_turi)
        instance.save()
        return instance