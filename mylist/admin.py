from django.contrib import admin
from mylist.models import CheckList, Task

class CheckListAdmin(admin.ModelAdmin):
    pass

admin.site.register(CheckList, CheckListAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task, TaskAdmin)
