from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    dateandtime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title = title, description = description)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo = alltodo)

@app.route("/update/<int:sno>", methods = ["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        updatetodo = Todo.query.filter_by(sno=sno).first()
        updatetodo.title = title
        updatetodo.description = description
        db.session.add(updatetodo)
        db.session.commit()
        return redirect("/")
    updatetodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", updatetodo = updatetodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    deletetodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect("/")
