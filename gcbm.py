import json
import xmltodict
from urllib import request

def reCoupon(mebid):
    url = 'http://114.55.172.147:9701/DisountCouponsService.asmx?op=QueryCouponsListByMebID'

    data = '<?xml version="1.0" encoding="utf-8"?>'
    data += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    data += '<soap:Body>'
    data += '<QueryCouponsListByMebID xmlns="www.mingyansoft.com">'
    data += '<nMebID>'+mebid+'</nMebID>'
    data += '<objCondition>'
    data += '</objCondition>'
    data += '<nPageSize>100</nPageSize>'
    data += '<nPageNo>1</nPageNo>'
    data += '</QueryCouponsListByMebID>'
    data += '</soap:Body>'
    data += '</soap:Envelope>'
    
    headers = {'Content-Type': 'text/xml'}
    
    req = request.Request(url, data=data.encode('utf-8'), headers=headers)
    x = request.urlopen(req)
    
    xmlparse = xmltodict.parse(x) 
    
    t = xmlparse['soap:Envelope']['soap:Body']['QueryCouponsListByMebIDResponse']['QueryCouponsListByMebIDResult']['DataSet']['DiscountCoupons']
    
    
    lister = []
    if isinstance(t,list):
        for i in t:
            coupon = {
            'DiscountID':i['DiscountID'],
            'Value':i['Value'],
            'BeginDate':i['BeginDate'],
            'EndDate':i['EndDate'],
            'DisTypeName':i['DisTypeName']
            }
            lister.append(coupon)
        print(lister)
    else:
        coupon = {
            'DiscountID':t['DiscountID'],
            'Value':t['Value'],
            'BeginDate':t['BeginDate'],
            'EndDate':t['EndDate'],
            'DisTypeName':t['DisTypeName']
        }
        lister.append(coupon)
        print(lister)

reCoupon('81278')
