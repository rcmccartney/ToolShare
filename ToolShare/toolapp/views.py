from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from toolapp.models import ToolUser, Tool, ShareZone,CommunityShed, ToolStatistics
from toolapp.forms import RegisterToolForm,CustomRegistrationForm, ProfilePersonalInfoToolUserForm, ProfilePersonalInfoToolUserForm, ProfilePreferencesToolUserForm,BorrowRequestForm,CreateCommunityShedForm
from django.contrib.auth.models import Permission,User
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from registration.backends.default.views import RegistrationView
from django.contrib import messages
from toolapp import forms
from toolapp import models
import pprint;
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.utils import timezone

'''
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return index(request)
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        print("The username and password were incorrect.")
'''

def home(request):
    if (request.user.is_authenticated()):
        return redirect('/my-tools')
    return login(request, template_name='toolapp/index.html')

def logout_view(request):
    logout(request)
    return redirect('/index/')

def index(request):
    print(request.user)
    latest_user_list = ToolUser.objects.order_by('-date_joined')[:5]
    context = {'latest_user_list': latest_user_list }
    return render(request, 'toolapp/index.html', context)

@login_required
def profile_personalInfo(request):
    if request.method == 'POST':        
        _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
        form = ProfilePersonalInfoToolUserForm(request.POST, instance=_toolUser,request=request)        
        if form.is_valid():
            messages.success(request, 'Your changes have been successfully saved') 
            newUser = form.save(commit=False)                        
            newUser.save()
            
            return render(request, 'toolapp/profile.html', {
                'form': form,
            })
    else:
        _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
        form = ProfilePersonalInfoToolUserForm(instance=_toolUser,request=request)

    return render(request, 'toolapp/profile.html', {
        'form': form,
    })


class profile_view(generic.DetailView):
    template_name = 'toolapp/profile_view.html'
    model = User 
    context_object_name='user'   
    def get_object(self):
        return self.request.user


@login_required
def profile_preferences(request):
    if request.method == 'POST':        
        _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
        form = ProfilePreferencesToolUserForm(request.POST, instance=_toolUser)        
        if form.is_valid():
            messages.success(request, 'Your changes have been successfully saved') 
            newUser = form.save(commit=False)                        
            newUser.save()
            
            return render(request, 'toolapp/profile_preferences.html', {
                'form': form,
            })
    else:
        _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
        form = ProfilePreferencesToolUserForm(instance=_toolUser)

    return render(request, 'toolapp/profile_preferences.html', {
        'form': form,
    })

@login_required
def tools(request):

    search = request.GET.get('search') 
    sort = request.GET.get('sort')
    page = request.GET.get('page') 
    layout = getLayout(request,'client_tool_layout',default='cols')  

    tool_list = Tool.objects.filter(~Q(owner = request.user.tooluser)).exclude(status=Tool.ToolStatus.Deactivated.value)
    tool_list = filterToolsBySearch(search,tool_list)
    tool_list = orderToolsBy(sort,tool_list)
    tool_list = [x for x in tool_list if x.available()]
    tool_list = [x for x in tool_list if x.get_sharezone() == request.user.tooluser.get_sharezone()]
    tool_list = getToolPage(page=page, tool_list=tool_list)


    context = {
        'tool_list': tool_list,
        'can_borrow':True,
        'search':search,
        'layout_type':'client_tool_layout',
        'layout':layout,
        'sort':sort,
        'title': "<strong>Available Tools</strong><br><small>ShareZone " + str(request.user.tooluser.get_sharezone()) + "</small>"
    }

    return render(request, 'toolapp/tools.html', context)

@login_required
def my_tools(request):

    search = request.GET.get('search') 
    sort = request.GET.get('sort')
    page = request.GET.get('page') 
    layout = getLayout(request,'admin_tool_layout',default='list')  

    tool_list = Tool.objects.filter(owner=request.user.tooluser)
    tool_list = filterToolsBySearch(search,tool_list)
    tool_list = orderToolsBy(sort,tool_list)
    tool_list = getToolPage(page=page, tool_list=tool_list)

    context = {
        'tool_list': tool_list, 
        'can_edit':True,
        'my_tools':True,
        'search':search,
        'layout_type':'admin_tool_layout',
        'layout':layout  ,
        'sort':sort,
        'title': "<strong>My Tools</strong><br><small>ShareZone " + str(request.user.tooluser.get_sharezone()) + "</small>"

    }
    
    return render(request, 'toolapp/my-tools.html', context)


