from django.contrib.sites import requests
import requests

from Test_Task.fileupload_app import views as views
## Role Based Token Will Assign if needed
def token(request):
    acces_token = views.token_jwt(request,"CHECK",'')
    return "Bearer  " + acces_token