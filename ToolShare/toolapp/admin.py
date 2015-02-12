from django.contrib import admin
from toolapp.models import ToolUser, Tool
import reversion

class ChoiceInline(admin.TabularInline):
    model = Tool
    extra = 1


class UserAdmin(reversion.VersionAdmin):
    fieldsets = [
        (None, {'fields': ['first_name', 'last_name', 'email']}),
        ('Date information', {'fields': ['date_joined'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id', 'first_name', 'last_name', 'joined_recently')
    list_filter = ['date_joined']
    search_fields = ['first_name', 'last_name', 'date_joined']


class ToolAdmin(reversion.VersionAdmin):
    fields = ['owner', 'make', 'model', 'description', 'status', 'pickupArrangement']

class ToolUserAdmin(reversion.VersionAdmin):
    pass


admin.site.register(ToolUser,ToolUserAdmin)
admin.site.register(Tool, ToolAdmin)