def orderToolsBy(sort,tool_list):

    if not sort:
        # default is order by id desc
        sort = "-id"

    return tool_list.order_by(sort)

def filterToolsBySearch(search,tool_list):

    if search:
        query_split = search.split()
        q = Q()
        for word in query_split:
            q |= Q(make__icontains = word)
            q |= Q(model__icontains = word)
        tool_list = tool_list.filter(q)
    else:
        search=''

    return tool_list

def getLayout(request,name,default):
    if name not in request.session:
        request.session[name] = default

    layout = request.GET.get(name,request.session[name])
    request.session[name] = layout
    return layout

def getToolPage(page, tool_list):
    paginator = Paginator(tool_list, 16) # Show 16 tools per page
    try:
        tool_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tool_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tool_list = paginator.page(paginator.num_pages)
    return tool_list


@login_required
def tools_register(request):
    _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
    if request.method == 'POST':                
        form = RegisterToolForm(request.POST, request.FILES,request=request)        
        if form.is_valid():            
            newTool = form.save(commit=False)
            newTool.owner=_toolUser
            if 'picture' in request.FILES:
                newTool.picture = request.FILES['picture']

            sharingLoc=request.POST.get('sharing_location')
            if sharingLoc=='HOME':
                newTool.share(shareLocation=Tool.ShareLocationType.Home.value)                
            elif sharingLoc!='':                 
                _communityShed=CommunityShed.objects.get(id=sharingLoc)
                newTool.share(shareLocation=Tool.ShareLocationType.CommunityShed.value,communityShed=_communityShed )                
            elif sharingLoc=='':
                newTool.share(shareLocation=Tool.ShareLocationType.Dont_Shared.value)
                
            newTool.save()
            return render(request, 'toolapp/tools_register_completed.html', {
                'form': form,
            })
    else:
        # TODO: instead of toolTemp use initial={} see tools_borrow view
        toolTemp = Tool(pickupArrangement=_toolUser.defaultPickupArrangement)
        form = RegisterToolForm(instance=toolTemp, request=request)

    return render(request, 'toolapp/tools_register.html', {
        'form': form,
    })

@login_required
def community_shed_create(request):
    if request.method == 'POST': 
        form = CreateCommunityShedForm(request.POST)
        if form.is_valid():            
            newCommunityShed = form.save(commit=False)
            newCommunityShed.coordinator = request.user.tooluser #set the coordinator as the current loggedin user
            newCommunityShed.save()
            return redirect('/community-shed/created')    
    else:
        form = CreateCommunityShedForm()

    return render(request, 'toolapp/community_shed_create.html', {
        'form':form, 'tooluser': request.user.tooluser
    })

@login_required
def stats(request):
    lend_stats = ToolStatistics.getMostActiveLenders(request.user.tooluser.get_sharezone())
    borrow_stats = ToolStatistics.getMostActiveBorrowers(request.user.tooluser.get_sharezone())
    tool_stats = ToolStatistics.getMostUsedTools(request.user.tooluser.get_sharezone())
    recent_tools = ToolStatistics.getMostRecentlyUsedTools(request.user.tooluser.get_sharezone())
    return render(request, 'toolapp/stats.html', {'borrow_stats': borrow_stats, 'lend_stats': lend_stats,
                                                 'tool_stats': tool_stats,  'recent_tools': recent_tools})

@login_required
def community_shed_created(request):
    return render(request, 'toolapp/community_shed_created.html')

@login_required
def community_shed_mylist(request):
    cs_list = CommunityShed.objects.filter(coordinator=request.user.tooluser)
    return render(request, 'toolapp/community_shed_mylist.html',{'cs_list':cs_list})

