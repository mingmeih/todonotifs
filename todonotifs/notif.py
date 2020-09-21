import datetime
from dateutil.parser import parse
import time
import todonotifs.queries as queries
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore

sched = BackgroundScheduler()

def send_notification(title, message):
    notification.notify(
            title = title,
            message = message,
            app_icon = r"resources\icons\default_notification.ico",
            timeout = 20,
        )

def add_notification(params, todo_id, notif_time=None):
    if params['date']:
        date = parse(params['date'])
        title = date.strftime("%a %b %d %I:%M %p")
        if params['subject']:
            title += params['subject']
        message = params['name']
        new_notif_id = str(queries.run_query(queries.add_notif, [todo_id, notif_time]))
        if notif_time:
            sched.add_job(send_notification, "date", [title, message], run_date = notif_time, id = new_notif_id)
            print("Notification set for:", notif_time)
        else:
            sched.add_job(send_notification, "cron", [title, message], hour = 12, id = new_notif_id) # repeats daily at 12 pm by default, will add option to customize daily reminders

def delete_notifications(todo_id):
    notifications = queries.run_query(queries.get_notif_by_todo, [todo_id])
    for i in notifications:
        notif_id = i[0]
        sched.remove_job(str(notif_id))

def start():
    print('Notifier started.')
    sched.start()