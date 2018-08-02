import email
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
uid = ""

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
        uid = user_info.id        
        print (uid)                                  
        return render(request,'dashboard.html')    
    #return render(request, 'send_email.html', {'email_object_id': user_info.id, 'status': 'Login Successful!'})               
    return render(request, 'homepage.html', {'status': 'Login Not Successful! Please enter your credentials again!'})

def dashboard(request):
    return render(request, 'dashboard.html', {'status': ''})

def compose(request):

    return render(request, 'send_email.html', {'email_object_id': uid, 'status': 'Login Successful!'})
    '''
    if request.method == 'POST':
        form = send_email(request.POST or None,id)
        if form.is_valid():
            #unpack form values
            to_email= form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_object = retrieve_email_object(email, password)

            if email_object.send_email(to_email,subject,message):
                return HttpResponse("Message sent successfully!!!")

            else:
                return HttpResponse("Message sending unsuccessful!!!")
                

        return HttpResponseRedirect(reverse('email'))   
    else:
        form = send_email(request,id)
     '''   
    #return render(request, 'send_email.html') #, {'form':form})

def inbox(request):
    FROM_EMAIL = email #Enter the email name
    FROM_PWD = password #Enter email password

    email_object, status, host, port = retrieve_email_object(email, password)

    SMTP_SERVER = "imap.gmail.com"
    NUM_TO_READ = 10 #Replace with number of earliest emails desired

    #Establish a connection and login to the Gmail account
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    if email_object.authenticate_login():
        
        mail.login(FROM_EMAIL,FROM_PWD)

    #Look for all emails in the inbox
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
    for id in idList:
        typ, data = mail.fetch(id, '(RFC822)')

        if x >= NUM_TO_READ:
            break
        else:
            x += 1
            msg = email.message_from_bytes(data[0][1])

            print('Message #', x)
            email_subject = msg['subject']
            email_from = msg['from']
            print('From : ' + email_from)
            print('Subject : ' + email_subject + '\n')

    return render(request, 'inbox.html',{'msg':msg})



def send_email(request, id):
    try:
        user_info = UserInfo.objects.get(id=id)
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_object, status, host, port = retrieve_email_object(user_info.email, user_info.password)

        if email_object.authenticate_login():
            if email_object.send_email(to_email, subject, message):
                return HttpResponse("Message sent successfully!!!")
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
