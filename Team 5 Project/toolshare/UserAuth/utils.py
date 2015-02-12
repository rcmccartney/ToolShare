from Sharing.models import ShareZone

#Helper Methods
def CreateAllocateZone(code):
    if not ShareZone.objects.filter(zipcode = code):
        NewZone = ShareZone(int(code))
        NewZone.name =  "ToolShare Zone " + str(code)
        NewZone.description = "Zipcode sharezone"
        NewZone.zipcode = code 
        NewZone.save()
        return NewZone
    else:
        OldZone = ShareZone.objects.get(zipcode = code) 
        return OldZone
