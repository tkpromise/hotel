import json
import hashlib
from suds.client import Client
from xml.sax.saxutils import escape

def gettext(username, password):
    url = 'http://114.55.172.147:9701/MemberService.asmx?wsdl'
    client = Client(url)
    m = hashlib.md5(password.encode('utf-8'))
    pswd = m.hexdigest()
    print(username)
    print(pswd)
    text=client.service.MemberLoginJson(sCondition=username, sPassword=pswd)
    dic = json.loads(escape(text))
    print( dic['MebID'] )

def getintegral(username, password):
    url = 'http://114.55.172.147:9701/MemberService.asmx?wsdl'
    client = Client(url)
    m = hashlib.md5(password.encode('utf-8'))
    pswd = m.hexdigest()
    text=client.service.MemberLoginJson(sCondition=username, sPassword=pswd)
    dic = json.loads(escape(text))
    mid = dic['MebID']
    integral = client.service.GetMemberPointSum(nMebID=mid)
    return integral

getintegral('1986825', '1986825')

