from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from .forms import *#RegistrationForm, LogInForm, UserVerifyForm, CustomUserProfileForm,CustomUserPasswordForm
from .models import User

# Create your views here.

def welcome_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        user = request.user

        return render(request, 'customuser/index_page.html', {'user_data':user,'page_title':'Welcome Page'})

def registration_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#commit=False
            #'first_name', 'last_name', 'email','bio','location','birth_date'
            # form brings back a plain text string, not an encrypted password
            pw = user.password
            # thus we need to use set password to encrypt the password string
            user.set_password(pw)
            user.date_joined=timezone.now()
            user.is_active=0 #change it via mail verification
            user.is_staff=0
            user.user_type='gen'
            user.avatar=''
            user.save()
            return render(request, 'customuser/register.html', {'formresponse':'congrats','page_title':'Registration'})
        else:
            return render(request, 'customuser/register.html', {'form':form,'page_title':'Registration'})
    form = RegistrationForm()
    return render(request, 'customuser/register.html', {'form':form,'page_title':'Registration'})

def login_page(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    else:
        logout(request) #logs out user upon reaching the /login/ page
        email = password = ''

        if request.method == "POST":
            form = LogInForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:

                if user.is_active:#will not work here as authenticate() will already check this
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    form = LogInForm()
                    state = "Your account is not active, please contact the administrator."
                    return render(request, 'customuser/login.html', {'form':form,'formresponse':state,'page_title':'LogIn'})
            else:
                form = LogInForm()
                state = "Your email and/or password were incorrect."
                return render(request, 'customuser/login.html', {'form':form,'formresponse':state,'page_title':'LogIn'})
        else:
            form = LogInForm()
            return render(request, 'customuser/login.html', {'form':form,'page_title':'LogIn'})

def verify_user(request,pk):
    logout(request)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserVerifyForm(request.POST, instance=user, pk=pk)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('/', pk=user.pk)

    elif request.method == "GET":
        form = UserVerifyForm(pk=pk)
        return render(request, 'customuser/verify_user.html', {'form': form,'page_title':'Verify User'})

def user_profile(request):
    user = request.user

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    if request.method == "POST":
        if 'update_user_profile' in request.POST:

            form = CustomUserProfileForm(request.user, request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)#commit=False
                #user.user = request.user
                user.save()
                return render(request, 'customuser/user_profile.html', {'formresponse':'Profile Updated','page_title':'Profile'})
            else:
                return render(request, 'customuser/user_profile.html', {'form':form,'formresponse':form.errors,'page_title':'Profile'})

        else:
            pswrdform = CustomUserPasswordForm(request.user, request.POST, request.FILES, instance=request.user)
            if pswrdform.is_valid():
                user = pswrdform.save(commit=False)
                pw = user.password
                user.set_password(pw)
                user.save()
                #logout user when password change to login with new password
                return HttpResponseRedirect('/logout/')
                #return render(request, 'customuser/user_profile.html', {'formresponse2':'Password Changed','page_title':'Profile'})
            else:
                return render(request, 'customuser/user_profile.html', {'password_form':pswrdform,'formresponse2':pswrdform.errors,'page_title':'Profile'})

    #user = request.user
    form = CustomUserProfileForm(user=user)
    password_form = CustomUserPasswordForm(user=user)

    return render(request, 'customuser/user_profile.html', {'form':form,'password_form':password_form,'user_data':user,'page_title':'Profile'})
