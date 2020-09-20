import datetime
from dateutil.parser import parse
import time
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

def send_notification(title, message):
    notification.notify(
            title = title,
            message = message,
            app_icon = r"resources\icons\default_notification.ico",
            timeout = 20,
        )

def add_notification(params):
    if params['date']:
        date = parse(params['date'])
        title = date.strftime("%a %b %d %I:%M %p")
        if params['subject']:
            title += params['subject']
        message = params['name']
        sched.add_job(send_notification, "date", [title, message])


def main():
    sched.add_job(send_notification, 'interval', seconds=20)
    sched.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Notifier shut down.')