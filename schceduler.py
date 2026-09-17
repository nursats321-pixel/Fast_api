
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from database import tasks_collection
from bot import send_telegram_message


def check_deadlines():
    now_str = datetime.now().strftime("%H:%M")

    tasks = tasks_collection.find({
        "completed": False,
        "notified": False,
        "deadline": {"$ne": None}
    })

    for task in tasks:
        deadline = task["deadline"]

        if deadline <= now_str:
            msg = (
                f"<b>ВНИМАНИЕ! Просрочка</b>\n\n"
                f"Задача <i>'{task['title']}'</i> "
                f"должна быть выполнена к {deadline}!"
            )

            success = send_telegram_message(
                task["chat_id"],
                msg
            )

            if success:
                tasks_collection.update_one(
                    {"_id": task["_id"]},
                    {
                        "$set": {
                            "notified": True
                        }
                    }
                )

                print(
                    f"[Scheduler] "
                    f"Уведомление по задаче {task['id']} отправлено"
                )


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_deadlines,
        "interval",
        minutes=1
    )

    scheduler.start()

    print("[Scheduler] Запущен")