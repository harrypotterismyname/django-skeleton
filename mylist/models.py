from django.db import models
from django.utils.translation import ugettext_lazy as _
from userena.utils import user_model_label


class CheckList(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024, blank=True)
    slug = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024, blank=True)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    id_check_list = models.ForeignKey(CheckList, null=True)