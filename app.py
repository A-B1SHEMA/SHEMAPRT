from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET"

# ---- Users ----
users = {
    "admin": generate_password_hash("admin123")
}

# ---- Apartments ----
apartments = [
    {"id": 1, "name": "A1", "type": "1 Bedroom", "status": "Available", "bookings": []},
    {"id": 2, "name": "A2", "type": "1 Bedroom", "status": "Available", "bookings": []},
    {"id": 3, "name": "B1", "type": "2 Bedroom", "status": "Available", "bookings": []},
    {"id": 4, "name": "B2", "type": "2 Bedroom", "status": "Available", "bookings": []},
    {"id": 5, "name": "B3", "type": "2 Bedroom", "status": "Available", "bookings": []},
    {"id": 6, "name": "B4", "type": "2 Bedroom", "status": "Available", "bookings": []},
    {"id": 7, "name": "C1", "type": "3 Bedroom", "status": "Available", "bookings": []},
]

# ---- Login decorator ----
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ---- Routes ----
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
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

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", apartments=apartments)

@app.route("/update_booking", methods=["POST"])
@login_required
def update_booking():
    apt_id = int(request.form.get("apt_id"))
    status = request.form.get("status")
    start = request.form.get("start_date")
    end = request.form.get("end_date")
    price = float(request.form.get("price"))
    deposit = float(request.form.get("deposit"))

    # Find apartment
    apt = next((a for a in apartments if a["id"] == apt_id), None)
    if not apt:
        return "Apartment not found", 404

    # Check availability (no overlap)
    for b in apt.get("bookings", []):
        if (start <= b["end"] and end >= b["start"]):
            return "Error: dates overlap with existing booking", 400

    # Add booking
    apt["bookings"].append({
        "start": start,
        "end": end,
        "status": status,
        "price": price,
        "deposit": deposit
    })

    # Update apartment current status if latest booking
    apt["status"] = status

    return redirect(url_for("dashboard"))

@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")

@app.route("/get_bookings")
@login_required
def get_bookings():
    events = []
    for apt in apartments:
        for b in apt.get("bookings", []):
            color = "green" if b["status"]=="Available" else ("red" if b["status"]=="Reserved" else "orange")
