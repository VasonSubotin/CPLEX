# Sample Test passing with nose and pytest
staticPoint = 'https://emulator-api.juice.net/v1'
#staticPoint = 'https://bc65934f-ba9e-4ad7-be60-c64e867ceaa1.mock.pstmn.io'
Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiYW5kcml5QGVtb3RvcndlcmtzLmNvbSIsImlzcyI6ImVtdWxhdG9yLWFwaS5lbW90b3J3ZXJrcy5jb20iLCJhdWQiOiJlbXVsYXRvci1hcGkuZW1vdG9yd2Vya3MuY29tIn0.lH_3YG1da8f2Uc6zperTjvXVnZ7R6Bb0ArtY3YZ6eNw"

import ccemulator as cc
from ccemulator.mainmodule import session as ss

from ccemulator.APIRequest import APItoEmulator as api
from .. import ccemulator
def test_pass():
        assert True, "dummy sample test"

#def testgetall():

     #ss.packtest(staticPoint,Authorization)
s= ss
ss.hello()
