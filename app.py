from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db  = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    iteam = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(200),nullable=False)
    Created_date = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return  f"{self.sno}"  f"{self.iteam}"

@app.route('/',methods=["GET","POST"])
def hello():
    if request.method =="POST":
        iteam=request.form['iteam']
        desc=request.form['desc']
        todo=Todo(iteam=iteam,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo =Todo.query.all()
    return render_template('index.html',alltodo=alltodo)
    #return 'Hello World'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo =Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=["POST","GET"])
def update(sno):
    if request.method=="POST":
        iteam=request.form['iteam']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.iteam=iteam
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


# @app.route('/show')
# def product():
#     alltodo =Todo.query.all()
#     print(alltodo)
    # return render_template('update.html')
    # return 'This is my product'

if __name__ == '__main__':
    app.run(debug=True)

