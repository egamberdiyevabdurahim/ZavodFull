from django.shortcuts import render
from django.db.models import Q, F, Count, Sum, Min, Max

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.parsers import MultiPartParser, JSONParser

from User.serializers import XodimSer

from .serializers import (PhotoSer, Ish_TuriSer, BulimSer, MahsulotSer,
                          XatolarSer, MissedSer, MissedGetSer)
from .models import *
from User.models import *


from datetime import datetime, timedelta
from django.utils import timezone

from Post import serializers            


# class XodimStatistic(APIView):
#     parser_classes = [JSONParser, MultiPartParser]

#     def get(self, request):
#         xozir = timezone.now()
        
#         bir_yil_oldin = xozir - timedelta(days=365)
#         olti_oy_oldin = xozir - timedelta(days=30*6)
#         bir_oy_oldin = xozir - timedelta(days=30)
#         bir_xafta_oldin = xozir - timedelta(days=7)
#         bir_kun_oldin = xozir - timedelta(days=1)

#         statistics = []

#         def statistika(start_date, end_date):
#             xodimlar = Xodim.objects.all()
#             data = []
#             for x in xodimlar:
#                 missed = Missed.objects.filter(xodim=x, created_at__range=[start_date, end_date])
#                 total_ish_vaqti = 0
#                 total_xato_soni = 0
#                 total_butun_soni = 0
#                 for hisobot in missed:
#                     total_ish_vaqti += hisobot.ish_vaqti
#                     total_xato_soni += hisobot.xato_soni
#                     total_butun_soni += hisobot.butun_soni
#                 data.append({
#                     'ism': x.first_name,
#                     'ish_vaqti': total_ish_vaqti,
#                     'xato_soni': total_xato_soni,
#                     'butun_soni': total_butun_soni
#                 })
#             return data

#         # Calculate statistics for different time periods and append to the statistics list
#         statistics.append({'period': '1 year', 'data': statistika(bir_yil_oldin, xozir)})
#         statistics.append({'period': '6 months', 'data': statistika(olti_oy_oldin, xozir)})
#         statistics.append({'period': '1 month', 'data': statistika(bir_oy_oldin, xozir)})
#         statistics.append({'period': '1 week', 'data': statistika(bir_xafta_oldin, xozir)})
#         statistics.append({'period': '1 day', 'data': statistika(bir_kun_oldin, xozir)})

#         return Response(statistics)


class PhotoEditView(APIView):
    def get(self, request, id):
        photo = Photo.objects.get(id=id)
        ser = PhotoSer(photo)
        return Response(ser.data)

    def patch(self, request, id):
        photo = Photo.objects.get(id=id)
        rasm = request.data.get('photo')
        photo.photo = rasm
        photo.save()
        return Response({'message': 'successfully'})
    
    def delete(self, request, id):
        photo = Photo.objects.get(id=id)
        photo.delete()
        return Response({'message': 'deleted successfully'})


