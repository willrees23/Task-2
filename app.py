from flask import Flask, request, render_template, session, url_for, redirect
from flask_session import Session
import db

app = Flask(__name__)
app.config["SESSION_TYPE"] = (
    "filesystem"  # options: "filesystem", "redis", "memcached", "null", "cachelib"
)
Session(app)


@app.route("/")
def index():
    if session.get("user"):
        return render_template("index.html", user=session["user"])
    return render_template("index.html")


@app.route("/become-a-tutor")
def become_a_tutor():
    return render_template("become-a-tutor.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user"):
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form["email"]
        if db.email_taken(email):
            return "Email already taken!"
        type = "student"
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]
        if password != confirm:
            return "Passwords do not match!"
        user = db.create_user(type, first_name, last_name, email, password)
        session["user"] = user
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db.get_user(email)
        if user is None:
            return render_template("login.html", error="Incorrect email or password.")
        if not db.check_password(user, password):
            return render_template("login.html", error="Incorrect email or password.")
        session["user"] = user
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
