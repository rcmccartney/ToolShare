from django.db import models

class ShareZone(models.Model):   
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    zipcode = models.IntegerField(verbose_name ="Zipcode")
    
    def __str__(self):
        return self.name

class Shed(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    description = models.CharField(verbose_name="Description", max_length=200)
    sharezone = models.ForeignKey(ShareZone, related_name = 'sheds',null =True,blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    coordinators = models.ManyToManyField('UserAuth.UserProfile', related_name = 'sheds', null =True,blank = True)

    def iscoordinator(self,profile):
        if profile in self.coordinators.all():
            return True
        else:
            return False

    def __str__(self):
        return self.name

class Arrangement(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_arrangement = models.CharField(verbose_name="Arrangement", max_length=200)
    borrower = models.ForeignKey('UserAuth.UserProfile',related_name='asked_requests')
    lender = models.ForeignKey('UserAuth.UserProfile',related_name='recieved_requests')
    tool = models.ForeignKey('ToolMgmt.Tool',related_name='tools', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "borrower: <"+ str(self.borrower) + "> lender: <" + str(self.lender) + ">"

class Sharing(Arrangement): 
    comment = models.CharField(verbose_name="Comment about the sharing", max_length=200)
    returned = models.BooleanField(default=False)

class Request(Arrangement):
    msg = models.CharField(verbose_name="Arrangement message for requesting", max_length=200)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return "<"+ str(self.borrower) + "> has requested <" + str(self.lender) + "> a <" + str(self.tool) + ">"
