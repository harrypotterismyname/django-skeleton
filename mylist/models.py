import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from userena.utils import user_model_label
from django.utils.timezone import utc

class CheckList(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    slug = models.CharField(_('Slug'), max_length=255)

    rate = models.FloatField(_('Rate'), null=True, blank=True)
    owner = models.ForeignKey(user_model_label, null=True, related_name='owner', verbose_name=_('Owner'))
    start_at = models.DateTimeField(_('Start at'))

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Parent'))
    is_deleted = models.BooleanField(_('Deleted'), default=False)
    created_at = models.DateTimeField(_('Created at'), null=True, auto_now_add=True)
    public = models.BooleanField(_('Public'), default=False,
                                 help_text=_('Check this if you want to publish checklist.'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CheckList, self).save(*args, **kwargs)

    def get_list_task(self):
        return self.tasks.filter(is_deleted=False, parent__isnull=True)

    def count_task(self):
        return self.tasks.filter(is_deleted=False).count()

    def get_absolute_url(self):
        return reverse('mylist:detail', kwargs={'slug': self.slug, 'id': self.id})

    class Meta:
        ordering = ('-created_at',)


class Task(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    check_list = models.ForeignKey(CheckList, related_name='tasks', verbose_name=_('Checklist'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Parent'))

    due_date = models.PositiveSmallIntegerField(_('Due date'), default=0)

    is_checked = models.BooleanField(_('Checked'), default=False)
    is_deleted = models.BooleanField(_('Deleted'), default=False)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def can_edit(self, user):

        if self.check_list.owner == user or user.is_staff:
            return True

        return False

    def __unicode__(self):
        return self.title

    def get_by_is_checked(self):
        return self.objects.filter(is_checked=True, is_deleted=False)

    def get_child_task(self):
        return self.children.filter(is_deleted=False)

    def count_child_task(self):
        return self.get_child_task().count()

    def is_overdated(self):
        if self.check_list.start_at and self.due_date > 0:
            if (self.check_list.start_at + datetime.timedelta(days=self.due_date)) < timezone.now():
                return True
        return False

    def remain_date(self):
        if not self.is_overdated():
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            return (self.check_list.start_at + datetime.timedelta(days=self.due_date)) - now
        return None

    class Meta:
        ordering = ('-check_list', 'order',)



