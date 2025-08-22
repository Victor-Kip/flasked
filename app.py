from flask import Flask,render_template,redirect,request 
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

assets = Environment(app)
scss = Bundle("scss/styles.scss", filters="libsass", output="css/styles.css")
assets.register("scss_all", scss)
assets.auto_build = True
assets.debug = False

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydadabase.db"
db =SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(100),nullable=False)
    complete = db.Column(db.Integer,default = 0)
    created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self)->str:
        return f"Task{self.id}"
with app.app_context():
        db.create_all()
    
@app.route('/',methods=["POST","GET"])
def index():
    #add a task to database
    if request.method == "POST":
        current_task =  request.form['content']
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    #list tasks in the database
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html',tasks = tasks)

#delete a task
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"
    
@app.route("/edit/<int:id>",methods = ["GET","POST"])
def edit(id:int):
    update_task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html',task = update_task)

@app.route('/test')
def test():
    return render_template('testing.html')

if __name__ == '__main__':
    
    app.run(debug=True)
