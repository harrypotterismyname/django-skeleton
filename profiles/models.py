from django.db import models
from django.utils.translation import ugettext_lazy as _

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