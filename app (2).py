from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "SECRET_KEY_CHANGE_THIS"

# ---- Database (in-memory) ----
users = {
    "admin": generate_password_hash("admin123")
}

apartments = [
    {"id": 1, "name": "A1", "type": "1 Bedroom", "status": "Available"},
    {"id": 2, "name": "A2", "type": "1 Bedroom", "status": "Reserved"},
    {"id": 3, "name": "B1", "type": "2 Bedroom", "status": "On Hold"},
    {"id": 4, "name": "B2", "type": "2 Bedroom", "status": "Available"},
    {"id": 5, "name": "B3", "type": "2 Bedroom", "status": "Available"},
    {"id": 6, "name": "B4", "type": "2 Bedroom", "status": "Reserved"},
    {"id": 7, "name": "C1", "type": "3 Bedroom", "status": "Available"},
]

# ---- Login Required Decorator ----
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ---- AUTH ----
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---- DASHBOARD ----
@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", apartments=apartments)


# ---- UPDATE STATUS ----
@app.route("/update", methods=["POST"])
@login_required
def update():
    apt_id = int(request.form["id"])
    new_status = request.form["status"]

    for apt in apartments:
        if apt["id"] == apt_id:
            apt["status"] = new_status

    return redirect(url_for("dashboard"))


# ---- CALENDAR ----
@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


# ---- RUN ----
if __name__ == "__main__":
    app.run(debug=True)
