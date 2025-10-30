from flask import Flask, render_template, request, redirect
from models import db, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/bbs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        if name and content:
            post = Post(
                name=name,
                content=content,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(post)
            db.session.commit()
        return redirect('/')
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = db.session.get(Post, post_id)  # SQLAlchemy 2.0対応
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/')

# 🔸 app.run() は削除。Render では gunicorn が起動するため不要