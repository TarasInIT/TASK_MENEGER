from datetime import datetime
from app import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    telegram_id = db.Column(db.Integer, unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    surname = db.Column(db.String(80), nullable=True)
    position = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(120), nullable=True)

    authored_tasks = db.relationship('Task', back_populates='creator', foreign_keys='Task.user_id')
    assigned_tasks = db.relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(500), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', back_populates='authored_tasks', foreign_keys=[user_id])

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assignee = db.relationship('User', back_populates='assigned_tasks', foreign_keys=[assignee_id])

    def __repr__(self):
        return f'<Task {self.title}>'
