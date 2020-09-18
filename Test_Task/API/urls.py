from django.urls import path
from Test_Task.API import views as view
from Test_Task.API import view_file as view_file

urlpatterns = [
    path('token', view.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', view.TokenRefreshView.as_view(), name='token_refresh'),
    path('order_save', view_file.video_upload.as_view()),
    path('File_data_view', view_file.video_upload.as_view()),
]


