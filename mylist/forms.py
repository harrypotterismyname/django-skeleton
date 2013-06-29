from django import forms
from mylist.models import CheckList, Task


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ['title', 'start_at', 'public']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['is_checked']