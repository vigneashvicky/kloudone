

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
import datetime

from Test_Task.fileupload_app.Model import filemodel

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        # The default result (access/refresh tokens)
      #  data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        try:
            if (self.context['request'].data['apitype']) == 'Indirect' :

                obj_location = filemodel.login()
                obj_location.code = (self.context['request'].data['employee_id'])
                obj_location.password = (self.context['request'].data['employee_pwd'])
                result = obj_location.get_login()
                if result[1][0] == 'SUCCESS':
                    data["refresh"] = str(refresh)
                    data["access"] = str(refresh.access_token)
                    return data
                else :
                    return {"Error":"Fail In Login"}
            elif (self.context['request'].data['apitype']) == 'Direct':
                datenow = str(datetime.datetime.now().strftime("%Y-%m-%d"))
                password = (self.context['request'].data['username'])
                password = datenow+password[::-1]
                password = filemodel.converttoascii(password)
                auth_pwd = self.context['request'].data['auth_pwd']
                if password == auth_pwd:
                    data["refresh"] = str(refresh)
                    data["access"] = str(refresh.access_token)
                    return data
                else:
                    return {"Error": "Authentication Failed."}
            else:
                return {"Error": "Enter Valid Type"}
        except Exception as e:
            return ({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class CustomTokenverifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        verify= TokenVerifySerializer.validate(self,attrs)

        return verify

def deff():
    TokenVerifySerializer().validate()



class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
token_refresh = TokenRefreshView.as_view()

class verifyToken(TokenVerifyView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenverifySerializer