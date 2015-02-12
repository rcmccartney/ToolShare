from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USPostalCodeField
from Sharing.models import ShareZone
# Create your models here.

class UserProfile(models.Model):
    NOREMINDER = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    SOMETIMES = 4

    REMINDER_CHOICES = ( 
        (NOREMINDER, 'Dont notify'),
        (DAILY, 'Daily'),
        (WEEKLY, 'In a Week'),
        (SOMETIMES, 'Sometimes'), # extensible.
    ) 
    user = models.OneToOneField(User, related_name='profile')
    add_line1 = models.CharField(verbose_name="Address Line 1",max_length = 100)
    add_line2 = models.CharField(verbose_name="Address Line 2",max_length = 100)
    state = USStateField(choices = STATE_CHOICES)
    reminder_preferences =models.IntegerField(choices = REMINDER_CHOICES) 
    pickup_loc = models.CharField(verbose_name="Pickup arrangements",max_length = 100)
    profile_photo = models.ImageField(upload_to="images/users/", blank=True, null=True)
    sharezone = models.ForeignKey(ShareZone, related_name = 'members',null = True,blank = True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass
        super(UserProfile, self).save(*args, **kwargs) 
