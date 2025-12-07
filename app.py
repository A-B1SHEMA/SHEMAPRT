from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET"  # change this for security

# -------------------------
# Users
# -------------------------
users = {
    "admin": generate_password_hash("admin123")  # default admin user
}

# -------------------------
# Apartments
# -------------------------
apartments = [
    {"id": 1, "name": "A1", "type": "1 Bedroom", "status": "Available", "booked_date": "2025-12-10"},
    {"id": 2, "name": "A2", "type": "1 Bedroom", "status": "Reserved", "booked_date": "2025-12-11"},
    {"id": 3, "name": "B1", "type": "2 Bedroom", "status": "On Hold", "booked_date": "2025-12-12"},
    {"id": 4, "name": "B2", "type": "2 Bedroom", "status": "Available", "booked_date": "2025-12-13"},
    {"id": 5, "name": "B3", "type": "2 Bedroom", "status": "Available", "booked_date": "2025-12-14"},
    {"id": 6, "name": "B4", "type": "2 Bedroom", "status": "Reserved", "booked_date": "2025-12-15"},
    {"id": 7, "name": "C1", "type": "3 Bedroom", "status": "Available", "booked_date": "2025-12-16"},
]

# -------------------------
# Login required decorator
# -------------------------
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------
# Routes
# -------------------------

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

@app.route("/update", methods=["POST"])
@login_required
def update():
    apt_id = int(request.form.get("id"))
    new_status = request.form.get("status")
    new_date = request.form.get("booked_date", "")
    for apt in apartments:
        if apt["id"] == apt_id:
            apt["status"] = new_status
            if new_date:
                apt["booked_date"] = new_date
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
        color = "green" if apt["status"]=="Available" else ("red" if apt["status"]=="Reserved" else "orange")
        events.append({
            "title": f"{apt['name']} {apt['status']}",
            "start": apt.get("booked_date", "2025-12-10"),
            "color": color
        })
    return jsonify(events)

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    # host 0.0.0.0 allows access from Codespaces / network
    # port 8080 is easy to forward
    app.run(debug=True, host="0.0.0.0", port=8080)


# ---- RUN ----
if __name__ == "__main__":
    app.run(debug=True)

