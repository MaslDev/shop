from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from authentication.models import Customer
from authentication.user import User

# Create your views here.
@require_POST
def user_login(request):
    email = request.POST['email']
    password = request.POST['password']
    response_data = {}
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                response_data = {'response': 'success'}
        else:
            response_data = {'response': "dismatch"}
    except User.DoesNotExist:
        response_data = {'response': "nouser"}
    return JsonResponse(response_data)


def user_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def signup(request):
    return render(request, 'registration/page_sign_up.html')


@require_POST
def user_create(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    phone = request.POST['phone']
    response_data = {}
    if (User.objects.filter(email=email).exists()):
        response_data = {'response': 'yesemail'}
    elif (User.objects.filter(phone=phone).exists()):
        response_data = {'response': 'yesphone'}
    else:
        customer = Customer.objects.create_user(email=email, phone=phone, first_name=first_name, last_name=last_name,
                                                password=password,
                                                is_active=False)
        subject = 'Account activation'
        id = customer.id
        activate_url = 'http://127.0.0.1:8000/accounts/user_activate/{}'.format(id)
        msg = 'Hi, welcome to our shop \n\nTo activate your account, follow the link below: \n{} \n\nIf you have not registered on our site, just ignore this message.'.format(
            activate_url)
        customer.email_user(subject=subject, message=msg)
        response_data = {'response': 'success'}
    return JsonResponse(response_data)


@require_GET
def user_activate(request, id):
    user = Customer.objects.get(id=id)
    user.is_active = True
    user.save()
    return render(request, 'registration/page_account_activate_success.html')


def forgot_password(request):
    return render(request, 'registration/page_forgot_password.html')


@require_POST
def forgot_password_send_email(request):
    email = request.POST['email']
    response_data = {}
    try:
        user = User.objects.get(email=email)
        subject = 'Change Password'
        id = user.id
        url = 'http://127.0.0.1:8000/accounts/change_password/{}'.format(id)
        msg = 'Hi, If you really want to change your password, click on the link below. \n{} \n\nUnless you requested a password change, just ignore this message.'.format(
            url)
        user.email_user(subject=subject, message=msg)
        response_data = {'response': 'success'}
    except User.DoesNotExist:
        response_data = {'response': "nouser"}
    return JsonResponse(response_data)


@require_GET
def change_password(request, id):
    return render(request, 'registration/page_change_password.html', {'id': id})


@require_GET
def change_password_success(request):
    password = request.GET['password']
    response_data = {}
    user = User.objects.get(id=request.GET['id'])
    user.set_password(password)
    user.save()
    response_data = {'response': 'success'}
    return JsonResponse(response_data)
