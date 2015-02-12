from registration.forms import RegistrationForm
from django.forms import ModelForm,CharField,Textarea, ChoiceField,HiddenInput,TypedChoiceField
from toolapp.models import ToolUser,Tool,Address,Reservation,CommunityShed
from localflavor.us.forms import USZipCodeField
from django.contrib.auth.models import User
import pprint
import django.forms as forms


class UserRegistrationForm(ModelForm):
  zipcode = USZipCodeField()
  defaultPickupArrangement=CharField(required=False,widget=Textarea(),label="Default Pickup Arrangement")
  address2 = CharField(required=False)
  class Meta:
    model = ToolUser
    exclude = ['user']
    # labels = {
    #     'defaultPickupArrangement': 'Default Pickup Arrangement',
    # }
RegistrationForm.base_fields.update(UserRegistrationForm.base_fields)

class RegisterToolForm(ModelForm):    
    sharing_location= ChoiceField(choices=(), required=False)    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super(RegisterToolForm, self).__init__(*args, **kwargs)        
        CHOICES = (
        ('','Don\'t share'),
        ('HOME', 'Home'),
        ('None', '-------------Community Sheds-------------')
        )
        _toolUser = ToolUser.objects.get(user__id=self.request.user.id)
        choicesComShed = tuple([(p.id,p.name) for p in CommunityShed.objects.filter(coordinator__zipcode=_toolUser.zipcode)]) 
        self.fields['sharing_location'].choices=CHOICES+choicesComShed
    def clean_sharing_location(self):
        data = self.cleaned_data["sharing_location"]
        if data=='None':
            raise forms.ValidationError("You must select a valid location.")
        if hasattr(self.request,'idTool') and self.request.idTool!=-1:
            _tool=Tool.objects.get(id=self.request.idTool)
            if not _tool.canChangeLocation():
                errormsj="You cannot change this tool's location, because it has some reservations that have not been finished yet."
                if (data==''):
                    raise forms.ValidationError(errormsj)
                if (data!='HOME' and not hasattr(_tool.communityShed,'id')):
                    raise forms.ValidationError(errormsj)
                if hasattr(_tool.communityShed,'id') and data!=str(_tool.communityShed.id):
                    raise forms.ValidationError(errormsj)
        return data  
    class Meta:        
        model = Tool
        exclude = ['owner','location','type','communityShed']

class ProfilePreferencesToolUserForm(ModelForm):
    class Meta:
        model = ToolUser        
        fields = ('emailReminderFrequency','defaultPickupArrangement')

class CreateCommunityShedForm(ModelForm):
    class Meta:
        model = CommunityShed   
        exclude = ['coordinator']   


class BorrowRequestForm(ModelForm): 
    class Meta:
        model = Reservation
        exclude = ['status','statusMessage']
        widgets = {
            # hide the tool field, the user can't change this
            'tool': HiddenInput(),
            'borrower':HiddenInput(),
            'fromDate':forms.TextInput(attrs={'class':"datepicker-from","autocomplete":"off"}),
            'toDate':forms.TextInput(attrs={'class':"datepicker-to","disabled":"disabled","autocomplete":"off"})
        }
        labels = {
            'requestMessage': "Request Message",
            "fromDate": "From",
            "toDate": "To"
        }

class BlackOutDateForm(ModelForm): 
    class Meta:
        model = Reservation
        exclude = ['status','statusMessage','requestMessage']
        widgets = {
            # hide the tool field, the user can't change this
            'tool': HiddenInput(),
            'borrower':HiddenInput(),
            'fromDate':forms.TextInput(attrs={'class':"datepicker-from","autocomplete":"off"}),
            'toDate':forms.TextInput(attrs={'class':"datepicker-to","disabled":"disabled","autocomplete":"off"})
        }
        labels = {
            'requestMessage': "Request Message",
            "fromDate": "From",
            "toDate": "To"
        }


class ProfilePersonalInfoToolUserForm(ModelForm):
    zipcode = USZipCodeField()
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProfilePersonalInfoToolUserForm, self).__init__(*args, **kwargs) 
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        _toolUser = ToolUser.objects.get(user__id=self.request.user.id)
        if not _toolUser.canChangeZipcode() and data!=_toolUser.zipcode:
            errormsj="You cannot change zipcode, because you have some reservations that have not been finished yet."
            raise forms.ValidationError(errormsj)
        return data  
    class Meta:
        model = ToolUser
        exclude = ['id','user','emailReminderFrequency','defaultPickupArrangement']


class CustomRegistrationForm(RegistrationForm):
    pass

class ApproveBorrowRequestForm(forms.Form):
    borrow_request_id = forms.CharField(widget=HiddenInput())
    message = forms.CharField(label='Message',widget=Textarea(attrs={'rows':4}))

class RejectBorrowRequestForm(forms.Form):
    borrow_request_id = forms.CharField(widget=HiddenInput())
    message = forms.CharField(label='Message (Required)',widget=Textarea(attrs={'rows':4}))

