from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes_main import main
    from app.auth import auth
    from app.routes_admin import admin
    from app.routes_task import tasks
    from app.routes_users import profile
    from app.utils import generate_initials_avatar


    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(profile, url_prefix='/profile')

    app.jinja_env.globals.update(generate_initials_avatar=generate_initials_avatar)

    return app
