from django.shortcuts import render
import json
import base64
from Test_Task.fileupload_app.Model import filemodel
import requests
from django.http import JsonResponse
import datetime
import Test_Task.fileupload_app.jwt_file as jwt

def main_page(request):
    return render(request, "Main_page.html")

def loginIndex(request):
    return render(request, "Login.html")

def save_order(request):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            datas = json.dumps(jsondata)
            params = {'Group': "INSERT"}
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("http://127.0.0.1:8001/order_save", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            return e


def filesummary(request):
    try:
        if request.method == 'POST':
            jsondata = json.loads(request.body.decode('utf-8'))
            params = {'Group': "FILE_SUMMARY" }
            datas = json.dumps(jsondata)
            token = jwt.token(request)
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("http://127.0.0.1:8001/File_data_view", params=params, headers=headers, data=datas, verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)
    except Exception as e:
        return e

def loginpswd(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Type = jsondata.get('parms').get('TYPE')
        if Type == 'LOGIN_LOCAL':
            obj_location = filemodel.Sales_Model()
            obj_location.code = jsondata.get('parms').get('username')
            obj_location.password = jsondata.get('parms').get('password')
            result = obj_location.get_login()
            if (result[1][0] == 'SUCCESS'):
                request.session.flush()
                out_msg = token_jwt(request, "LOGIN",obj_location.code)
                if out_msg != 'SUCCESS':
                    return JsonResponse(json.dumps('FAIL'), safe=False)

                request.session['Emp_gid'] = result[0][0].get('employee_gid')
                request.session['Emp_name'] = result[0][0].get('employee_name')
                request.session['Entity_gid'] = result[0][0].get('entity_gid')
                request.session['Entity_state_gid'] = 1
                request.session['Entity_detail_gid'] = 1
                request.session['Branch_gid'] = result[0][0].get('branch_gid')
                output = result[0][0]
                return JsonResponse(json.dumps(output), safe=False)
            else:
                return JsonResponse(json.dumps('FAIL'), safe=False)
    else:
        return render(request, "Shared/bigFlowLogin.html")



def token_jwt(request,ref,username):
    try:
        if ref == 'LOGIN':
            datenow = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            password = datenow + username[::-1]
            password = filemodel.converttoascii(password)
            headers = {"content-type": "application/json"}
            params = ''
            datas = json.dumps({"username":username,"password":"abcd","auth_pwd":password,"apitype":"Direct"})
            resp = requests.post("http://127.0.0.1:8001/token", params=params, data=datas, headers=headers,
                                 verify=False)

            token_data = json.loads(resp.content.decode("utf-8"))
            ### Validations
            if token_data != '' and resp.status_code == 200 :
                access_token = token_data.get("access")
                refresh_token = token_data.get("refresh")
                access_expirytime = access_token.split('.')
                access_expirytime = access_expirytime[1]
                access_expirytime = base64.b64decode(access_expirytime +"==")
                access_expirytime = json.loads(access_expirytime)
                access_expirytime = access_expirytime.get("exp")
                access_expirytime = datetime.datetime.fromtimestamp(access_expirytime).strftime("%I:%M:%S")
                request.session["access_token"] = access_token
                request.session["refresh_token"] = refresh_token
                request.session["access_expirytime"] = access_expirytime
                refresh_expirytime = refresh_token.split('.')
                refresh_expirytime = refresh_expirytime[1]
                refresh_expirytime = base64.b64decode(refresh_expirytime + "==")
                refresh_expirytime = json.loads(refresh_expirytime)
                refresh_expirytime = refresh_expirytime.get("exp")
                refresh_expirytime = datetime.datetime.fromtimestamp(refresh_expirytime).strftime("%m/%d/%Y, %H:%M:%S")
                request.session["refresh_expirytime"] = refresh_expirytime

                return 'SUCCESS'
            elif resp.status_code != 200:
                return 'FAIL'


        elif ref =='CHECK':
            if datetime.datetime.now().strftime("%I:%M:%S") < request.session["access_expirytime"] :
                return request.session["access_token"]
            elif datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") < request.session["refresh_expirytime"]:
                headers = {"content-type": "application/json"}
                params = ''
                datas = json.dumps({"refresh":request.session["refresh_token"] })
                resp = requests.post("http://127.0.0.1:8001/api/token/refresh/", params=params, data=datas, headers=headers,
                                     verify=False)
                token_data = json.loads(resp.content.decode("utf-8"))
                access_token = token_data.get("access")
                access_expirytime = access_token.split('.')
                access_expirytime = access_expirytime[1]
                access_expirytime = base64.b64decode(access_expirytime +"==")
                access_expirytime = json.loads(access_expirytime)
                access_expirytime = access_expirytime.get("exp")
                access_expirytime = datetime.datetime.fromtimestamp(access_expirytime).strftime("%I:%M:%S")
                request.session["access_token"] = access_token
                request.session["access_expirytime"] = access_expirytime
                return access_token
            else:
                request.session.flush()
                return 'FAIL'
    except Exception as e:
        return 'FAIL'

