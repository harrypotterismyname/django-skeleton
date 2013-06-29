from django.db import models
from django.utils.translation import ugettext_lazy as _
from userena.utils import user_model_label
from django.template.defaultfilters import slugify
from random import randint

class CheckList(models.Model):
    title = models.CharField(max_length=1024, blank=True)
    slug = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    grade = models.FloatField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    users = models.ManyToManyField(user_model_label, through='UserCheckList')
    owner = models.ForeignKey(user_model_label, null=True, related_name='owner')


    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        #TODO: fix this

        if self.slug is None or self.slug == "":
            self.slug = CheckList.generate_slug(self.title)

        super(CheckList, self).save(*args, **kwargs)

    def get_by_id(self, id):
        return self.objects.get(id=id)

    def update(self, title):
        self.title = title
        self.save()
        return self;

    def update(self, checklist):
        self.title = checklist.title
        return  self

    def delete(self):
        self.is_deleted = True
        self.update(self)
        return self

    def get_by_slug(self,slug):
        return CheckList.objects.only(slug=slug)

    def get_list_task(self):
        return Task.objects.filter(id_check_list = self.id)

    def count_task(self):
        return Task.objects.filter(check_list_id=self.id).count()

    def get_url(self):
        return '/checklist/' + self.slug + '/'

    @classmethod
    def generate_slug(self, name):
        count = 1
        slug = slugify(name)

        def _get_query(slug):
            if CheckList.objects.filter(slug=slug).count():
                return True

        while _get_query(slug):
            slug = slugify(u'{0}-{1}'.format(name, count))
            # make sure the slug is not too long
            while len(slug) > CheckList._meta.get_field('slug').max_length:
                name = name[:-1]
                slug = slugify(u'{0}-{1}'.format(name, count))
            count = randint(1,100)
        return slug


class Task(models.Model):
    title = models.CharField(max_length=1024, blank=True)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    check_list = models.ForeignKey(CheckList, null=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_by_id(self):
        return self.objects.filter(id=id)

    def get_by_title(self, title):
        return self.objects.filter(title=title)

    def get_by_is_checked(self):
        return self.objects.filter(is_checked=True)

    def get_child_task(self):
        return Task.objects.filter(parent=self)

    def count_child_task(self):
        return Task.objects.filter(parent=self).count()

    def delete(self):
        self.is_deleted = True
        self.update(self)
        return True

    def update(self, task):
        self.title = task.title
        self.is_checked = task.is_checked
        self.id_check_list = task.id_check_list
        self.is_deleted = task.is_deleted
        self.parent = task.parent
        return  self


class UserCheckList(models.Model):
    user = models.ForeignKey(user_model_label)
    checklist = models.ForeignKey(CheckList)
   # is_owner = models.BooleanField(default=False)

