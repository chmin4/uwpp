from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'common'

urlpatterns = [
    path('userpage/',views.userpage, name='userpage'),
    path('login/',auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('intro/',views.intro , name='intro'),
    path('file_list/',views.file_list, name='file_list'),
    path('upload/',views.upload_file, name='upload'),
    path('download/<int:file_id>',views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),

]