class PhotoList(ListCreateAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Photo.objects.all()
    serializer_class = PhotoSer


class IshTuriList(ListCreateAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Ish_Turi.objects.all()
    serializer_class = Ish_TuriSer


class Ish_TuriDetail(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Ish_Turi.objects.all()
    serializer_class = Ish_TuriSer


class XatolarList(ListCreateAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Xatolar.objects.all()
    serializer_class = XatolarSer


class XatolarDetail(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Xatolar.objects.all()
    serializer_class = XatolarSer


# class MissedList(ListCreateAPIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     queryset = Missed.objects.all()
#     serializer_class = MissedSer


# class MissedDetail(RetrieveUpdateDestroyAPIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     queryset = Missed.objects.all()
#     serializer_class = MissedSer


# class PhotoList(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request):
#         photos = Photo.objects.all()
#         ser = PhotoSer(photos, many=True)
#         return Response(ser.data)
    
#     def post(self, request):
#         ser = PhotoSer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=201)
#         return Response(ser.errors, status=400)


# class IshTuriList(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request):
#         ishturi = Ish_Turi.objects.all()
#         ser = Ish_TuriSer(ishturi, many=True)
#         return Response(ser.data)
    
#     def post(self, request):
#         ser = Ish_TuriSer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=201)
#         return Response(ser.errors, status=400)


# class Ish_TuriDetail(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request, id):
#         ishturi = Ish_Turi.objects.get(id=id)
#         ser = Ish_TuriSer(ishturi)
#         return Response(ser.data)
    
#     def patch(self, request, id):
#         ishturi = Ish_Turi.objects.get(id=id)
#         ser = Ish_TuriSer(ishturi, data=request.data, partial=True)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=201)
#         return Response(ser.errors, status=400)
    
#     def delete(self, request, id):
#         ishturi = Ish_Turi.objects.get(id=id)
#         ishturi.delete()
#         return Response(status=204)


class BulimList(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request):
        """
        name : string
        bulim_id : string (unique)
        user : id
        """
        bulim = Bulim.objects.all()
        ser = BulimSer(bulim, many=True)
        return Response(ser.data)
    
    def post(self, request):
        """
        name : string
        bulim_id : string (unique)
        user : id
        """
        ser = BulimSer(data=request.data)
        if ser.is_valid():
            userr = ser.validated_data.get('user')
            if userr.is_bulim==True:
                ser.save()
                return Response(ser.data, status=201)
            return Response({'message': 'Bu User Bulimga Boshliq Bo\'lolmaydi Chunki Bu User Bulim Uchun Emas!'})
        return Response(ser.errors, status=400)


class BulimDetail(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request, id):
        # try:
            bulim = Bulim.objects.get(id=id)
            xod = Xodim.objects.filter(bulimi = bulim)
            ser = BulimSer(bulim)
            xodim = XodimSer(xod, many=True)
            a = {}
            if Missed.objects.filter(xodim__bulimi=bulim):
                missed = Missed.objects.filter(xodim__bulimi=bulim)
                sum_xato = missed.aggregate(soni=Sum('xato_soni'))
                sum_butun = missed.aggregate(soni=Sum('butun_soni'))
                total_mistakes = sum_xato['soni'] + sum_butun['soni']
                xato_foizi = round((sum_xato['soni'] * 100) / (total_mistakes) if total_mistakes else 0, 2)
                butun_foizi = round((sum_butun['soni'] * 100) / (total_mistakes) if total_mistakes else 0, 2)
                a[str('bulim_name')]=str(bulim.name)
                a[str('bulim_id')]=str(bulim.bulim_id)
                a[str('bulim_boshliq')]=str(bulim.user.first_name)
                a[str('xato_soni')]=sum_xato
                a[str('butun_soni')]=sum_butun
                a[str('Xato_foizi')]=xato_foizi
                a[str('Butun_foizi')]=butun_foizi
                a[str('hisobot_soni')]=len(missed)
                b = missed.aggregate(Count('xodim'))
                a[str('xodim_soni')]=b
                c = []
                for j in missed:
                    found = False
                    for item in c:
                        if item['mahsulot_name'] == j.mahsulot.name:
                            item['mahsulot_id'] = j.mahsulot.mahsulot_id
                            item['xato_soni'] += j.xato_soni
                            item['butun_soni'] += j.butun_soni
                            found = True
                            break
                    if not found:
                        c.append({'mahsulot_name': j.mahsulot.name, 'mahsulot_id': j.mahsulot.mahsulot_id, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni})
                for i in missed:
                    for item in c:
                        if item['mahsulot_name'] == i.mahsulot.name:
                            item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                            item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
                d = []
                for j in missed:
                    found = False
                    for item in d:
                        if item['xato_name'] == j.xato.name:
                            item['xato_id'] = j.xato.xato_id
                            item['mahsulot_name'] = j.mahsulot.name
                            item['xato_soni'] += j.xato_soni
                            found = True
                            break
                    if not found:
                        d.append({'xato_name': j.xato.name, 'xato_id': j.xato.xato_id, 'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni})
                now = timezone.now()

                one_year_ago = now - timedelta(days=365)
                six_months_ago = now - timedelta(days=30*6)
                three_months_ago = now - timedelta(days=30*3)
                one_month_ago = now - timedelta(days=30)
                one_week_ago = now - timedelta(days=7)
                one_day_ago = now - timedelta(days=1)

                statistics = []

                def calculate_statistics(start_date, end_date):
                    data = []
                    bulim = Bulim.objects.get(id=id)
                    hisobots = Missed.objects.filter(xodim__bulimi=bulim, created_at__range=[start_date, end_date])
                    total_xato_soni = 0
                    total_butun_soni = 0
                    total_mistakes = 0
                    xato_foizi = 0
                    butun_foizi = 0
                    for hisobot in hisobots:
                        total_xato_soni += hisobot.xato_soni
                        total_butun_soni += hisobot.butun_soni
                        total_mistakes = total_xato_soni + total_butun_soni
                        xato_foizi = round((total_xato_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                        butun_foizi = round((total_butun_soni * 100) / (total_mistakes) if total_mistakes else 0, 2)
                    data.append({
                        'bulim_name': bulim.name,
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

                return Response({'data':ser.data,
                             'statistic':a,
                             'mahsulot':c,
                             'xato': d,
                             'xodimlar':xodim.data,
                             'time_statistic':statistics,
                             })
            return Response({'data':ser.data,
                             'statistic':None,
                             'mahsulot':None,
                             'xato': None,
                             'xodimlar':None,
                             'time_statistic':None,
                             })
        # except:
        #     return Response({'message': "bu id xato"})
    
    def patch(self, request, id):
        bulim = Bulim.objects.get(id=id)
        ser = BulimSer(bulim, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)
    
    def delete(self, request, id):
        user = request.user
        bulim = Bulim.objects.get(id=id)
        if request.user.is_admin==True or request.user.is_direktor==True:
            bulim.delete()
            return Response(status=204)
        return Response({'message':'Bulimni Siz Uchirolmaysiz, Uchirish Uchun Direktor Yoki Adminga Murojat Qiling'})


class MahsulotList(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request):
        maxsulot = Mahsulot.objects.all()
        ser = MahsulotSer(maxsulot, many=True)
        l=[]
        for i in maxsulot:
            h = Missed.objects.filter(mahsulot=i)
            for j in h:
                found = False
                for item in l:
                    if item['mahsulot_name'] == j.mahsulot.name:
                        item['xato_soni'] += j.xato_soni
                        item['butun_soni'] += j.butun_soni
                        found = True
                        break
                if not found:
                    l.append({'id':j.mahsulot.id, 'mahsulot_id':j.mahsulot.mahsulot_id, 'mahsulot_name': j.mahsulot.name, 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni, 'Xato_foizi': None, 'Butun_foizi': None})
            for i in h:
                for item in l:
                    if item['mahsulot_name'] == i.mahsulot.name:
                        item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                        item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 

        return Response({'data':ser.data,
                         'statistic': l})
    
    def post(self, request):
        ser = MahsulotSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)


class MahsulotDetail(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request, id):
        try:
            mahsulot = Mahsulot.objects.get(id=id)
            ser = MahsulotSer(mahsulot)
            a = []
            if Missed.objects.filter(mahsulot=mahsulot):
                missed = Missed.objects.filter(mahsulot=mahsulot)
                for j in missed:
                    found = False
                    for item in a:
                        if item['xato_name'] == j.xato.name:
                            item['xato_soni'] += j.xato_soni
                            item['butun_soni'] += j.butun_soni
                            found = True
                            break
                    if not found:
                        a.append({'xato_name': j.xato.name , 'xato_soni': j.xato_soni, 'butun_soni': j.butun_soni})
                for i in missed:
                    for item in a:
                        if item['xato_name'] == i.xato.name:
                            item['Xato_foizi'] = round(item['xato_soni']*100/(item['xato_soni'] + item['butun_soni']), 2)
                            item['Butun_foizi'] = round(item['butun_soni']*100/(item['xato_soni'] + item['butun_soni']), 2) 
                return Response({'data':ser.data,
                                 'statistic':a})
            return Response({'data':ser.data,
                                 'statistic':None})
        except:
            return Response({'message': "bu id xato"})
    
    def patch(self, request, id):
        mahsulot = Mahsulot.objects.get(id=id)
        ser = MahsulotSer(mahsulot, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)
    
    def delete(self, request, id):
        mahsulot = Mahsulot.objects.get(id=id)
        if request.user.is_admin==True or request.user.is_direktor==True:
            mahsulot.delete()
            return Response(status=204)
        return Response({'message':'Mahsulotni Siz Uchirolmaysiz, Uchirish Uchun Direktor Yoki Adminga Murojat Qiling'})


# class XatolarList(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request):
#         xatolar = Xatolar.objects.all()
#         ser = XatolarSer(xatolar, many=True)
#         return Response(ser.data)
    
#     def post(self, request):
#         ser = XatolarSer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=201)
#         return Response(ser.errors, status=400)


# class XatolarDetail(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request, id):
#         xatolar = Xatolar.objects.get(id=id)
#         ser = XatolarSer(xatolar)
#         return Response(ser.data)
    
#     def patch(self, request, id):
#         xatolar = Xatolar.objects.get(id=id)
#         ser = XatolarSer(xatolar, data=request.data, partial=True)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=201)
#         return Response(ser.errors, status=400)
    
#     def delete(self, request, id):
#         xatolar = Xatolar.objects.get(id=id)
#         xatolar.delete()
#         return Response(status=204)


class MissedList(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        missed = Missed.objects.all()
        ser = MissedGetSer(missed, many=True)
        return Response(ser.data)
    
    def post(self, request):
        data = request.data
        data['user']=request.user.id
        ser = MissedSer(data=data)
        if ser.is_valid() and request.user.is_tekshiruvchi==True or request.user.is_admin==True or request.user.is_direktor==True:
            if request.data.get('photo'):
                news = ser.save()
                photo_list = request.data.getlist('photo', [])
                for x in photo_list:
                    p = Photo.objects.create(photo=x)
                    news.photo.add(p)
                    return Response(ser.data, status=201)
            else:
                ser.save()
                return Response(ser.data, status=201)
        return Response(ser.errors, status=400)


class MissedDetail(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated,]
    def get(self, request, id):
        try:
            missed = Missed.objects.get(id=id)
            ser = MissedSer(missed)
            return Response(ser.data)
        except Missed.DoesNotExist:
            return Response({'message': '  not found'})
    
    def patch(self, request, id):
        photo_list = request.data.getlist('photo')
        missed = Missed.objects.get(id=id)
        ser = MissedSer(missed, data=request.data, partial=True)
        if ser.is_valid() and request.user.is_tekshiruvchi==True or request.user.is_admin==True or request.user.is_direktor==True:
            news = ser.save()
            if photo_list:
                for x in photo_list:
                    p = Photo.objects.create(photo=x)
                    news.photo.add(p)
            return Response(ser.data, status=201)
        return Response({'error':ser.errors,
                         'message':'Hisobotni tahrirlolmaysiz Tahrirlash uchun Tekshiruvchi, Admin yoki Direktorga Murojat Qiling!'}, status=400)
    
    def delete(self, request, id):
        missed = Missed.objects.get(id=id)
        if request.user.is_tekshiruvchi==True or request.user.is_admin==True or request.user.is_direktor==True:
            missed.delete()
            return Response({'message': 'Hisobot Uchirildi!'})
        return Response({'message': 'Hisobotni uchirolmaysiz Uchirish uchun Tekshiruvchi, Admin yoki Direktorga Murojat Qiling!'})

