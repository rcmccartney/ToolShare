from ToolMgmt.models import Tool 
from UserAuth.models import UserProfile

#Evaluates if the owner of the is given user or not
def Is_Owner(profile,tool):
    if (tool.owner == profile):
        return True
    else:
        return False
