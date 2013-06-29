from django import forms
from mylist.models import CheckList


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ['title', 'start_at', 'public']