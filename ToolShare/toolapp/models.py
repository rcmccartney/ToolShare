from django.db import models
from django.contrib.auth.models import User
from django.db.utils import ConnectionDoesNotExist
from localflavor.us.models import USStateField,PhoneNumberField
import os # this is for ImageField
import datetime
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail

from toolapp.choiceenum import ChoiceEnum


class ToolUser(models.Model):
    class EmailFrequency(ChoiceEnum):
        Daily=0
        Weekly=1
        Monthly=2
        Never=3

    user = models.OneToOneField(User)
    # I know this should be in it's own Address class..., but It's harder to make ModelForm work att Carlos
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = USStateField()
    zipcode = models.IntegerField(default=0)
    country = models.CharField(max_length=3,
                                      choices=(
                                          ('USA', 'United States'),
                                      ),
                                      default='USA')

    phoneNumber = PhoneNumberField("Phone")
    emailReminderFrequency = models.CharField("Email Reminder Frequency",max_length=1, choices=EmailFrequency.choices())
    defaultPickupArrangement = models.TextField("Default Pickup Arrangement")

    def __str__(self):
        return self.user.__str__()

    def joined_recently(self):
        return self.date_joined >= timezone.now() - datetime.timedelta(days=30)

    def borrow_requests(self):
        return Reservation.objects.filter(tool__owner=self).exclude(tool__missing=True)

    def borrow_requests_waiting(self):
        return self.borrow_requests().filter(status=BorrowRequestStatus.Waiting).exclude(tool__status=Tool.ToolStatus.Deactivated.value).order_by('-updatedAt')

    def borrow_requests_approved(self):
        return self.borrow_requests().filter(status=BorrowRequestStatus.Approved).exclude(tool__status=Tool.ToolStatus.Deactivated.value).order_by('-updatedAt')

    def borrow_requests_rejected(self):
        return self.borrow_requests().filter(status=BorrowRequestStatus.Rejected).exclude(tool__status=Tool.ToolStatus.Deactivated.value).order_by('-updatedAt')

    def borrow_requests_finished(self):
        return self.borrow_requests().filter(status=BorrowRequestStatus.Finished).exclude(tool__status=Tool.ToolStatus.Deactivated.value).order_by('-updatedAt')

    def reservations(self):
        return Reservation.objects.filter(borrower=self).exclude(tool__status=Tool.ToolStatus.Deactivated.value).exclude(tool__missing=True).order_by('-createdAt');

    def has_requested_tool(self, tool):
        ''' Returns true if user has requested the Tool already'''
        return len(Reservation.objects.filter(tool=tool,borrower=self,status=BorrowRequestStatus.Waiting))>0

    def get_sharezone(self):
        try:
            val = ShareZone.objects.get(zipcode=self.zipcode).pk
        except:
            val = -1  #this is for old models without a sharezone
        return val

    def canChangeZipcode(self):
        _reservation=Reservation.objects.filter(tool__owner=self).exclude(status=BorrowRequestStatus.Finished).exclude(status=BorrowRequestStatus.Rejected)
        _communityShed= CommunityShed.objects.filter(coordinator=self)        
        if _reservation.count()>0 or _communityShed.count()>0:
            return False
        return True

    joined_recently.admin_order_field = 'date_joined'
    joined_recently.boolean = True
    joined_recently.short_description = 'Joined recently?'



def get_image_path(instance, filename):
    return os.path.join('static/photos', str(instance.id), filename)


class Address(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField()
    zipcode = models.IntegerField(default=0)
    country = models.CharField(max_length=50)
    def __str__(self):
        s="\n"
        return self.address1 + s + self.address2 + s + self.city + "," + self.state + s + str(self.zipcode) + s + self.country



class CommunityShed(models.Model):
    name = models.CharField(max_length=50)
    coordinator = models.ForeignKey(ToolUser)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)

    def addTool(self):
        pass
    def removeTool(self):
        pass
    def getTools(self):
        return Tool.objects.filter(communityShed__id=self.id)

class Category(models.Model):
    description = models.CharField(max_length=400,primary_key=True)
    def __str__(self):
        return self.description
        
