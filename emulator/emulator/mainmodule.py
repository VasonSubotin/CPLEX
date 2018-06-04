#staticPoint = 'https://bc65934f-ba9e-4ad7-be60-c64e867ceaa1.mock.pstmn.io'
#staticPoint = 'https://emwemulator-api.azurewebsites.net/v1'
#sys.path.append('E:\Projects\emulatorrep\emulator')

import sys
import emulator
import uuid
import time 
import requests 
import json
import numpy as np
import pandas as pd
from emulator.APIRequest import APItoEmulator as api
from os import path

#staticPoint = 'https://emulator-api.juice.net/v1'
#Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiYW5kcml5QGVtb3RvcndlcmtzLmNvbSIsImlzcyI6ImVtdWxhdG9yLWFwaS5lbW90b3J3ZXJrcy5jb20iLCJhdWQiOiJlbXVsYXRvci1hcGkuZW1vdG9yd2Vya3MuY29tIn0.lH_3YG1da8f2Uc6zperTjvXVnZ7R6Bb0ArtY3YZ6eNw"

class session:
    def __init__(self,staticPoint, Authorization):
        self.staticPoint = staticPoint
        self.Authorization = Authorization
        self.SessionId = uuid.uuid4()
        self.TemplateList = []
        print("SessionId: ",self.SessionId)
        self.wanted_keys = ["template_id", "voltage", "instant_current","temperature", "frequency","plugged_in","online","instance_count"]
        

    
    def _GenerateCustomDataFrameForTemplates(self, number, instance_count):
        startNum, trash = self._findMaxIndexofTemplateList(self.TemplateList)
        startNum = startNum+1
        template_id = list(np.empty(number))
        template_id = None
        voltage = list(np.random.randint(2350,2450,size=(number)))
        instant_current = list(np.random.randint(350,470,size=(number)))
        temperature = list(np.random.randint(25,39,size=(number)))
        frequency = list(np.random.randint(340,349,size=(number)))
        df = pd.DataFrame({"template_id":template_id, "voltage": voltage, "instant_current":instant_current,"temperature":temperature, "frequency":frequency},
                          columns = ['template_id','voltage', 'instant_current', 'temperature', 'frequency' ])
        df["plugged_in"] = False
        df["online"] = False
        df["instance_count"] = instance_count
        print(df.head())
        return(df)
        
               
    def AddSomeTemplatestoSession(self, number, instance_count):
        df = self._GenerateCustomDataFrameForTemplates(number, instance_count)

        for row in df.iterrows():
            temp = Template(staticPoint, row[1].tolist())#[1:len(row[1])].tolist())
            
                                # Post all/one devices onto the backend
            self.TemplateList.append(temp)
            json = api.postt(self, "/templates/", temp.Json)

            temp.template_id = json["template_id"] 
            print("Object Json", temp.Json)
                                
    def FindAllTemplatesForSessionObject(self):
         for index, template in enumerate(self.TemplateList):
             print(template.Json)

            
    def _findMaxIndexofTemplateList(self, obj):
        tls = []
        if self.TemplateList ==[]:
            result = -1
        else:
            for index, temp in enumerate(self.TemplateList):
                tls.append(temp.template_id)
            result = max(tls) 
        return(result, tls)

                                # Modify a Template from session based on its Id         
    def ModifyTemplateParam(self, template_id, Param, value):
        if self._FindTemplateBasedOnId(template_id):
            setattr(self._FindTemplateBasedOnId(template_id), Param, value)
            self._FindTemplateBasedOnId(template_id).Json = self._FindTemplateBasedOnId(template_id).WriteJsonFromTemplateAttr()
            print("Updated Json is:", self._FindTemplateBasedOnId(template_id).Json)
            GetResult = api.putt(self, "/templates/{}".format(template_id), self._FindTemplateBasedOnId(template_id).Json )
            print(GetResult)
        else:
            print("No resouce found")

    def ModifySetOfParamPATCH(self, template_id, ListParamandValues):
        dic = dict([(k, v) for k,v in zip (ListParamandValues[::2], ListParamandValues[1::2])])
        if self._FindTemplateBasedOnId(template_id):
            for Param, value in dic.items():
                        setattr(self._FindTemplateBasedOnId(template_id), Param, value)
                        self._FindTemplateBasedOnId(template_id).Json = self._FindTemplateBasedOnId(template_id).WriteJsonFromTemplateAttr()
            GetResult = api.patch(self, "/templates/{}".format(template_id), self._FindTemplateBasedOnId(template_id).Json )
            print(GetResult)
        else:
            print("Template_id is invalid")


                                        # Get a Template from session based on its Id

    def GetOneTemplate(self, template_id):
        GetResult = api.gett(self, "/templates/{}".format(template_id))
        self._EitherToAddTemplateToTemplalteListOrNot(GetResult)
        print(GetResult)
     

                                # Get All Template from session
    def GetAllTemplate(self):
        GetResult = api.gett(self, "/templates/")
        for index, obj in enumerate(GetResult):
            self._EitherToAddTemplateToTemplalteListOrNot(obj)
            print(obj)
    
    def _EitherToAddTemplateToTemplalteListOrNot(self, obj):
        dic = dict((k, obj[k]) for k in self.wanted_keys if k in obj)
        if bool(dic): 
            if  not self._FindTemplateBasedOnId(dic["template_id"]):
                temp = Template(self.staticPoint, list(dic.values()))
                self.TemplateList.append(temp)
            
            else:
                print("Template exists, nothing to add")



    def _FindTemplateBasedOnId(self, template_id):
        return(next((template for template in self.TemplateList if template.template_id == template_id),False) )
            

                                # Delete a Template from session based on its Id : {{url}}/templates/{id}
    def _EitherToDeleteTemplateFromTemplalteListOrNot(self, obj):
        if not self._FindTemplateBasedOnId(obj.template_id):
            print("Temaplate does not exist in Template List, nothing to delete")
        else:
            self.TemplateList.remove(obj)
            print("Template with {} deleted".format(obj.template_id))
            print("\nTamplets left:", len(self.TemplateList ))


    def DeleteOneItemFromListBasedOnId(self, template_id):
        temp = self._FindTemplateBasedOnId(template_id)
        if not temp:
            print("None found")
        else:
            api.deletee(self, "/templates/{}".format(template_id))
            self._EitherToDeleteTemplateFromTemplalteListOrNot(temp)


                                # Delete all Tamplates from session and backend: {{url}}/templates/ 
    def DeleteAllItemsFromList(self):
        max, ids = self._findMaxIndexofTemplateList(self.TemplateList)
        self.TemplateList.clear()
        api.deletee(self, "/templates/")
        print("\nTemplateList is empty", len(self.TemplateList))

                                # Get status of plugged or online states for Template: {{url}}/templates/{id}/plugged_in 
    def GetStatus(self, template_id, status):
        GetResult = api.gett(self, "/templates/{}/{}".format(template_id,status))
        print(GetResult)
                                # Update status of plugged or online states for a Template: {{url}}/templates/{id}/online 
    def UpdateStatus(self, template_id, status, value):
        GetResult = api.putt(self, "/templates/{}/{}".format(template_id,status))
        print(GetResult)

    def hello(self):
        """EPRST """
        return("Hello Package!")

    def packtest(self):
        self.GetAllTemplate(self)

    def main(self):
        s = session(staticPoint,Authorization)
        s.GetAllTemplate(s)

        
class Template(session):

    def __init__(self, staticPoint,  ParamList):
        self.template_id, self.voltage, self.instant_current, self.temperature, self.frequency, self.plugged_in,  self.online, self.instance_count = ParamList
        self.Json = self.WriteJsonFromTemplateAttr()
        
        
        

    def WriteJsonFromTemplateAttr(self):
        body_request = {"voltage": self.voltage, "instant_current": self.instant_current, "temperature": self.temperature,
                      "frequency": self.frequency,  "plugged_in": self.plugged_in, "online": self.online, "instance_count": self.instance_count}
        dumps = json.dumps(body_request)
        return(dumps)

    def WriteJsonFromTemplateFewAttr(self, ParamNameValues ):
        dic = dict([(k, v) for k,v in zip (ParamNameValue[::2], ParamNameValue[1::2])])
        body_request = dic
        dumps = json.dumps(body_request)
        print("dumps", dumps)
        return(dumps)



    if __name__=="__main__":
        main()



#s.AddSomeTemplatestoSession(1,2)
#s.ModifySetOfParamPATCH(70, ["voltage",555,"frequency", 55])

#sys.path.append("C:/Users/EMV_AF/source/repos/PythonApplication2/EmulatorPRoject")