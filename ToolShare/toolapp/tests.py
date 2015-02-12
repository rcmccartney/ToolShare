from django.test import TestCase

from toolapp.models import ToolUser, Tool, Address,CommunityShed
from toolapp.forms import RegisterToolForm,CustomRegistrationForm, ProfilePersonalInfoToolUserForm, ProfilePersonalInfoToolUserForm, ProfilePreferencesToolUserForm,BorrowRequestForm,CreateCommunityShedForm,UserRegistrationForm
from django.contrib.auth.models import Permission,User

# Create your tests here.
_User = User(password="123",username="test_user", email="ivantm24@gmail.com",is_active=1)
_toolUser=ToolUser(user=_User,address1="add",address2="add",city="NY",state="NY",zipcode="14623",country="USA",phoneNumber="2342341234",emailReminderFrequency=ToolUser.EmailFrequency.Daily.value,defaultPickupArrangement="knock")

class CreateCommunityShedTest(TestCase):

	def testShedCreation(self):
		shed=CommunityShed(name="ivan",coordinator=_toolUser,address1="123",address2="")
		form= CreateCommunityShedForm({'name':shed.name,'coordinator':shed.coordinator,'address1':shed.address1})
		self.assertEquals(form.is_valid(),True)

	def testShedCreation_emptyAdd1(self):
		shed=CommunityShed(name="ivan",coordinator=_toolUser,address1="",address2="")
		form= CreateCommunityShedForm({'name':shed.name,'coordinator':shed.coordinator,'address1':shed.address1})
		self.assertEquals(form.is_valid(),False)

class UserRegistrationTest(TestCase):
	_User = User(password="123",username="test_user", email="ivantm24@gmail.com",is_active=1)
	def testUserRegistration_1(self):
		form= UserRegistrationForm({'user':_toolUser.user,'address1':_toolUser.address1,'city':_toolUser.city,'state':_toolUser.state,'zipcode':_toolUser.zipcode,'country':_toolUser.country,'phoneNumber':_toolUser.phoneNumber,'emailReminderFrequency':_toolUser.emailReminderFrequency,'defaultPickupArrangement':_toolUser.defaultPickupArrangement,'address2':_toolUser.address2})
		self.assertEquals(form.is_valid(),True)

	def testUserRegistration_wrongphonenumber_3(self):
		user3=ToolUser(user=self._User,address1="add",address2="",city="r",state="NY",zipcode="14623",country="USA",phoneNumber="111222",emailReminderFrequency=ToolUser.EmailFrequency.Daily.value,defaultPickupArrangement="knock")
		form= UserRegistrationForm({'user':user3.user,'address1':user3.address1,'city':user3.city,'state':user3.state,'zipcode':user3.zipcode,'country':user3.country,'phoneNumber':user3.phoneNumber,'emailReminderFrequency':user3.emailReminderFrequency,'defaultPickupArrangement':user3.defaultPickupArrangement,'address2':user3.address2})
		self.assertEquals(form.is_valid(),False)

	# def testUserRegistration_existingusername_4(self):


	# def testUserRegistration_wrongemailformat_5(self):
		

	def testUserRegistration_emptyfrequencyinfo_6(self):
		user2=ToolUser(user=self._User,address1="add",address2="",city="r",state="NY",zipcode="14623",country="USA",phoneNumber="1112223333",emailReminderFrequency="",defaultPickupArrangement="knock")
		form= UserRegistrationForm({'user':user2.user,'address1':user2.address1,'city':user2.city,'state':user2.state,'zipcode':user2.zipcode,'country':user2.country,'phoneNumber':user2.phoneNumber,'emailReminderFrequency':user2.emailReminderFrequency,'defaultPickupArrangement':user2.defaultPickupArrangement,'address2':user2.address2})
		self.assertEquals(form.is_valid(),False)

	def testUserRegistration_emptycity_7(self):
		user1=ToolUser(user=self._User,address1="add",address2="",city="",state="NY",zipcode="14623",country="USA",phoneNumber="1112223333",emailReminderFrequency=ToolUser.EmailFrequency.Daily.value,defaultPickupArrangement="knock")
		form= UserRegistrationForm({'user':user1.user,'address1':user1.address1,'city':user1.city,'state':user1.state,'zipcode':user1.zipcode,'country':user1.country,'phoneNumber':user1.phoneNumber,'emailReminderFrequency':user1.emailReminderFrequency,'defaultPickupArrangement':user1.defaultPickupArrangement,'address2':user1.address2})
		self.assertEquals(form.is_valid(),False)


	

# class RegisterToolTest(TestCase):
# 	_User = User(password="123",username="test_user", email="ivantm24@gmail.com",is_active=1)
# 	_toolUser=ToolUser(user=_User,address1="add",address2="add",city="NY",state="NY",zipcode="14623",country="USA",phoneNumber="2342341234",emailReminderFrequency=ToolUser.EmailFrequency.Daily.value,defaultPickupArrangement="knock")
# 	_shareLocation=ShareLocation(type=ShareLocation.ShareLocationType.choice())

#     def testToolRegistration(self):
#     	tool=Tool(owner=self._toolUser,make="111",model="123",description="222",status=Tool.ToolStatus.choices(),location=self._shareLocation,pickupArrangement=self._toolUser.defaultPickupArrangement,pictur="",)
#     	form=RegisterToolForm({'choicesComShed'=,'sharing_location'=tool.location})
#     	self.assertEquals(form.is_valid(),False)