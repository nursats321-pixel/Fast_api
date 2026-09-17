from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from database import tasks_db
from bot import send_telegram_message

def check_deadlines():
    now_str = datetime.now().strftime("%H:%H")

    for task in tasks_db:
        if not task["completed"] and not task["notifiend"]:
            if task["deadline"] <= now_str:
                msg = f"<b>ВНИМАНИЕ! Просрочка</b>\n\nЗадача <i>'{task['title']}'</i> должна быть выполнена к{task['deadline']}!"


                success = send_telegram_message(task["chat_id"], msg)

                if success:
                    task["notified"] = True
                    print(f"[Scheduler] Уведомление по задаче {task['id']} отправлено")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_deadlines, 'interval', minutes=1)
    scheduler.start()
    print()