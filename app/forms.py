from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, FileField, EmailField, \
    TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.utils import get_all_users

class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired(), Length(min=3, max=25)],
        render_kw={"placeholder": "Введите имя пользователя", "autocomplete": "username"})
    email = EmailField(
        'Робоча електронна пошта',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Введите email", "autocomplete": "email"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Введите пароль", "autocomplete": "new-password"}
    )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"placeholder": "Введите пароль ещё раз", "autocomplete": "new-password"}
    )
    submit = SubmitField('Зарегистрироваться')



class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Введите email", "autocomplete": "email"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"placeholder": "Введите пароль", "autocomplete": "current-password"}
    )
    submit = SubmitField('Войти')



class TaskForm(FlaskForm):

    title = StringField(
        'Название задачи',
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Введите название задачи"}
    )
    description = TextAreaField(
        'Описание задачи',
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Опишите задачу"}
    )
    is_done = BooleanField('Завершено')

    deadline = DateTimeField(
        'Конечный срок',
        format='%Y-%m-%d %H:%M',
        validators=[DataRequired()],
        render_kw={"placeholder": "Выберите конечный срок", "type": "datetime-local"}
    )

    assignees = QuerySelectMultipleField(
        'Исполнители',
        query_factory=get_all_users,
        get_label='username',
        allow_blank=True
    )

    submit = SubmitField('Сохранить')


class ProfileForm(FlaskForm):
    username = StringField(
        'Имя',
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Введите ваше имя"}
    )
    surname = StringField(
        'Фамилия',
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"placeholder": "Введите вашу фамилию"}
    )
    position = StringField(
        'Должность',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "Введите вашу должность"}
    )
    phone = StringField(
        'Телефон',
        validators=[Optional(), Length(max=20)],
        render_kw={"placeholder": "Введите ваш рабочий телефон"}
    )
    avatar = FileField(
        'Аватар',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')]
    )

    submit = SubmitField('Сохранить изменения')





