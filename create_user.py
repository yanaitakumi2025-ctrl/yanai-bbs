# create_user.py
from app import db, User
from werkzeug.security import generate_password_hash

with db.session.begin():
    user = User(username="takumi", password=generate_password_hash("yourpassword"))
    db.session.add(user)

print("ユーザー登録完了")