class Tool(models.Model):
    class ToolStatus(ChoiceEnum):
        Activated=0
        Deactivated=1
    class ShareLocationType(ChoiceEnum):
        Home=0
        CommunityShed=1    
        Dont_Shared=2
    owner = models.ForeignKey(ToolUser, null=True)
    missing = models.BooleanField(default=False)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=400, unique=True)
    category = models.ForeignKey(Category, null=True)
    status = models.CharField(max_length=1, choices=ToolStatus.choices())
    special_instructions = models.TextField("Special Instructions",max_length=100, null=True, blank=True)
    
    
    type = models.CharField(max_length=1, choices=ShareLocationType.choices())
    communityShed = models.ForeignKey(CommunityShed, blank=True, null=True)
    pickupArrangement = models.TextField("Pickup Arrangement")
    picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.make + " " + self.model + ": " + self.description

    def available(self):       
        return str(self.type)!=str(Tool.ShareLocationType.Dont_Shared.value) and self.missing==False

    def share(self,shareLocation, communityShed=None):
        self.type=shareLocation
        if shareLocation==Tool.ShareLocationType.CommunityShed.value:
            self.communityShed=communityShed
        else:
            self.communityShed=None
    def borrow(self):
        pass
    def isInCommunityShed(self):
        if self.type==str(Tool.ShareLocationType.CommunityShed.value):
            return True
        return False

    def canBeBorrowed(self):
        pass
    def getLocationText(self):
        if self.type==str(Tool.ShareLocationType.CommunityShed.value):
            return self.communityShed.name
        elif self.type==str(Tool.ShareLocationType.Home.value):
            return self.owner.user.username+'\'s home'
        else:
            return 'None'
    def getLocationLabel(self):
        if self.type==str(Tool.ShareLocationType.CommunityShed.value):
            return 'label-warning'
        elif self.type==str(Tool.ShareLocationType.Home.value):
            return 'label-primary'
        else:
            return 'label-default'

    def address1(self):
        if self.type==str(Tool.ShareLocationType.CommunityShed.value):
            return self.communityShed.coordinator.address1
        elif self.type==str(Tool.ShareLocationType.Home.value):
            return self.owner.address1
        else:
            return ''        
    
    def address2(self):
        if self.type==str(Tool.ShareLocationType.CommunityShed.value):
            return self.communityShed.coordinator.address2
        elif self.type==str(Tool.ShareLocationType.Home.value):
            return self.owner.address2
        else:
            return ''                


    def get_picture_or_default(self):
        if (self.picture):
            return '/' + str(self.picture)
        return '/static/img/no-image.jpg'

    def get_sharezone(self):
        try:
            val = ShareZone.objects.get(zipcode=self.owner.zipcode).pk
        except:
            val = -1  #this is for old models without a sharezone
        return val
    def canChangeLocation(self):
        _reservation=Reservation.objects.filter(tool__id=self.id).exclude(status=BorrowRequestStatus.Finished).exclude(status=BorrowRequestStatus.Rejected).exclude(status=BorrowRequestStatus.Blackout_date)
        if _reservation.count()>0:
            return False
        return True
    def getReservations(self):
        _reservation=Reservation.objects.filter(tool__id=self.id)
        return _reservation
    def getReservationsForAvailability(self):
        _reservation=self.getReservations()
        return _reservation.exclude(status=BorrowRequestStatus.Rejected).exclude(status=BorrowRequestStatus.Finished)
    
    def get_disabled_dates(self):

        reservations = self.getReservationsForAvailability()
        disabled_dates = []
        for reservation in reservations:
            date = reservation.fromDate
            while date < reservation.toDate:
                disabled_dates.append(date.strftime("%d %m %Y"))
                date = date + datetime.timedelta(days=1)
        
            
            disabled_dates.append(date.strftime("%d %m %Y"))

        return ",".join(disabled_dates)
    def confirmationNeeded(self):#needs confirmation if tool deactivated and have future reservation that are not rejected
        today = datetime.datetime.now()

        _reservation= Reservation.objects.filter(tool__id=self.id,toDate__gte=today).exclude(status=BorrowRequestStatus.Finished).exclude(status=BorrowRequestStatus.Rejected)
        if _reservation.count()<=0:
            return False
        return True 
    def notifyBorrowers(self):
        today = datetime.datetime.now()
        sent = {}
        _reservation= Reservation.objects.filter(tool__id=self.id,toDate__gte=today).exclude(status=BorrowRequestStatus.Finished).exclude(status=BorrowRequestStatus.Rejected)
        for _res in _reservation:            
            if not _res.borrower.user.email in sent:
                send_mail('Tool deactivated', "Tool "+ str(self) +"was deactivated ", self.owner.user.email,[_res.borrower.user.email], fail_silently=False)
            sent[_res.borrower.user.email]=True



class ShareZone(models.Model):
    zipcode = models.IntegerField(default=0)


class BorrowRequestStatus:
    Waiting='0'
    Approved='1'
    Rejected='2'
    Finished='3'
    Blackout_date='4'

