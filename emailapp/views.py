from django.shortcuts import render
from django.http import HttpResponse

from .models import UserInfo
from helpers.email import Email


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html', {'status': ''})


def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    # Three SMTP clients for now
    host_mapping = {'gmail': ['smtp.gmail.com', 587],
                    'outlook': ['smtp.live.com', 587],
                    'yahoo': ['smtp.mail.yahoo.com', 465]}
    client = ''
    for host in host_mapping.keys():
        if host in email:
            client = host
            break
    if client == '':
        return render(request, 'homepage.html', {'status': 'Login Not Successful!'})

    email_object = Email(host=host_mapping.get(client)[0],
                         port=host_mapping.get(client)[1],
                         email=email,
                         password=password)
    if email_object.authenticate_login():
        user_info, created = UserInfo.objects.get_or_create(email=email, password=password,
                                                   host=host_mapping.get(client)[0],
                                                   port=host_mapping.get(client)[1])
        return render(request, 'send_email.html', {'email_object_id': user_info.id, 'status': 'Login Successful!'})

    return render(request, 'homepage.html', {'status': 'Login Not Successful!'})


def send_email(request):
    pass
