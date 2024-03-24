from rest_framework import serializers

from .models import *
from User.serializers import *


class PhotoSer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class Ish_TuriSer(serializers.ModelSerializer):
    class Meta:
        model = Ish_Turi
        fields = '__all__'


class BulimSer(serializers.ModelSerializer):
    class Meta:
        model = Bulim
        fields = '__all__'


class MahsulotSer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot
        fields = '__all__'


class XatolarSer(serializers.ModelSerializer):
    class Meta:
        model = Xatolar
        fields = '__all__'


class MissedSer(serializers.ModelSerializer):
    # photo = PhotoSer(many=True)
    class Meta:
        model = Missed
        fields = ('id', 'xodim', 'user', 'xato', 'xato_soni', 'butun_soni', 'mahsulot', 'created_at', 'updated_at', 'photo', 'izoh', 'ish_vaqti', 'audio')
        read_only_fields = ['photo']

    def update(self, instance, validated_data):
        instance.xodim = validated_data.get('xodim', instance.xodim)
        instance.xato = validated_data.get('xato', instance.xato)
        instance.xato_soni = validated_data.get('xato_soni', instance.xato_soni)
        instance.butun_soni = validated_data.get('butun_soni', instance.butun_soni)
        instance.mahsulot = validated_data.get('mahsulot', instance.mahsulot)
        # instance.photo = validated_data.get('photo', instance.photo)
        instance.izoh = validated_data.get('izoh', instance.izoh)
        instance.ish_vaqti = validated_data.get('ish_vaqti', instance.ish_vaqti)
        instance.audio = validated_data.get('audio', instance.audio)
        a = validated_data.get('photo',None)
        if a:
            for x in a:
                new_photo = Photo.objects.create(photo=x)
                instance.photo.add(new_photo)
            
        # instance.photo.remove(validated_data.get('photo', instance.photo))
        # news = instance.save()
        # for track_data in instance.photo:
        #     p = Photo.objects.create(photo=track_data, **track_data)
        #     news.photo.add(p)
        instance.save()
        return instance


class MissedGetSer(serializers.ModelSerializer):
    xodim = XodimSer()
    user = UserSer()
    xato = XatolarSer()
    mahsulot = MahsulotSer()
    photo = PhotoSer(many=True)
    class Meta:
        model = Missed
        fields = ('id', 'xodim', 'user', 'xato', 'xato_soni', 'butun_soni', 'mahsulot', 'created_at', 'updated_at', 'photo', 'izoh', 'ish_vaqti', 'audio')
