from django.utils import timezone
from mylist.models import Task
from south.utils.datetime_utils import datetime

__author__ = 'hanhdoan'


from django.core.management.base import BaseCommand, CommandError




from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

class Command( BaseCommand):
    args = ''
    help = ''

    def handle (self, *args, **options):

        today = timezone.now()
        day_prev =  today - datetime.timedelta(days=-3)

        late_task = Task.objects.filter( real_due_date__lte = today, is_delete = False, last_reminder__lt =  day_prev , is_checked = False  )


        for task in late_task:


            template = get_template("mail/daily_reminder.html")
            context = Context({
                "task":task,
            })
            message  = template.render(context)

            #print message

            msg = EmailMessage('[ChecklistSimply] Nhắc nhở bạn!',message, 'EduSmile Team <hong@vietnamdevelopers.com>',[ task.check_list.owner.email ])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
