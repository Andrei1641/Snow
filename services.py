import json
import os

from sqlalchemy import text
from db import *
from models import User



def get_users_safe():
    try:
        db.session.execute(text("SELECT 1"))

        user = User.query.first()
        score = user.scores
        return score

    except Exception as e:
        score = []
        if not os.path.exists("data.json"):
            with open("data.json", "w") as f:
                file = {'scores': []}
                json.dump(file, f)

        with open("data.json", "r") as f:
            file = json.load(f)
            score = file.get('scores')

        return score

def set_users_safe(file):
    try:
        user = User.query.first()
        new_score = file['scores']
        user.scores = new_score

        db.session.commit()
    except Exception:
        with open("data.json", "w") as f:
            json.dump(file, f)

# app = create_app()
# with app.app_context():
#     print(get_users_safe())
