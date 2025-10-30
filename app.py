from flask import Flask, render_template, request, redirect
from models import db, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Flask 3.x では app_context で DB 初期化
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
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)