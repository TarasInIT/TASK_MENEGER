import os
from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Task


admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if current_user.email != os.getenv('ADMIN_EMAIL'):
        flash('У вас нет доступа к этой странице.', 'danger')
        return redirect(url_for('main.index'))

    tab = request.args.get('tab', 'users')
    users = User.query.paginate(page=request.args.get('page', 1, type=int))
    tasks = Task.query.paginate(page=request.args.get('page', 1, type=int), per_page=10)

    return render_template(
        'admin_panel.html', title='Admin Panel', users=users, tasks=tasks, active_tab=tab)


@admin.route('/update_position', methods=['POST'])
@login_required
def update_position():
    if not current_user.is_admin or current_user.email == os.getenv('ADMIN_EMAIL'):
        flash("Недостаточно прав для редактирования должности.", "danger")
        return redirect(url_for('main.index'))

    current_user.position = request.form.get('position')
    db.session.commit()
    flash("Должность обновлена.", "success")
    return redirect(url_for('main.profile'))


@admin.route('/admin/set-role/<int:user_id>', methods=['POST'])
@login_required
def set_user_role(user_id):
    if current_user.email != os.getenv('ADMIN_EMAIL'):
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get('new_role')
    user.is_admin = (new_role == 'admin')
    db.session.commit()
    flash(f"Роль пользователя {user.username} обновлена", 'success')
    return redirect(url_for('admin.admin_panel'))

