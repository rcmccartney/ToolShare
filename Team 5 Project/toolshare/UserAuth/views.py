from django.views import generic
from UserAuth.forms import UserForm, UserProfileForm, UserEditForm
from django.views.generic.edit import FormView
from UserAuth.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pdb
from .utils import CreateAllocateZone
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core import validators
from django.contrib import messages
from django.core.urlresolvers import reverse
from Sharing.models import ShareZone

@login_required(login_url='users:login')
def index(request):
    context = RequestContext(request)
    return render_to_response('UserAuth/index.html', context)

@login_required(login_url='users:login')
def user_preferences(request):
    context = RequestContext(request)
    form = UserPreferences()
    return HttpResponse("Test")

def sign_up(request):
    context = RequestContext(request)
    signed_up=False
    if request.method == 'POST':
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(request.POST['password'])
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            zone = CreateAllocateZone(request.POST['zipcode'])
            profile.sharezone = zone
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully signed up.')
            signed_up=True
            return HttpResponseRedirect(reverse('home'))
    else:
        user_form= UserForm()
        profile_form= UserProfileForm()

    return render_to_response(
        'UserAuth/sign_up.html', {'user_form': user_form, 'profile_form':profile_form, 'signed_up':signed_up}, context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['username']= username
        request.session['password']= password
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.add_message(request, messages.SUCCESS, 'Successfully logged in')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.add_message(request, messages.ERROR, 'User is not active')
        else:
            messages.add_message(request, messages.WARNING, 'Wrong username or password')
        return HttpResponseRedirect(reverse('users:login'))
    else:
        return render_to_response('UserAuth/login.html',{},context)

@login_required(login_url='users:login')
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='users:login')
def user_edit(request):
    context = RequestContext(request)
    edited1=False
    user1 = request.user
    #instill the instance in the form
    edit_form= UserEditForm(instance=request.user)
    current_profile = UserProfile.objects.get(user = request.user)
    profile_form= UserProfileForm(instance = current_profile)

    if request.method == 'POST':
        edit_form= UserEditForm(data=request.POST,instance = request.user)
        profile_form= UserProfileForm(request.POST, request.FILES)
        if edit_form.is_valid() and profile_form.is_valid():
            user=edit_form.save()
            #if user.password is not None and len(user.password) > 0:
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            edited1=True
            messages.add_message(request, messages.SUCCESS, 'Successfully updated.')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.ERROR, profile_form.errors)
            return HttpResponseRedirect(reverse('users:edit'))
    else:
        return render_to_response(
            'UserAuth/edit.html',
            {'edit_form':edit_form,'profile_form':profile_form,'edited1':edited1},
            context)
        return render(request,'UserAuth/edit.html')

@login_required(login_url='users:login')
def changepassword(request):
    changepasswordform = PasswordChangeForm(request.user,data = request.POST) 
    context = RequestContext(request)
    if request.method == 'POST':
        if changepasswordform.is_valid():
            changepasswordform.save()
            messages.add_message(request, messages.SUCCESS, 'Your password has been changed')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(request, messages.ERROR, changepasswordform.errors)
            return HttpResponseRedirect(reverse('users:change_password'))
    else:
        return render_to_response(
                'UserAuth/changepassword.html',
                {'changepasswordform':changepasswordform},
                context)

#Helper Methods
def CreateAllocateZone(code):
    if not ShareZone.objects.filter(zipcode = code):
        new_sharezone = ShareZone(zipcode = code)
        new_sharezone.name =  "ToolShare Zone " + str(code)
        new_sharezone.description = "Zipcode sharezone"
        new_sharezone.zipcode = code 
        new_sharezone.save()
        return new_sharezone
    else:
        old_sharezone = ShareZone.objects.get(zipcode = code) 
        return old_sharezone
