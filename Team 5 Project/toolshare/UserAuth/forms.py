from django import forms
from django.contrib.auth.models import User
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Password',max_length=16)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label='Confirm Password',max_length=16)
    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    class Meta:
        model= User
        fields= ('username','email','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    zipcode = USZipCodeField()
    class Meta:
        model = UserProfile
        fields= ('add_line1','add_line2','zipcode','reminder_preferences','pickup_loc','profile_photo')
        # fields= ('add_line1','add_line2','reminder_preferences','pickup_loc','profile_photo')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('email', 'first_name','last_name')
        
class UserPreferences(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('reminder_preferences','pickup_loc')
