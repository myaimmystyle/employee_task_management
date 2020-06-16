import pandas as pd
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta
from django.utils import timezone
from core.models import Tasks

@periodic_task(run_every=(crontab(minute=0, hour=0, day_of_week='sunday')), name="some_task", ignore_result=True)
def generate_report():
    now = timezone.now()
    monday = now.date() - timedelta(days=7)
    df = pd.DataFrame(list(Tasks.objects.filter(created_on__gte=monday,created_on__lte=timezone.now()).values("task_name","task_status","task_time","created_by__first_name","created_by__last_name")))
    df.to_excel("Reports"+"/"+str(now.strftime("%m-%d-%Y"))+'_TaskReport.xlsx', index = False)