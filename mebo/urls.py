from django.urls import path
from . import views

app_name = 'mebo'

urlpatterns = [
    path('',views.index, name='index'),
    path('<int:memo_id>/',views.detail, name='detail'),
    path('memo/create/',views.memo_create, name='memo_create'),
    path('inmemo/create/<int:memo_id>/',views.inmemo_create,name='inmemo_create'),
    path('memo/modify/<int:memo_id>/', views.memo_modify, name='memo_modify'),
    path('memo/delete/<int:memo_id>/',views.memo_delete, name='memo_delete'),
    path('inmemo/modify/<int:inmemo_id>/', views.inmemo_modify, name='inmemo_modify'),
    path('inmemo/delete/<int:inmemo_id>/',views.inmemo_delete, name='inmemo_delete'),
    path('access-ide/',views.ide_redirect,name='secure-ide-view'),
]
