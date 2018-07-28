from django.shortcuts import render
from django.http import HttpResponse

from .models import UserInfo
from helpers.email import Email
from helpers import readmail

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', {'status': ''})


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
        return render(request, 'send_email.html', {'email_object_id': user_info.id, 'status': 'Login Successful!'})

    return render(request, 'homepage.html', {'status': 'Login Not Successful! Please enter your credentials again!'})


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
