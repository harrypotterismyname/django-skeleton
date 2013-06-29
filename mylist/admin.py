from django.contrib import admin
from mylist.models import *

class CheckListAdmin(admin.ModelAdmin):
    pass

admin.site.register(CheckList, CheckListAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task, TaskAdmin)

class UserCheckListAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserCheckList, UserCheckListAdmin)