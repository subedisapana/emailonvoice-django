import email as emale
import imaplib
import smtplib
import sys
import tempfile
import time

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from helpers.email import Email

from .models import UserInfo

#from helpers.readmail import Readmail
email = ""
password = ""
uid = 1

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', {'status': ''})

def logout(request):
    return render(request, 'logout.html', {'status':''})

def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    email_object, status, host, port = retrieve_email_object(email, password)

    if status != '':
        return render(request, 'homepage.html', {'status': status})

    if email_object.authenticate_login():
        user_info, created = UserInfo.objects.get_or_create(email=email, password=password,
                                                   host=host,
                                                   port=port)                                      
        return render(request,'dashboard.html')               
    return render(request, 'homepage.html', {'status': 'Login Not Successful! Please enter your credentials again!'})

def dashboard(request):
    return render(request, 'dashboard.html', {'status': ''})

def sentmail(request):
    user_info = UserInfo.objects.get(id=uid)
    FROM_EMAIL = user_info.email#Enter the email name
    FROM_PWD = user_info.password#Enter email password
    
    #email_object, status, host, port = retrieve_email_object(email, password)

    SMTP_SERVER = "imap.gmail.com"
    NUM_TO_READ = 22 #Replace with number of earliest emails desired

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    #print(mail.list())

    mail.select('"[Gmail]/Sent Mail"')
    typ, data = mail.search(None, 'ALL')

    x = 0
    idList = []

    #Get a list of all the email ids, reverse it so that 
    #the newest ones are at the front of the list
    for id in data[0].rsplit():
        idList.append(id)

    idList = list(reversed(idList))

    #Fetch the first NUM_to_READ email subject lines and 
    #their recipients
    number = []
    email_froms = []
    email_sub = []
    for id in idList:
        typ, data = mail.fetch(id, '(RFC822)')
        #msg = emale.message_from_bytes(data[0][1])
        
        if x >= NUM_TO_READ:
            break
        else:
            x += 1
            msg = emale.message_from_bytes(data[0][1])
            #print(msg['bcc'])
            #print('Message #', x)
            number.append(x)
            email_from = msg['bcc']
            if email_from is None:
                email_from = "self"
            if '<' in email_from:
                _,_,rest = email_from.partition('<')
                result,_,_ = rest.partition('>')
                email_from = result
            email_froms.append(email_from)
            email_subject = msg['subject']
            email_sub.append(email_subject)
            #print('From : ' + email_from)
            #print('Subject : ' + email_subject + '\n')
    #print (email_sub)
    return render(request, 'sentmails.html', {'shankhya':number, 'kasle': email_froms, 'kuro': email_sub})
    #return render(request, 'sentmails.html')

def compose(request):
    return render(request, 'send_email.html', {'email_object_id': uid, 'status': 'Login Successful!'})

def inbox(request):
    user_info = UserInfo.objects.get(id=uid)
    FROM_EMAIL = user_info.email#Enter the email name
    FROM_PWD = user_info.password#Enter email password
    
    #email_object, status, host, port = retrieve_email_object(email, password)

    SMTP_SERVER = "imap.gmail.com"
    NUM_TO_READ = 22 #Replace with number of earliest emails desired

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    #print(mail.list())

    mail.select('inbox')
    typ, data = mail.search(None, 'ALL')

    x = 0
    idList = []

    #Get a list of all the email ids, reverse it so that 
    #the newest ones are at the front of the list
    for id in data[0].rsplit():
        idList.append(id)

    idList = list(reversed(idList))

    #Fetch the first NUM_to_READ email subject lines and 
    #their recipients
    number = []
    email_froms = []
    email_sub = []
    for id in idList:
        typ, data = mail.fetch(id, '(RFC822)')
        #msg = emale.message_from_bytes(data[0][1])
            
        if x >= NUM_TO_READ:
            break
        else:
            x += 1
            msg = emale.message_from_bytes(data[0][1])

            #print('Message #', x)
            number.append(x)
            email_from = msg['from']
            if '<' in email_from:
                _,_,rest = email_from.partition('<')
                result,_,_ = rest.partition('>')
                email_from = result
            email_froms.append(email_from)
            email_subject = msg['subject']
            email_sub.append(email_subject)
            #print('From : ' + email_from)
            #print('Subject : ' + email_subject + '\n')
    #print (email_sub)
    return render(request, 'inbox.html', {'shankhya':number, 'kasle': email_froms, 'kuro': email_sub})

'''
    return render (request, 'inbox.html')
'''

def send_email(request, id):
    try:
        user_info = UserInfo.objects.get(id=id)
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_object, status, host, port = retrieve_email_object(user_info.email, user_info.password)

        if email_object.authenticate_login():
            if email_object.send_email(to_email, subject, message):
                return render(request, 'dashboard.html')
            else:
                return HttpResponse("Message sending unsuccessful!!!")

    except Exception as error:
        print(error)
        return HttpResponse("Error while sending message!!")


def retrieve_email_object(email, password):
    host_mapping = {'gmail': ['smtp.gmail.com', 587],
                    'outlook': ['smtp.live.com', 587],
                    'yahoo': ['smtp.mail.yahoo.com', 465]}
    client = ''
    for host in host_mapping.keys():
        if host in email:
            client = host
            break

    status = ''
    if client == '':
        status = 'Login Unsuccessful! No Email Entered!'
        return None, status, None, None

    email_object = Email(host=host_mapping.get(client)[0],
                         port=host_mapping.get(client)[1],
                         email=email,
                         password=password)
    return email_object, status, host_mapping.get(client)[0], host_mapping.get(client)[1]
