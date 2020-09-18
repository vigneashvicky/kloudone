from django.db import connection
import pandas as pd
import json
# from Test_Task.fileupload_app.Model import mfile


class Sales_Model():
    def upload_video(self):
        cursor = connection.cursor()
        parameters = (self.Action,json.dumps(self.json_data),self.create_by, '')
        cursor.callproc('sp_order_set', parameters)
        cursor.execute('select @_sp_order_set_2')
        output_msg = cursor.fetchone()
        return output_msg

    def get_smry_data(self):
        cursor = connection.cursor()
        parameters = (self.Action,'{}','{}' ,'')
        cursor.callproc('Sp_Order_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        rows = list(rows)
        df_grndetail = pd.DataFrame(rows, columns=columns)
        return df_grndetail

    def get_login(self):
        cursor = connection.cursor()
        param = (0, self.code, converttoascii(self.password), '')
        cursor.callproc("sp_client_Get",param)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.execute('select @_sp_client_Get_3')
        id = cursor.fetchone()
        ldist = [ldict, id]
        return ldist

def converttoascii(password):
    l=len(password)
    newuser=''
    for i in range(0,l):
        tmp=ord(password[i])
        temp = tmp - l
        g=len(str(temp))
        newuser = newuser + ("0" if g < 3 else "") + str(temp)
    return newuser


