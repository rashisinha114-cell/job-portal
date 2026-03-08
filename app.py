from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Rashi123%40sinha@localhost/jobportal'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)


# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    description = db.Column(db.Text)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer)
    user_email = db.Column(db.String(100))
    resume = db.Column(db.String(200))


# ROUTES
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register-page")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    user = User(
        username=request.form["username"],
        email=request.form["email"],
        password=request.form["password"]
    )
    db.session.add(user)
    db.session.commit()
    return redirect("/login-page")


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        session["user"] = email
        return redirect("/dashboard")
    else:
        return "Login Failed"



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login-page")

    jobs = Job.query.all()
    return render_template("dashboard.html", jobs=jobs)


@app.route("/post-job-page")
def post_page():
    return render_template("post_job.html")


@app.route("/post-job", methods=["POST"])
def post_job():
    job = Job(
        title=request.form["title"],
        company=request.form["company"],
        description=request.form["description"]
    )
    db.session.add(job)
    db.session.commit()
    return redirect("/dashboard")


@app.route("/apply/<int:jid>")
def apply_page(jid):
    return render_template("apply_job.html", jid=jid)


@app.route("/apply-job", methods=["POST"])
def apply_job():
    file = request.files["resume"]
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    application = Application(
        job_id=request.form["jid"],
        user_email=session["user"],
        resume=filename
    )
    db.session.add(application)
    db.session.commit()

    return redirect("/dashboard")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
