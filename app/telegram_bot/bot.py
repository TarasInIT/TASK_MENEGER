import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app import create_app, db
from app.models import User, Task

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_ID = int(os.getenv('ALLOWED_CHAT_ID'))

flask_app = create_app()
telegram_app = ApplicationBuilder().token(TOKEN).build()

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with flask_app.app_context():
        user = User.query.filter_by(telegram_id=update.effective_user.id).first()
        if user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome back! Press /tasks to see your tasks.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first.")


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with flask_app.app_context():
        user = User.query.filter_by(telegram_id=update.effective_user.id).first()
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first.")
            return

        task_list = Task.query.filter_by(user_id=user.id).all()

        if not task_list:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks found.")
            return

        tasks_lines = [f"{t.id}. {t.title} {'✅' if t.is_done else '❌'}" for t in task_list]

        message = "📝 *Your tasks🫵:*\n" + "\n".join(tasks_lines)

        # Надсилаємо повідомлення користувачу
        await context.bot.send_message(
            chat_id=user.telegram_id,
            text=message,
            parse_mode="Markdown"  # Використовуємо Markdown для форматування
        )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with flask_app.app_context():
        user = User.query.filter_by(telegram_id=update.effective_user.id).first()
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first.")
            return

        # Отримуємо заголовок задачі, який користувач передає після команди /add
        task_title = " ".join(context.args)
        if not task_title:  # Якщо не вказано заголовок задачі
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a task title.")
            return

        # Створюємо нову задачу
        new_task = Task(title=task_title, user_id=user.id)
        db.session.add(new_task)
        db.session.commit()

        # Підтвердження, що задача була додана
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Task '{task_title}' added successfully!")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with flask_app.app_context():
        user = User.query.filter_by(telegram_id=update.effective_user.id).first()  # Шукаємо користувача
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please register first.")
            return

        try:
            task_id = int(context.args[0])
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid task ID.")
            return

        task = Task.query.get(task_id)
        if not task or task.user_id != user.id:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Task not found or you don't have permission to delete it.")
            return

        db.session.delete(task)
        db.session.commit()

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Task '{task.title}' deleted successfully!")


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tasks", tasks))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("delete", delete))

if __name__ == "__main__":
    print("Starting Telegram bot...")
    app.run_polling()
