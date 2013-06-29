from django.db import models
from django.utils.translation import ugettext_lazy as _
from mylist.models import CheckList, Task

from userena.models import UserenaLanguageBaseProfile
from userena.utils import user_model_label


class Profile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(user_model_label,
                                unique=True,
                                verbose_name=_('User'),
                                related_name='profile')

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    website = models.URLField(_('Website'), blank=True)
    location = models.CharField(_('Location'), max_length=255, blank=True)
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    about = models.TextField(_('About'), blank=True, max_length=3000)

    def __unicode__(self):
        return "profile of %s" % self.user.username

    def clone_checklist(self, old_checklist):

        new_checklist = CheckList( title = old_checklist.title, owner = self.user )
        new_checklist.save()

        for task in old_checklist.tasks.filter( is_deleted = False):
            new_task = Task( title = task.title, check_list = new_checklist, due_date = task.due_date , order = task.order  )
            new_task.save()

        return  new_checklist
