import json
import os

from sqlalchemy import text
from db import *
from models import User


def get_users_safe():
    try:
        db.session.execute(text("SELECT 1"))

        users = User.query.all()
        score = []
        for user in users:
            score.append(user.score)
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