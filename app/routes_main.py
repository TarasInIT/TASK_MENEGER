from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/link-telegram/<int:telegram_id>')
@login_required
def link_telegram(telegram_id):
    current_user.telegram_id = telegram_id
    db.session.commit()
    flash('Telegram ID linked successfully!', 'success')
    return redirect(url_for('main.index'))


