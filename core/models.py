from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

TASK_STATUS = [('IN','Inprogress'),('CP','Complete')]
NOTIFICATION_STATUS = [('R','read'),('U','unread')]

class CommonFields(models.Model):
    created_by = models.ForeignKey(User,related_name='CommonFields_created_by',on_delete=models.SET_NULL,null=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(User,related_name='CommonFields_modified_by',on_delete=models.SET_NULL,null=True)
    modified_on = models.DateTimeField(default=timezone.now)


class Tasks(CommonFields):
    task_name = models.CharField(max_length=50)
    task_time = models.IntegerField(default=0)
    task_status = models.CharField(max_length=2,choices=TASK_STATUS,default='IN')

    def __str__(self):
        return self.task_name

class Comments(CommonFields):
    task = models.ForeignKey(Tasks,related_name='Tasks_Comments',on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment

class Reports(models.Model):
    report = models.FileField(upload_to='reports/')
    created_on = models.DateTimeField(default=timezone.now)

class Notifications(models.Model):
    content = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=NOTIFICATION_STATUS,default='U')

    def __str__(self):
        return self.content

# method for updating
@receiver(post_save, sender=Tasks)
def create_notifications(sender, instance, **kwargs):
    first_name = instance.created_by.first_name
    last_name = instance.created_by.last_name
    text = first_name+" "+last_name+" added/modified task "+instance.task_name
    obj = Notifications.objects.create(content=text)
    obj.save()


