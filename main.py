import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User

app = create_app()

def create_admin():
    load_dotenv()
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')

    if not User.query.filter_by(is_admin=True).first():

        admin = User(
            username=admin_username,
            email=admin_email,
            telegram_id=admin_chat_id,
            is_admin=True
        )

        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user {admin_username} created.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)

    admin_chat_id = os.getenv('ALLOWED_CHAT_IDS')
