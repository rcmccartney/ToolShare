from django import forms
from django.contrib.auth.models import User
from Sharing.models import Shed
from UserAuth.models import UserProfile
from localflavor.us.forms import USZipCodeField
from localflavor.us.forms import USStateField
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions
import pdb
class ShedCreateForm(forms.ModelForm):
    class Meta:
        model = Shed
        fields = ('name','description')

class ShedEditForm(forms.ModelForm):
    coordinators = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Shed
        fields = ('name','description', 'coordinators')
