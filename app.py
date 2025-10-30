import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite データベースの絶対パス（Render対応）
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "bbs.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 投稿モデル
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# トップページ
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

# 投稿処理
@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content")
    if content:
        new_post = Post(content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect("/")

# Render 用ポートバインド
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)