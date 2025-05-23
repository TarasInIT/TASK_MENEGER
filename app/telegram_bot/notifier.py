# routes_main.py
import os
import asyncio
from collections import Counter
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from telegram import Bot
from app import create_app, db
from app.models import Task, User

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

flask_app = create_app()

import os
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from telegram import Bot
from app import create_app, db
from app.models import Task, User

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
flask_app = create_app()

def check_deadlines():
    with flask_app.app_context():
        now = datetime.now()
        soon = now + timedelta(hours=24)

        tasks = Task.query.filter(
            Task.deadline != None,
            Task.deadline <= soon,
            Task.is_done == False
        ).all()

        user_tasks = {}

        for task in tasks:
            if task.user_id not in user_tasks:
                user_tasks[task.user_id] = []
            user_tasks[task.user_id].append(task)

        for user_id, task_list in user_tasks.items():
            user = User.query.get(user_id)
            if not user or not user.telegram_id:
                continue

            task_lines = [f"{t.id}. {t.title} — до {t.deadline.strftime('%Y-%m-%d %H:%M')}" for t in task_list]
            count = len(task_lines)
            message = f"У вас {count} не виконаних задач:\n" + "\n".join(task_lines)
            bot.send_message(chat_id=user.telegram_id, text=message)

scheduler = BackgroundScheduler()
scheduler.add_job(check_deadlines, 'interval', minutes=1)
scheduler.start()


def wrapped_check_deadlines():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(check_deadlines())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(check_deadlines())


scheduler = BackgroundScheduler()
scheduler.add_job(wrapped_check_deadlines, 'interval', hours=3, minutes=0)
scheduler.start()


try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
