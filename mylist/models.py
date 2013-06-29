from django.db import models
from django.utils.translation import ugettext_lazy as _
from userena.utils import user_model_label
from django.template.defaultfilters import slugify

class CheckList(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024, blank=True)
    slug = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


    def get_by_id(self, id):
        return self.objects.get(id=id)

    def insert(self, checklist):
        self.title = checklist.title
        self.slug = generate_slug(checklist.title)
        self.save()
        return self

    def insert(self, title):
        self.title = title
        self.slug = generate_slug(title)
        self.save()
        return self

    def update(self, title):
        self.title = title
        self.slug = generate_slug(title)
        self.save()

        return self;
    def get_by_slug(self,slug):
        return CheckList.objects.only(slug=slug)

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
        count += 1 # + 1
    return slug

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024, blank=True)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    id_check_list = models.ForeignKey(CheckList, null=True)
    parent = models.ForeignKey('self', null=True, blank=True)