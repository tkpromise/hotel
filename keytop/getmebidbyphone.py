import json
import xmltodict
from urllib import request

def reMebid(phone):
    url = 'http://114.55.172.147:9701/MemberService.asmx?op=GetPersonMemberByMobile'

    data = '<?xml version="1.0" encoding="utf-8"?>'
    data += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    data += '<soap:Body>'
    data += '<GetPersonMemberByMobile xmlns="http://www.mingyansoft.com/">'
    data += '<sMobile>'+phone+'</sMobile>'
    data += '</GetPersonMemberByMobile>'
    data += '</soap:Body>'
    data += '</soap:Envelope>'

    headers = {'Content-Type': 'text/xml'}

    req = request.Request(url, data=data.encode('utf-8'), headers=headers)
    x = request.urlopen(req)

    xmlparse = xmltodict.parse(x) 

    t = xmlparse['soap:Envelope']['soap:Body']['GetPersonMemberByMobileResponse']['GetPersonMemberByMobileResult']['MebID']
    print(t)
    return str(t)

reMebid('18758831324')
