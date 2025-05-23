import os
import random
from datetime import datetime, timedelta

from faker import Faker
from app import create_app, db
from app.models import User, Task
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

fake = Faker()
app = create_app()

with app.app_context():
    # Створюємо всі таблиці
    db.create_all()

    # Адмін: дані з .env або дефолтні
    admin_email = os.getenv("ADMIN_EMAIL", "admin@admin.by")
    admin_username = "Головний Адмін"
    admin_password = os.getenv("ADMIN_PASSWORD", "adminadmin")

    # Перевірка чи головний адмін існує
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            username=admin_username,
            email=admin_email,
            is_admin=True,
            position="Головний адміністратор",
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("✅ Створено головного адміна")

    # Створюємо 4 додаткових адміни (керівники)
    managers = [admin]  # додаємо головного адміна до списку
    for _ in range(4):
        manager = User(
            username=fake.name(),
            email=fake.unique.email(),
            is_admin=True,
            position="Керівник",
        )
        manager.set_password("password123")
        db.session.add(manager)
        managers.append(manager)

    # Створюємо 15 працівників (звичайні юзери)
    workers = []
    for _ in range(15):
        worker = User(
            username=fake.name(),
            email=fake.unique.email(),
            is_admin=False,
            position="Працівник",
        )
        worker.set_password("password123")
        db.session.add(worker)
        workers.append(worker)

    db.session.commit()
    print("👥 Користувачі створені")

    # Створюємо 40 задач — створюють лише адміни, а виконавці — тільки працівники
    for _ in range(40):
        creator = random.choice(managers)     # автор — один з адмінів
        assignee = random.choice(workers)     # виконавець — звичайний юзер

        task = Task(
            title=fake.sentence(nb_words=4),
            description=fake.text(max_nb_chars=120),
            is_done=random.choice([True, False]),
            deadline=datetime.utcnow() + timedelta(days=random.randint(-7, 30)),
            user_id=creator.id,
        )

        task.assignees = [assignee]
        db.session.add(task)

    db.session.commit()
    print("📝 Задачі створені")
    print("🎉 База даних заповнена тестовими даними!")
