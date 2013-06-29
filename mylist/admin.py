from django.contrib import admin
from mylist.models import CheckList, Task


class CheckListAdmin(admin.ModelAdmin):
    list_display = ('title', 'rate', 'owner', 'public')
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ('owner',)


class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Task, TaskAdmin)