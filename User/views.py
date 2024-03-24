from genericpath import exists
from django.shortcuts import render
from django.db.models import Q, F, Sum, Min, Max
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from Post.models import *
from .serializers import UserSer, XodimSer, ChangePasswordSerializer, ForgotPasswordSerializer


class ForgotPasswordView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if request.user.is_authenticated and request.user.status == 'Admin':
            if serializer.is_valid():
                username = serializer.data.get("username")
                new_password = serializer.data.get("new_password")
                user = get_user_model().objects.filter(username=username).first()
                if user:
                    user.set_password(new_password)
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                    "detail": "Password updated successfully",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
                return Response({'message': 'User topilmadi'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Siz admin emassiz yoki ro\'yxatdan o\'tmagansiz'})



class ChangePasswordView(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'})

            user.set_password(new_password)
            user.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({'detail': 'Password changed successfully.',
                             'access_token': access,
                             'refresh_token': str(refresh)
                             })

        return Response(serializer.errors)


class Userdetail(APIView):
    # permission_classes = [IsAuthenticated,] 
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            ser = UserSer(user)
            return Response(ser.data)
        except:
            return Response({'message': 'bu id xato'})
    
    def patch(self, request, id):
        user = User.objects.filter(id=id).first()
        if Xodim.objects.filter(user=user).first():
            xodim = Xodim.objects.filter(user=user).first()
            ser = UserSer(data=request.data, instance=user, partial=True)
            if ser.is_valid():
                ser.save()
                if user.is_xodim==False:
                    xodim.delete()
                    ser.save()
                    return Response(ser.data)
                ser.save()
                return Response(ser.data)
        ser = UserSer(data=request.data, instance=user, partial=True)
        if ser.is_valid():
            ser.save()
            if user.is_direktor==False and user.is_tekshiruvchi==False and user.is_bulim==False:
                user.is_xodim = True
                user.save()
                Xodim.objects.create(user=user)
                return Response(ser.data)
            if user.is_xodim==True:
                Xodim.objects.create(user=user)
                ser.save()
                return Response(ser.data)
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user.is_admin==True or user.is_direktor==True:
            user.delete()
            return Response(status=204)
        if user.is_admin==True:
            return Response({'message': 'Siz Adminni Uchirolmaysiz Uchirish Uchun Dirketorga Murojat Qiling!'})
        elif user.is_direktor==True:
            return Response({'message': 'Siz Direktorni Uchirolmaysiz Uchirish Uchun Adminga Murojat Qiling!'})
        elif user.is_bulim==True:
            return Response({'message': 'Siz Bulim Boshlig\'ini Uchirolmaysiz Uchirish Uchun Admin yoki Direktorga Murojat Qiling!'})
        elif user.is_tekshiruvchi==True:
            return Response({'message': 'Siz Tekshiruvchini Uchirolmaysiz Uchirish Uchun Admin yoki Direktorga Murojat Qiling!'})
        elif user.is_xodim==True:
            return Response({'message': 'Siz Xodimni Uchirolmaysiz Uchirish Uchun Admin yoki Direktorga Murojat Qiling!'})



# class XodimDetail(RetrieveUpdateDestroyAPIView):
#     parser_classes = [MultiPartParser, JSONParser]
#     queryset = Xodim.objects.all()
#     serializer_class = XodimSer


class SignUp(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        user = User.objects.all()
        ser = UserSer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        data = request.data
        ser = UserSer(data=data)
        if ser.is_valid():
            if ser.validated_data.get('is_direktor') is True or ser.validated_data.get('is_tekshiruvchi') is True or ser.validated_data.get('is_bulim') is True:
                ser.validated_data['is_xodim'] = False
                dirketor = ser.validated_data.get('is_direktor')
                admin = ser.validated_data.get('is_admin')
                if dirketor:
                    if User.objects.filter(is_direktor=dirketor).exists():
                        return Response({'message': f'Bunday Dirketor Tayinlab Bulingan'})
                if admin:
                    if User.objects.filter(is_admin=admin).exists():
                        return Response({'message': f'Bunday Admin Tayinlab Bulingan'})
                ser.save()
                return Response(ser.data)
            if ser.validated_data.get('is_direktor') is not exists and ser.validated_data.get('is_tekshiruvchi') is not exists and ser.validated_data.get('is_bulim') is not exists:
                dirketor = ser.validated_data.get('is_direktor')
                admin = ser.validated_data.get('is_admin')
                if dirketor:
                    if User.objects.filter(is_direktor=dirketor).exists():
                        return Response({'message': f'Bunday Dirketor Tayinlab Bulingan'})
                if admin:
                    if User.objects.filter(is_admin=admin).exists():
                        return Response({'message': f'Bunday Admin Tayinlab Bulingan'})
                ser.save()
                ser.validated_data['is_xodim'] = True
                ser.save()
                user = User.objects.filter(username=ser.validated_data.get('username')).first()
                Xodim.objects.create(user=user)
                return Response(ser.data)
        return Response(ser.errors)


class XodimList(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    def get(self, request):
        xodim = Xodim.objects.all()
        ser = XodimSer(xodim, many=True)
        return Response(ser.data)
    
    def post(self, request):
        ish_list = request.data.getlist('ish_turi', [])
        ser = XodimSer(data=request.data)
        if ser.is_valid():
            news = ser.save()
            for x in ish_list:
                news.ish_turi.add(x)
            return Response(ser.data)
        return Response(ser.errors)


class XodimDetail(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def get(self, request, id):
        try:
            now = timezone.now()

            one_year_ago = now - timedelta(days=365)
            six_months_ago = now - timedelta(days=30*6)
            three_months_ago = now - timedelta(days=30*3)
            one_month_ago = now - timedelta(days=30)
            one_week_ago = now - timedelta(days=7)
            one_day_ago = now - timedelta(days=1)

            statistics = []

            def calculate_statistics(start_date, end_date):
                xodim = Xodim.objects.get(id=id)
                data = []
                hisobots = Missed.objects.filter(xodim=xodim, created_at__range=[start_date, end_date])
                total_ish_vaqti = 0
                total_xato_soni = 0
                total_butun_soni = 0
                total_mistakes = 0
                xato_foizi = 0
                butun_foizi = 0
                for hisobot in hisobots:
                    total_ish_vaqti += hisobot.ish_vaqti
                    total_xato_soni += hisobot.xato_soni
                    total_butun_soni += hisobot.butun_soni
                    total_mistakes = total_xato_soni + total_butun_soni
                    xato_foizi = round((total_xato_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    butun_foizi = round((total_butun_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                data.append({
                    'ism': xodim.user.first_name,
                    'ish_vaqti': total_ish_vaqti,
                    'xato_soni': total_xato_soni,
                    'butun_soni': total_butun_soni,
                    'Xato_foizi': xato_foizi,
                    'Butun_foizi': butun_foizi,
                })
                return data

            statistics.append({'period': '1 year', 'data': calculate_statistics(one_year_ago, now)})
            statistics.append({'period': '6 months', 'data': calculate_statistics(six_months_ago, now)})
            statistics.append({'period': '3 months', 'data': calculate_statistics(three_months_ago, now)})
            statistics.append({'period': '1 month', 'data': calculate_statistics(one_month_ago, now)})
            statistics.append({'period': '1 week', 'data': calculate_statistics(one_week_ago, now)})
            statistics.append({'period': '1 day', 'data': calculate_statistics(one_day_ago, now)})
            
            xodim = Xodim.objects.get(id=id)
            ser = XodimSer(xodim)
            l=[]
            m=[]
            h = Missed.objects.filter(xodim=xodim)
            sum_xato = h.aggregate(soni=Sum('xato_soni'))['soni'] or 0
            sum_butun = h.aggregate(soni=Sum('butun_soni'))['soni'] or 0
            sum_ish_vaqti = h.aggregate(soni=Sum('ish_vaqti'))['soni'] or 0
            total_mistakes = sum_xato + sum_butun
            xato_foizi = round((sum_xato * 100) / (total_mistakes) if total_mistakes else 0, 2)
            butun_foizi = round((sum_butun * 100) / (total_mistakes) if total_mistakes else 0, 2)
            all_statistic = {
                'id': xodim.id,
                'xodimi': xodim.user.first_name,
                'ish_vaqti': sum_ish_vaqti,
                'Jami_xato': sum_xato,
                'Jami_butun': sum_butun,
                'Xato_foizi': xato_foizi,
                'Butun_foizi': butun_foizi
            }
            d={}
            for j in h:
                xodim_mistakes = Missed.objects.filter(xodim=j.xodim, mahsulot=j.mahsulot)
                xodim_mistakes_aggregated = xodim_mistakes.aggregate(total_xato_soni=Sum('xato_soni'))
                d[str(j.mahsulot.name)] = xodim_mistakes_aggregated['total_xato_soni']
            l = []
            for j in h:
                found = False
                for item in l:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    l.append({'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni, 'Xato_foizi': None, 'Butun_foizi': None})
            for i in h:
                for item in l:
                    if item['mahsulot_name'] == i.mahsulot.name:
                        item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                        item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
            return Response({'data':ser.data,
                                    'all_statistic': all_statistic,
                                    'mahsulot_xato_soni':d,
                                    'statistic':l,
                                    'time_statistic':statistics,
                                    })
        except:
            return Response({'message': "bu id xato"})
    
    def patch(self, request, id):
        xodim = Xodim.objects.get(id=id)
        xodimser = Xodim.objects.filter(id=id).first()
        ish_list = request.data.getlist('ish_turi', [])
        ser = XodimSer(data=request.data, instance=xodimser, partial=True)
        if ser.is_valid():
            news = ser.save()
            if request.data.get('ish_turi'):
                xodim.ish_turi.clear()
                for x in ish_list:
                    news.ish_turi.add(x)
            return Response(ser.data)
        return Response(ser.errors)
    
    def delete(self, request, id):
        user = request.user
        xodim = Xodim.objects.filter(id=id).first()
        userr = User.objects.filter(xodim_user=xodim).first() 
        if user.is_admin==True or user.is_direktor==True:
            userr.delete()
            xodim.delete()
            return Response(status=204)
        return Response({'message':'Xodimni Siz Uchirolmaysiz, Uchirish Uchun Direktor Yoki Adminga Murojat Qiling'})
