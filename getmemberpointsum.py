import json
import xmltodict
from urllib import request

def repoint(mebid):
    url = 'http://114.55.172.147:9701/MemberService.asmx?op=GetMemberPointSum'

    # gouzaoqingqiu
    data = '<?xml version="1.0" encoding="utf-8"?>'
    data += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    data += '<soap:Body>'
    data += '<GetMemberPointSum xmlns="http://www.mingyansoft.com/">'
    data += '<nMebID>'+mebid+'</nMebID>'
    data += '</GetMemberPointSum>'
    data += '</soap:Body>'
    data += '</soap:Envelope>'

    # qingqiutou
    headers = {'Content-Type': 'text/xml'}

    # use Request gouzaoyigewanzengdeqingqiutou
    req = request.Request(url, data=data.encode('utf-8'), headers=headers)
    x = request.urlopen(req)

    xmlparse = xmltodict.parse(x) 

    t = xmlparse['soap:Envelope']['soap:Body']['GetMemberPointSumResponse']['GetMemberPointSumResult']
    print(t)
    return str(t)

#repoint('23748')