class Reservation(models.Model):

    requestMessage = models.CharField(max_length=500)
    tool = models.ForeignKey(Tool)
    borrower = models.ForeignKey(ToolUser)
    fromDate = models.DateTimeField()
    toDate = models.DateTimeField()
    status = models.CharField(max_length=1, choices=(
        (BorrowRequestStatus.Waiting, 'Waiting'),
        (BorrowRequestStatus.Approved, 'Approved'),
        (BorrowRequestStatus.Rejected, 'Rejected'),
        (BorrowRequestStatus.Finished, 'Finished'),
        (BorrowRequestStatus.Blackout_date, 'Blackout'),
        ),default=BorrowRequestStatus.Waiting)
    statusMessage = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.borrower) + ": " + self.status

    def get_row_class(self):
        if self.status == BorrowRequestStatus.Waiting:
            return 'info'

        if self.status == BorrowRequestStatus.Rejected:
            return 'danger'

        if self.status == BorrowRequestStatus.Approved:
            return 'success'

        if self.status == BorrowRequestStatus.Blackout_date:
            return 'info'

        return ''

    def get_status_style(self):
        if self.status == BorrowRequestStatus.Waiting:
            return 'color:#337ab7;font-weight:bold;'

        if self.status == BorrowRequestStatus.Rejected:
            return 'color:#d9534f;font-weight:bold;'

        if self.status == BorrowRequestStatus.Approved:
            return 'color:#5cb85c;font-weight:bold;'
        
        if self.status == BorrowRequestStatus.Blackout_date:
            return 'color:#5cb85c;font-weight:bold;'

        return ''

    def approve(self,message):
        self.status = BorrowRequestStatus.Approved
        self.statusMessage = message
        self.updatedAt=timezone.now()
    def reject(self,message):
        self.status = BorrowRequestStatus.Rejected
        self.statusMessage = message
        self.updatedAt=timezone.now()
    def finish(self):
        self.status = BorrowRequestStatus.Finished
        self.updatedAt=timezone.now()
    def reserve(self):
        self.status = BorrowRequestStatus.Blackout_date
        self.updatedAt=timezone.now()
    def canBeFinished(self):
        return self.toDate <= timezone.now()
    def strToDate(self):
        return str(self.toDate)
    def strFromDate(self):
        return str(self.fromDate)


    def validate_dates(self):

        if(self.fromDate.isoformat()>=self.toDate.isoformat()):
            return False

        date = self.fromDate
        while(date != self.toDate):
            reservations = self.tool.getReservationsForAvailability().filter(Q(fromDate=date) | Q(toDate=date))
            print(reservations)
            if(len(reservations)>0):
                return False
            date = date + datetime.timedelta(days=1)


        return True


    def title(self):
        _title=""
        if self.status==BorrowRequestStatus.Approved:
            _title=_title+"Approved"
        elif self.status==BorrowRequestStatus.Rejected:
            _title=_title+"Rejected"
        elif self.status==BorrowRequestStatus.Finished:
            _title=_title+"Finished"
        elif self.status==BorrowRequestStatus.Waiting:
            _title=_title+"Pending"
        _title=_title+" reservation"
        if self.status==BorrowRequestStatus.Blackout_date:
            _title = "Blackout Date"
        return _title

class ToolStatistics():

    def getMostActiveLenders(shzone):
        mydict = {}
        for res in Reservation.objects.all():
            try:
                if res.tool.get_sharezone() == shzone:
                    owner = res.tool.owner.user.username
                    if owner in mydict:
                        mydict[owner] += 1
                    else:
                        mydict[owner] = 1
            except:
                pass
        sortedUsers = sorted(mydict, key=mydict.get, reverse=True)
        i = len(sortedUsers)
        if i > 5:
            i = 5
        d = {}
        d["Other"] = 0
        for k in range(i, len(sortedUsers)):
            d["Other"] += mydict[sortedUsers[k]]
        for j in range(i):
            d[sortedUsers[j]] = mydict[sortedUsers[j]]
        return d

    def getMostActiveBorrowers(shzone):
        mydict = {}
        for res in Reservation.objects.all():
            try:
                if res.tool.get_sharezone() == shzone:
                    borrower = res.borrower.user.username
                    if borrower in mydict:
                        mydict[borrower] += 1
                    else:
                        mydict[borrower] = 1
            except:
                pass
        sortedUsers = sorted(mydict, key=mydict.get, reverse=True)
        i = len(sortedUsers)
        if i > 5:
            i = 5
        d = {}
        d["Other"] = 0
        for k in range(i, len(sortedUsers)):
            d["Other"] += mydict[sortedUsers[k]]
        for j in range(i):
            d[sortedUsers[j]] = mydict[sortedUsers[j]]
        return d

    def getMostUsedTools(shzone):
        mydict = {}
        for res in Reservation.objects.all():
            try:
                if res.tool.get_sharezone() == shzone:
                    tool = str(res.tool.make) + " " + str(res.tool.model)
                    if tool in mydict:
                        mydict[tool] += 1
                    else:
                        mydict[tool] = 1
            except:
                pass
        sortedTools = sorted(mydict, key=mydict.get, reverse=True)
        i = len(sortedTools)
        if i > 10:
            i = 10
        d = {}
        for j in range(i):
            # short names if necessary
            key = sortedTools[j]
            if len(key) > 15:
                key = sortedTools[j][:17] + ".."
            d[key] = mydict[sortedTools[j]]
        return d

    def getMostRecentlyUsedTools(shzone):
        recents = []
        for res in Reservation.objects.order_by('-fromDate'):
            if res.status == BorrowRequestStatus.Finished and res.tool.get_sharezone() == shzone:
                recents.append(res)
                if len(recents) >= 10:
                    break
        return recents
