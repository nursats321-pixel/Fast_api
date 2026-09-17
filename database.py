from pymongo import MongoClient, ReturnDocument

client = MongoClient("mongodb://localhost:27017/")

db = client["tasks_db"]

tasks_collection = db["tasks"]


def get_all_tasks():
    tasks = list(
        tasks_collection.find(
            {},
            {"_id": 0}
        )
    )

    return tasks


def add_task(title: str, deadline: str, chat_id: int):
    last_task = tasks_collection.find_one(
        sort=[("id", -1)]
    )

    task_id = last_task["id"] + 1 if last_task else 1

    new_task = {
        "id": task_id,
        "title": title,
        "deadline": deadline,
        "chat_id": chat_id,
        "completed": False,
        "notified": False
    }

    tasks_collection.insert_one(new_task)

    return new_task


def mark_task_completed(task_id: int):
    result = tasks_collection.find_one_and_update(
        {"id": task_id},
        {"$set": {"completed": True}},
        return_document=ReturnDocument.AFTER
    )

    if result:
        result.pop("_id", None)

    return result