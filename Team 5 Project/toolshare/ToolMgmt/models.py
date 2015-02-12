from django.db import models
from UserAuth.models import UserProfile
from Sharing.models import ShareZone, Shed

class ToolCategory(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)

    def __str__(self):
        return self.name

class ToolStatus(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    description = models.CharField(verbose_name="Description", max_length=200)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(ToolCategory, related_name='category')
    status = models.ForeignKey(ToolStatus, related_name='status')
    owner = models.ForeignKey(UserProfile, related_name='owner', null=True)
    image = models.ImageField(upload_to="images/tools/", blank=True, null=True)
    identifier = models.CharField(verbose_name="Identifier", blank=True, null=True, max_length=200)
    shed = models.ForeignKey(Shed, related_name='tools', null = True, blank = True)
    in_shed = models.BooleanField(default = False)

    def __str__(self):
        return self.name
