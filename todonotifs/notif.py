import datetime
from dateutil.parser import parse
import todonotifs.queries as queries
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.base import STATE_RUNNING, STATE_STOPPED

jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///resources/sqlite/todos.db', tablename='notifs')}

sched = BackgroundScheduler(jobstores = jobstores)

def send_notification(title, message):
    notification.notify(
            title = title,
            message = message,
            app_icon = r"resources\icons\default_notification.ico", # customize according to subject icon later
            timeout = 20,
        )

def add_notification(params, todo_id, notif_time=None):
    date = parse(params['date'])
    title = date.strftime("%a %b %d %I:%M %p")
    if params['subject']:
        title += params['subject']
    message = params['name']
    if notif_time:
        job = sched.add_job(send_notification, "date", [title, message], next_run_time = notif_time, replace_existing = True)
        queries.run_query(queries.add_notif_todo_id, [todo_id, job.id])
        print("Notification set for:", notif_time)
    # todo: if date is not specified run cron job repeating every day

def delete_notifications(todo_id):
    notifications = queries.run_query(queries.get_notif_by_todo, [todo_id])
    for i in notifications:
       notif_id = i[0]
       sched.remove_job(notif_id)
    return True

def start():
    if sched.state == STATE_STOPPED:
        sched.start()
        print('Notifier started.')
