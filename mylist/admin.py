from django.contrib import admin
from mylist.models import CheckList, Task, UserCheckList


class CheckListAdmin(admin.ModelAdmin):
    list_display = ('title', 'rate', 'owner', '')


class TaskAdmin(admin.ModelAdmin):
    pass


class UserCheckListAdmin(admin.ModelAdmin):
    pass


admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserCheckList, UserCheckListAdmin)