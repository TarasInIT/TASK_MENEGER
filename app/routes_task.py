# routes_admin.py
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.forms import TaskForm
from app.models import Task, User
import os


tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks', methods=['GET'])
@login_required
def tasks_list():
    search_term = request.args.get('search', '')
    filter_status = request.args.get('status', 'all')
    user_id = request.args.get('user_id', type=int)

    # Формуємо запит
    if current_user.email == os.getenv('ADMIN_EMAIL') or current_user.is_admin:
        query = Task.query
        if user_id:
            query = query.filter_by(user_id=user_id)
    else:
        query = Task.query.filter_by(user_id=current_user.id)

    if filter_status == 'done':
        query = query.filter_by(is_done=True)
    elif filter_status == 'not-done':
        query = query.filter_by(is_done=False)
    if search_term:
        query = query.filter(Task.title.ilike(f'%{search_term}%'))

    tasks_data = query.all()
    users = User.query.all() if current_user.is_admin else []
    now = datetime.now()
    return render_template(
        'tasks.html',
        tasks=tasks_data,
        search_term=search_term,
        filter_status=filter_status,
        users=users,
        selected_user_id=user_id,
        now=now
    )


@tasks.route('/tasks/create', methods=['POST'])
@login_required
def create():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip() or None
    deadline_raw = request.form.get('deadline')
    assignee_id = request.form.get('assignee_id', type=int)

    # Просте валідоване title
    if not title:
        flash('Название задачи не может быть пустым.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    # Парсимо дедлайн
    deadline = None
    if deadline_raw:
        try:
            deadline = datetime.fromisoformat(deadline_raw)
        except ValueError:
            flash('Неверный формат дедлайна.', 'danger')
            return redirect(url_for('tasks.tasks_list'))

    # 1) Зберігаємо автора
    author_id = current_user.id

    # 2) Зберігаємо одноособового виконавця
    # (якщо адмiн обрав юзера – призначаємо, інакше None)
    valid_assignee_id = None
    if current_user.is_admin and assignee_id:
        # опційно перевіряємо, що такий юзер існує
        if User.query.get(assignee_id):
            valid_assignee_id = assignee_id
        else:
            flash('Користувач не знайдений для призначення.', 'danger')
            return redirect(url_for('tasks.tasks_list'))

    # Створюємо Task
    task = Task(
        title=title,
        description=description,
        deadline=deadline,
        user_id=author_id,         # автор
        assignee_id=valid_assignee_id  # одноособовий виконавець
    )
    db.session.add(task)
    db.session.commit()

    flash('Задачу успішно створено.', 'success')
    return redirect(url_for('tasks.tasks_list'))


@tasks.route('/tasks/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.is_admin and task.user_id != current_user.id:
        flash('У вас немає дозволу на редагування цієї задачі.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    # Витягуємо значення з форми (HTML POST)
    task.title = request.form.get('title', '').strip()
    task.description = request.form.get('description', '').strip() or None
    deadline_raw = request.form.get('deadline')
    is_done = request.form.get('is_done')
    assignee_id = request.form.get('assignee_id', type=int)

    # Обробка дедлайну
    try:
        task.deadline = datetime.fromisoformat(deadline_raw) if deadline_raw else None
    except ValueError:
        flash('Невірний формат дедлайну.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    # Статус
    task.is_done = True if is_done else False

    # Призначення виконавця
    if current_user.is_admin and assignee_id:
        user = User.query.get(assignee_id)
        if user:
            task.assignee_id = assignee_id
        else:
            flash('Користувач для виконавця не знайдений.', 'danger')
            return redirect(url_for('tasks.tasks_list'))

    db.session.commit()
    flash('Задача оновлена успішно!', 'success')
    return redirect(url_for('tasks.tasks_list'))


@tasks.route('/tasks/task/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.is_admin and task.user_id != current_user.id:
        flash('У вас немає дозволу на перегляд цієї задачі.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    users = User.query.all() if current_user.is_admin else []

    return render_template("tasks.html", tasks=tasks, users=users, current_user=current_user, now=datetime.utcnow())


@tasks.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.is_admin and task.user_id != current_user.id:
        flash('У вас немає дозволу на видалення цієї задачі.', 'danger')
        return redirect(url_for('tasks.tasks_list'))

    db.session.delete(task)
    db.session.commit()
    flash('Задачу успішно видалено.', 'success')
    return redirect(url_for('tasks.tasks_list'))