@login_required
def tools_community_shed(request, community_shed_id):
    communityShed = get_object_or_404(CommunityShed, id=community_shed_id)
    search = request.GET.get('search') 
    page = request.GET.get('page') 
    sort = request.GET.get('sort') 
    layout = getLayout(request,'admin_tool_layout',default='list')

    tool_list = communityShed.getTools()#Tool.objects.filter(owner=request.user.tooluser)
    tool_list = filterToolsBySearch(search,tool_list)
    tool_list = orderToolsBy(sort,tool_list)
    tool_list = getToolPage(page=page, tool_list=tool_list)

    context = {
        'tool_list': tool_list, 
        'can_edit':True,
        'my_tools':True,
        'search':search,
        'layout_type':'admin_tool_layout',
        'layout':layout,
        'sort':sort,
        'communityshed':communityShed,
        'title': "<strong>My Community Shed</strong><br><small>" + communityShed.name + "</small>"
    }
    
    return render(request, 'toolapp/tools_community_shed.html', context)    

@login_required
def tools_register_completed(request):
    return render(request, 'toolapp/tools_register_completed.html')


@login_required
def tools_borrow(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)

    has_requested_tool = request.user.tooluser.has_requested_tool(tool)

    if request.method == 'POST': 
        form = BorrowRequestForm(request.POST)
        if form.is_valid():            
            newBorrowRequest = form.save(commit=False)

            if not newBorrowRequest.validate_dates():
                return redirect("/tools/"+str(tool.id)+"/borrow?msg=invalid-date")

            if newBorrowRequest.tool.isInCommunityShed():
                newBorrowRequest.approve("")
                newBorrowRequest.save()
                return redirect('/my-reservations?msg=approved')   
            newBorrowRequest.save()
            return redirect('/my-reservations?msg=requested')    
    else:
        form = BorrowRequestForm(initial={
        'tool':tool,
        'borrower':request.user.tooluser # set the borrower to the current request tool user
    });

    #disabled_dates = '21 11 2014,22 11 2014,27 11 2014';
    disabled_dates = tool.get_disabled_dates();

    return render(request, 'toolapp/tools_borrow.html', {
        'disabled_dates':disabled_dates,
        'has_requested_tool':has_requested_tool,
        'tool':tool,
        'form':form,
        'msg':request.GET.get('msg')
    })


@login_required
def tools_blackout_dates(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)

    has_requested_tool = request.user.tooluser.has_requested_tool(tool)

    if request.method == 'POST': 
        form = forms.BlackOutDateForm(request.POST)
        if form.is_valid():            
            newBorrowRequest = form.save(commit=False)

            if not newBorrowRequest.validate_dates():
                return redirect("/tools/"+str(tool.id)+"/blackout_dates?msg=invalid-date")

            newBorrowRequest.reserve();#this marks the reservation as a black out date
            newBorrowRequest.save()
            return redirect('/my-reservations?msg=reserved')    
    else:
        form = forms.BlackOutDateForm(initial={
        'tool':tool,
        'borrower':request.user.tooluser # set the borrower to the current request tool user
    });

    #disabled_dates = '21 11 2014,22 11 2014,27 11 2014';
    disabled_dates = tool.get_disabled_dates();

    return render(request, 'toolapp/tools_blackout_dates.html', {
        'disabled_dates':disabled_dates,
        'has_requested_tool':has_requested_tool,
        'tool':tool,
        'form':form,
        'msg':request.GET.get('msg')
    })


@login_required
def tools_borrow_completed(request):
    return render(request, 'toolapp/tools_borrow_completed.html')


@login_required
def tools_availability(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)

    return render(request, 'toolapp/tools_availability.html', {
        'tool':tool,
        'approved_reservations':tool.getReservationsForAvailability(),
        'today':str(timezone.now()),
        'usecalendar':True,
    })

@login_required
def borrow_requests(request):

    approve_form = forms.ApproveBorrowRequestForm()
    reject_form = forms.RejectBorrowRequestForm()

    return render(request, 'toolapp/borrow_requests.html',{
        'msg':request.GET.get('msg'),
        'approve_form':approve_form,
        'reject_form':reject_form,
        'waiting_requests':request.user.tooluser.borrow_requests_waiting(),
        'approved_requests':request.user.tooluser.borrow_requests_approved(),
        'rejected_requests':request.user.tooluser.borrow_requests_rejected(),
        'finished_requests':request.user.tooluser.borrow_requests_finished(),
        })

