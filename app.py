from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
from datetime import datetime
from utils.analyzer import (
    ensure_files_exist,
    load_user_data,
    append_study_session,
    get_dashboard_metrics,
    generate_graphs,
    get_advanced_analytics,
    get_goal_progress,
    export_filtered_report,
    register_user,
    authenticate_user,
    recalculate_efficiency_for_existing_rows,  # ✅ added
)
from utils.recommender import generate_recommendations
from utils.streak_tracker import calculate_streak

app = Flask(__name__)
app.secret_key = "studysense_secret_key_2026"

DATA_FILE = "study_data.csv"
USERS_FILE = "users.csv"
GRAPH_DIR = os.path.join("static", "graphs")

# ✅ One-time flag so old wrong efficiency values are fixed only once
EFFICIENCY_FIX_DONE = False


@app.before_request
def setup():
    global EFFICIENCY_FIX_DONE
    ensure_files_exist(DATA_FILE, USERS_FILE, GRAPH_DIR)

    # ✅ one-time data correction for old rows
    if not EFFICIENCY_FIX_DONE:
        fixed = recalculate_efficiency_for_existing_rows(DATA_FILE)
        print(f"✅ Efficiency migration done. Fixed rows: {fixed}")
        EFFICIENCY_FIX_DONE = True


def login_required():
    return "username" in session


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def home():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("home.html", username=session["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter username and password.", "danger")
            return redirect(url_for("login"))

        if authenticate_user(USERS_FILE, username, password):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter username and password.", "danger")
            return redirect(url_for("register"))

        success, msg = register_user(USERS_FILE, username, password)
        flash(msg, "success" if success else "danger")

        if success:
            return redirect(url_for("login"))
        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/log-session", methods=["GET", "POST"])
def log_session():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        username = session["username"]
        subject = request.form.get("subject", "").strip()
        study_time = to_float(request.form.get("study_time"), 0.0)
        break_time = to_float(request.form.get("break_time"), 0.0)
        start_time = request.form.get("start_time", "").strip()
        difficulty = request.form.get("difficulty", "").strip()
        mood = request.form.get("mood", "").strip()
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")

        if not subject:
            flash("Subject is required.", "danger")
            return redirect(url_for("log_session"))

        append_study_session(
            DATA_FILE,
            username,
            date,
            subject,
            study_time,
            break_time,
            start_time,
            difficulty,
            mood
        )
        flash("Study session logged successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("log_session.html")


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    username = session["username"]
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    daily_goal = to_float(request.args.get("daily_goal"), 4.0)

    df = load_user_data(DATA_FILE, username, start_date, end_date)
    metrics = get_dashboard_metrics(df)
    streak_days = calculate_streak(df)

    # use selected end_date for goal progress context
    goal_progress = get_goal_progress(df, daily_goal, end_date)

    return render_template(
        "dashboard.html",
        username=username,
        metrics=metrics,
        streak_days=streak_days,
        goal_progress=goal_progress,
        daily_goal=daily_goal,
        start_date=start_date or "",
        end_date=end_date or ""
    )


@app.route("/analytics")
def analytics():
    if not login_required():
        return redirect(url_for("login"))

    username = session["username"]
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    df = load_user_data(DATA_FILE, username, start_date, end_date)
    graph_paths = generate_graphs(df, username, GRAPH_DIR)
    advanced = get_advanced_analytics(df)

    return render_template(
        "analytics.html",
        username=username,
        graph_paths=graph_paths,
        advanced=advanced,
        start_date=start_date or "",
        end_date=end_date or ""
    )


@app.route("/recommendations")
def recommendations():
    if not login_required():
        return redirect(url_for("login"))

    username = session["username"]
    df = load_user_data(DATA_FILE, username)
    recs = generate_recommendations(df)
    return render_template("recommendations.html", recommendations=recs, username=username)


@app.route("/export-report")
def export_report():
    if not login_required():
        return redirect(url_for("login"))

    username = session["username"]
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    output_file = export_filtered_report(DATA_FILE, username, start_date, end_date)
    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)