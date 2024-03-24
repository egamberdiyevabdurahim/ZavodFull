from django.urls import path

from .views import (PhotoList, PhotoEditView, IshTuriList, Ish_TuriDetail, BulimList, BulimDetail,
                    MahsulotList, MahsulotDetail, XatolarList, XatolarDetail,
                    MissedList, MissedDetail)


urlpatterns = [
    # path('maxsulot/', Maxsulot.as_view(), name='maxsulot'),
    # path('statistic/', XodimStatistic.as_view(), name='statistic'),
    path('photo/', PhotoList.as_view(), name='photo'),
    path('photoedit/<int:id>/', PhotoEditView.as_view(), name='photo_edit'),
    path('ish_turi/', IshTuriList.as_view(), name='ish_turi'),
    path('ish_turi/<int:pk>/', Ish_TuriDetail.as_view(), name='ish_turi_detail'),
    path('bulim/', BulimList.as_view(), name='bulim'),
    path('bulim/<int:id>/', BulimDetail.as_view(), name='bulim_detail'),
    path('mahsulot/', MahsulotList.as_view(), name='mahsulot'),
    path('mahsulot/<int:id>/', MahsulotDetail.as_view(), name='mahsulot_detail'),
    path('xatolar/', XatolarList.as_view(), name='xatolar'),
    path('xatolar/<int:pk>/', XatolarDetail.as_view(), name='xatolar_detail'),
    path('missed/', MissedList.as_view(), name='missed'),
    path('missed/<int:id>/', MissedDetail.as_view(), name='missed_detail'),
]