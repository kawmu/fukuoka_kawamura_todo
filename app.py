from flask import Flask, render_template,redirect,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
#import requests





 #アプリ名記入
app = Flask(__name__)
#データベースを使用する儀式
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'#todo.dbという名前のデータベースを設定
db = SQLAlchemy(app)   

with app.app_context():
    db.create_all()

#データベースに保存するデータは以下である
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)#idは整数
    title = db.Column(db.String(30), nullable=False)#タイトルは空白は許可しない
    detail = db.Column(db.String(100),nullable = False)#記入は空白でもよい
    due = db.Column(db.DateTime, nullable=False)

#アプリ内で表示
@app.route('/',methods = ['GET','POST'])
#この関数はrender_templateを用いてindex.htmlの中身を表示します
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()#締め切り近い順に変更
        return render_template('index.html',posts = posts,today = date.today())
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        #datetimeの場合、正しい文字列は%Y-%m-%dである。
        due = datetime.strptime(due,'%Y-%m-%d')
        new_post = Post(title = title, detail = detail, due = due )

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')


#アプリ内で表示
@app.route('/list')
def index_a():
    posts = Post.query.order_by(Post.due).all()
    post_list = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'detail': post.detail
        }
        post_list.append(post_data)
    return jsonify(post_list)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    if post is None:
        return "Error : Post not Found"#受信できなかったとき

    return render_template('detail.html',post = post)

#タスクを削除するための機能をつける
#ルートはdelete
@app.route('/delete/<int:id>')#削除機能を持ったurlとそのid
def delete(id):               #指定のidが引き渡されたらそのidに対応したタスクの削除
    post = Post.query.get(id)#該当する投稿のidを取得する

    db.session.delete(post)
    db.session.commit()#セッションに対して行われた変更をデータベースに反映する
    return redirect('/')#トップページに反映する

@app.route('/update/<int:id>',methods = ['GET','POST'])#編集機能
def update(id):
    post = Post.query.get(id)

    if request.method == 'GET':
        return render_template('update.html',post = post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

    

if __name__ ==  "__main__":
    app.run(debug=True)
