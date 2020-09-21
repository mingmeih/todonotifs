import time

from todonotifs import notif
if __name__ == '__main__':
    notif.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Notifier shut down.")
        