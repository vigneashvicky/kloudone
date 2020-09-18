from django.conf.urls import url
from django.urls import path
from Test_Task.fileupload_app import views


urlpatterns = [
    path('', views.loginIndex, name='login'),
    path('main_page/', views.main_page),
    path('save_orders/', views.save_order, name='files'),
    path('filesmryget/', views.filesummary, name='filesmrydata'),
    path('loginpswd/', views.loginpswd, name='loginpswd'),



]
