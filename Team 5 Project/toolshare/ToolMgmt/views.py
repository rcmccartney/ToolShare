from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ToolMgmt.models import Tool, ToolCategory, ToolStatus
from ToolMgmt.utils import Is_Owner
from UserAuth.models import UserProfile
from django.contrib import messages
from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from itertools import chain
import pdb

@login_required(login_url='users:login')
def index(request):
    all_tools = Tool.objects.all()
    all_tools = Tool.objects.filter(owner__sharezone = request.user.profile.sharezone)
    paginator = Paginator(all_tools, 6)
    page = request.GET.get('page')

    try:
        paged_tools = paginator.page(page)
    except PageNotAnInteger:
        paged_tools = paginator.page(1)
    except EmptyPage:
        paged_tools = paginator.page(paginator.num_pages)

    return render(request, 'ToolMgmt/index.html', {'all_tools': paged_tools})

@login_required(login_url='users:login')
def mytools(request):
    my_tools = Tool.objects.filter( owner = request.user.profile)
    return render(request, 'ToolMgmt/mytools.html', {'my_tools': my_tools})

@login_required(login_url='users:login')
def register(request):
    context = RequestContext(request)
    if request.POST:
        form = ToolModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_tool = form.save()
            new_tool.owner = UserProfile.objects.get( user = request.user)
            new_tool.actire = True
            new_tool.save()
            messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
            return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
        else:
            return render_to_response('ToolMgmt/register.html', {'form': form}, context)
    else:
        form = ToolModelForm()
        return render_to_response('ToolMgmt/register.html', {'form': form}, context)

@login_required(login_url='users:login')
def tool_edit(request, tool_id):
    context = RequestContext(request)
    tool = Tool.objects.get(id=tool_id)
    is_owner = Is_Owner(request.user.profile,tool)
    if is_owner:
        if request.POST:
            form = ToolModelForm(request.POST, request.FILES, instance=tool)
            if form.is_valid():
                new_tool = form.save()
                new_tool.owner = UserProfile.objects.get( user = request.user)
                new_tool.save()
                messages.add_message(request, messages.SUCCESS, 'Tool %s was successfully created' % new_tool)
                return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': new_tool.id}))
            else:
                return render_to_response('ToolMgmt/edit.html', {'form': form, 'tool' : tool}, context)
        else:
            form = ToolModelForm(instance=tool)
            return render_to_response('ToolMgmt/edit.html', {'form': form, 'tool' : tool}, context)
    else:
        messages.add_message(request,messages.ERROR, 'You are not authorised to edit this tool')
        return HttpResponseRedirect(reverse('toolmgmt:detail',kwargs = {'tool_id':tool_id}))

class ToolModelForm(forms.ModelForm):
    error_category = {
        'required': 'You must select a category.',
        # 'invalid': 'Wrong selection.'
    }

    identifier = forms.CharField(label="Identifier", help_text="Unique identifier to distinguish between similar tools", required=False)
    category = forms.ModelChoiceField(label="Category",queryset=ToolCategory.objects.all(), error_messages=error_category)
    class Meta:
        model = Tool
        fields= ('name', 'description', 'category', 'status', 'image', 'identifier', 'active')

@login_required(login_url='users:login')
def detail(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)
    is_owner = Is_Owner( request.user.profile, tool)
    if (request.method == 'GET'):
        return render(request, 'ToolMgmt/detail.html', {'tool': tool,'is_owner':is_owner})
    else:
        tool = Tool.objects.get(pk=tool_id)
        if tool.active:
            tool.active = False
        else:
            tool.active = True
        tool.save()
        return HttpResponseRedirect(reverse('toolmgmt:detail', kwargs={'tool_id': tool_id}))