@login_required
def borrow_request_approve(request):
    borrow_request_id = request.POST.get("borrow_request_id")
    borrow_request = get_object_or_404(models.Reservation, id=borrow_request_id)
    borrow_request.approve(request.POST.get('message'))
    send_mail('Tool request approved', request.POST.get('message'), borrow_request.tool.owner.user.email,
    [borrow_request.borrower.user.email], fail_silently=False)
    borrow_request.save()
    return redirect('/borrow-requests?msg=approved')


@login_required
def borrow_request_finish(request):
    borrow_request_id = request.POST.get("borrow_request_id")
    borrow_request = get_object_or_404(models.Reservation, id=borrow_request_id)
    borrow_request.finish()
    borrow_request.save()
    return redirect('/borrow-requests?msg=returned')

@login_required
def borrow_request_reject(request):
    borrow_request_id = request.POST.get("borrow_request_id")
    borrow_request = get_object_or_404(models.Reservation, id=borrow_request_id)
    borrow_request.reject(request.POST.get('message'))
    send_mail('Tool request rejected', request.POST.get('message'), borrow_request.tool.owner.user.email,
    [borrow_request.borrower.user.email], fail_silently=False)
    borrow_request.save()
    return redirect('/borrow-requests?msg=rejected')

@login_required
def my_reservations(request):
    return render(request, 'toolapp/my_reservations.html',{
        'msg':request.GET.get('msg'),
        'reservations':request.user.tooluser.reservations()
    })

@login_required
def tools_edit(request, tool_id): 
    _toolUser = get_object_or_404(ToolUser, user_id=request.user.id)
    tool = get_object_or_404(Tool, id=tool_id)
    request.idTool=tool.id
    if tool.owner != _toolUser:
        if tool.communityShed!=None:
            if tool.communityShed.coordinator!=_toolUser:
                return redirect("/")
        else:
            return redirect("/")
    if request.method == 'POST':                
        form = RegisterToolForm(request.POST, request.FILES,instance=tool,request=request)        
        if form.is_valid():             
            newTool = form.save(commit=False)            
            if 'picture' in request.FILES:
                newTool.picture = request.FILES['picture']

            sharingLoc=request.POST.get('sharing_location')
            if sharingLoc=='HOME':
                newTool.share(shareLocation=Tool.ShareLocationType.Home.value)                
            elif sharingLoc!='' and sharingLoc!='None':                 
                _communityShed=CommunityShed.objects.get(id=sharingLoc)
                newTool.share(shareLocation=Tool.ShareLocationType.CommunityShed.value,communityShed=_communityShed )                
            elif sharingLoc=='':
                newTool.share(shareLocation=Tool.ShareLocationType.Dont_Shared.value)

            confirmed=request.POST.get('confirmed')           
            statusChanged=request.POST.get('statusChanged') 
            if confirmed=='yes':
                print(newTool.status)
                print(tool.status)
                if tool.confirmationNeeded and str(newTool.status) =='1' and statusChanged=="yes":                    
                    tool.notifyBorrowers()
                newTool.save()
                return render(request, 'toolapp/tools_edit_completed.html', {
                    'form': form,
                })
    else:
        sharingLoc=''
        if tool.type == str(Tool.ShareLocationType.Home.value):
            sharingLoc='HOME'
        elif tool.type == str(Tool.ShareLocationType.Dont_Shared.value):
            sharingLoc=''
        elif tool.type == str(Tool.ShareLocationType.CommunityShed.value):
            sharingLoc=str(tool.communityShed.id)
        form = RegisterToolForm(instance=tool,request=request,initial={'sharing_location':sharingLoc})
    return render(request, 'toolapp/tools_edit.html', {
        'form': form,'tool':tool
    })

@login_required
def detail(request, user_id):
    user = get_object_or_404(ToolUser, pk=user_id)
    return render(request, 'toolapp/detail.html', {'user': user})



class UserRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    def register(self, request, **cleaned_data):
        user = super(UserRegistrationView, self).register(request, **cleaned_data)
        #cleaned_data['user'] = user
        tool_user = ToolUser()
        for (i, item) in cleaned_data.items():
            setattr(tool_user,i,item)
            if i == 'zipcode':
                if len(ShareZone.objects.filter(zipcode=item)) == 0:
                    share_zone = ShareZone(zipcode=item)
                    share_zone.save()

        tool_user.user = user
        tool_user.save()
        return user
