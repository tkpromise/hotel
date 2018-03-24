var xhr = new XMLHttpRequest();
function sendMsg() {
    var name = document.getElementById('name').value;
    var swUrl = 'http://114.55.172.147:9701/MemberService.asmx?op=MemberLogin'
    var soap = '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '<soap:Body><MemberLogin xmlns="http://www.mingyansoft.com/"><sCondition>string</sCondition><sPassword>string</sPassword></MemberLogin></soap:Body></soap:Envelope>'
    xhr.open('POST', wsUrl, true);
    xhr.setRequestHeader("Content-Type: text/xml; charset=utf-8")
    xhr.onreadystatechange = _back;
    xhr.send(soap);
}
function _back() {
    if (xhr.readyState == 4) {
        if(xhr.status == 200) {
            var ret = xhr.responseXML;
            var msg = ret.getElementsByTagName('return')[0];
            document.getElementById('showInfo').innerHTML = msg.text;
        }
    }
}
