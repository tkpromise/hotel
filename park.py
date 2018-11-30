import json
import xmltodict
from urllib import request

def reMebid():
    url = 'http://220.160.111.118:8099/WebServiceForPay.asmx?op=PayCarCardFee'

    data = '<?xml version="1.0" encoding="utf-8"?>'
    data += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    data += '<soap:Body>'
    data += '<PayCarCardFee xmlns="http://www.keytop.com.cn/">'
    data += '<appId>1</appId>'
    data += '<key>b20887292a374637b4a9d6e9f940b1e6</key'
    #data += '<key>b20887292a374637b4a9d6e9f940b1e6</key>'
    data += '</GetPersonMemberByMobile>'
    data += '<orderNo>168</orderNo>'
    data += '<amount>1</amount>'
    data += '</PayCarCardFee>'
    data += '</soap:Body>'
    data += '</soap:Envelope>'

    headers = {'Content-Type': 'text/xml'}

    req = request.Request(url, data=data.encode('utf-8'), headers=headers)
    x = request.urlopen(req)

    xmlparse = xmltodict.parse(x) 

    t = xmlparse['soap:Envelope']['soap:Body']['GetPersonMemberByMobileResponse']['GetPersonMemberByMobileResult']['MebID']
    print(t)
    return str(t)

reMebid()
