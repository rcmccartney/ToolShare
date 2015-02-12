from django.contrib import admin

# Register your models here.
from ToolMgmt.models import Tool, ToolCategory, ToolStatus


admin.site.register(Tool)
admin.site.register(ToolCategory)
admin.site.register(ToolStatus)