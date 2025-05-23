import random
from app.models import User

def get_all_users():
    return User.query.all()

def generate_initials_avatar(username, size=32):
    if not username:
        initials = "?"
    else:
        initials = ''.join([word[0].upper() for word in username.split() if word])

    colors = ["#F44336", "#E91E63", "#9C27B0", "#3F51B5",
              "#03A9F4", "#009688", "#4CAF50", "#FF9800", "#795548"]
    bg_color = random.choice(colors)

    svg = f'''
    <svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
        <circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg_color}" />
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
              font-size="{int(size * 0.5)}" fill="white" font-family="Arial, sans-serif">
            {initials}
        </text>
    </svg>
    '''
    return svg



