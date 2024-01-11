
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
#from django.contrib.sites.shortcuts import get_current_site
#from django.core.mail import EmailMessage
#from django.template.loader import render_to_string
# Create your views here.
def loginuser(request):
    if request.method=="POST":
        form=AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('homeview')
            else:
                messages.error(request, 'Invalid Username or password')
        else:
            messages.error(request, 'Invalid Username or password')
    else:
        form=AuthenticationForm()
    return render(request, 'session/login.html',{'form':form})

def logoutuser(request):
    logout(request)
    messages.success(request, "successfully logged out!")
    return redirect('homeview') 
from .forms import SignUpForm

def registration(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form=SignUpForm()
    return render(request, 'session/signup.html',{'form':form})

def change_password(request):
    if request.method=="POST":
        form= PasswordChangeForm(data=request.POST, user=request.user)  
        if form.is_valid():
            update_session_auth_hash(request, form.user)  
            messages.success(request, " Password has successfully Changed")
            return redirect('homeview')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request, 'session/change_pass.html',{'form':form})

from .forms import UserProfileForm
from .models import UserProfile

def userProfile(request):
    try:
        instance= UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance=None
    if request.method=="POST":
        if instance:
            form=UserProfileForm(request.POST,request.FILES, instance=instance)
        else:
            form=UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "successfully Saved Your profile")
            return redirect('homeview')
    else:
        form=UserProfileForm(instance=instance)
    context={
        'form':form
    }
    return render(request,'session/userproCreate.html',context)
def ownerprofile(request):
    user=request.user
    return render (request,'session/userprofile.html',{'user':user})
        