import uuid
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import ProfileForm

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.surname = form.surname.data
        current_user.position = form.position.data
        current_user.phone = form.phone.data

        if form.avatar.data:
            old_avatar = current_user.avatar
            if old_avatar and old_avatar != 'default.png':
                old_path = os.path.join('app/static/avatars', old_avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)

            avatar_filename = secure_filename(form.avatar.data.filename)
            unique_filename = f"{uuid.uuid4().hex}_{avatar_filename}"
            avatar_path = os.path.join('app/static/avatars', unique_filename)
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            form.avatar.data.save(avatar_path)
            current_user.avatar = unique_filename

        db.session.commit()
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('profile.edit_profile'))

    return render_template('settings.html', form=form)



