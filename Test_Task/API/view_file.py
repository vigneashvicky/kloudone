from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Test_Task.fileupload_app.Model import filemodel
import datetime
from Test_Task.settings import BASE_DIR, MEDIA_URL
from pathlib import Path
import base64

class video_upload(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "INSERT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = filemodel.Sales_Model()
                obj.Action = jsondata.get('Action')
                obj.json_data = jsondata.get('data').get('Params')
                jsonData = jsondata.get('data').get('Params')
                e = jsonData['Array']
                clasify = jsondata.get('data').get('Params').get('Client_name')
                obj.create_by = jsondata.get('data').get('Params').get('Client_Id')

                filejson_data = File_Upload(e,clasify)
                obj.json_data.update(filejson_data)
                ld_out_message = obj.upload_video()
                if (ld_out_message[0] > 0):
                    ld_dict = {"DATA": ld_out_message,
                                   "MESSAGE": 'SUCCESS'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FILE_SUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj = filemodel.Sales_Model()
                obj.Action = jsondata.get('Params').get('Action')
                ld_out_message = obj.get_smry_data()
                ld_dict = {"DATA": json.loads(ld_out_message.to_json(orient='records')),
                           "MESSAGE": "FOUND"}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
import json

def File_Upload(file_list,client):
    file_name_new = client + '_' + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
    current_month = datetime.datetime.now().strftime('%m')
    current_day = datetime.datetime.now().strftime('%d')
    current_year_full = datetime.datetime.now().strftime('%Y')
    # /media/  is the MEDIA_URL

    lsfile_name = str((BASE_DIR + '/Test_Task' + "/media/" + "JSON" + '/'
                       + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' +
                       file_name_new + '.' + 'json'))

    path = Path(lsfile_name)
    path.parent.mkdir(parents=True, exist_ok=True)

    dict = {"OREDERED_DATA":file_list}
    out_file = open(lsfile_name, "w")
    json.dump(dict, out_file, indent=6)
    out_file.close()
    ld_saved_file = {"file_name": file_name_new + '.' + 'json',
                        }
    return ld_saved_file  ### Wip for Multiple Files