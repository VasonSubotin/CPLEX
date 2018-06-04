import sys
import uuid
import time 
import requests 
import json
import numpy as np
import pandas as pd
from os import path


class APItoEmulator:
    def __init__(self):
        #self.Authorization = Authorization
        self.Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiYW5kcml5QGVtb3RvcndlcmtzLmNvbSIsImlzcyI6ImVtdWxhdG9yLWFwaS5lbW90b3J3ZXJrcy5jb20iLCJhdWQiOiJlbXVsYXRvci1hcGkuZW1vdG9yd2Vya3MuY29tIn0.lH_3YG1da8f2Uc6zperTjvXVnZ7R6Bb0ArtY3YZ6eNw"
        self.staticPoint = 'https://emulator-api.juice.net/v1'

    def gett(self, DynamPoint):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        print(endPoint)
        r = requests.get(endPoint,headers = headers)
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)#(json_input)
        else:
            json_input = r.json()
            print("Error status", r.status_code)
            return(json_input)

    def postt(self, DynamPoint, dumps={}, params = {}):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        r = requests.post(endPoint, data = dumps, headers = headers,params=params )
        print("\nServer Responce:", r.text) 
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)#(json_input)
        else:
            json_input = r.json()
            print("Status Code: ", r.status_code)
            return(json_input)
          

    def putt(self, DynamPoint, dumps):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        response = requests.put(endPoint, data = dumps, headers = headers) 
        print("\nPut status:", response.status_code, response.text) 
        return(response.status_code)

    def patch(self, DynamPoint, dumps):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        response = requests.put(endPoint, data = dumps, headers = headers) 
        print("\nPut status:", response.status_code, response.text) 
        return(response.status_code)

    def deletee(self, DynamPoint, dumps = {}):
        headers = {'Content-Type': 'application/json','Authorization': self.Authorization}
        endPoint = self.staticPoint + DynamPoint
        r = requests.delete(endPoint, data=dumps, headers = headers)
        if r.text == "":
            print("No resource found", r.status_code)
            return(r.text)
        else:
            json_input = r.json()
            print("Status Code: ", r.status_code)
            return(json_input)