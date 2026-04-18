import os
import hashlib
from datetime import datetime

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ==============================
# FILE SETUP
# ==============================
def ensure_files_exist(data_file, users_file, graph_dir):
    if not os.path.exists(data_file):
        df = pd.DataFrame(columns=[
            "username", "date", "subject", "study_time", "break_time",
            "start_time", "difficulty", "mood", "efficiency"
        ])
        df.to_csv(data_file, index=False)

    if not os.path.exists(users_file):
        udf = pd.DataFrame(columns=["username", "password_hash"])
        udf.to_csv(users_file, index=False)

    os.makedirs(graph_dir, exist_ok=True)


# ==============================
# AUTH FUNCTIONS
# ==============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(users_file, username, password):
    users_df = pd.read_csv(users_file)

    if username in users_df["username"].astype(str).values:
        return False, "Username already exists. Please login."

    new_user = pd.DataFrame([{
        "username": username,
        "password_hash": hash_password(password)
    }])

    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(users_file, index=False)

    return True, "Registration successful! Please login."


def authenticate_user(users_file, username, password):
    users_df = pd.read_csv(users_file)
    user_row = users_df[users_df["username"] == username]

    if user_row.empty:
        return False

    return user_row.iloc[0]["password_hash"] == hash_password(password)


# ==============================
# HELPER FUNCTIONS
# ==============================
def _safe_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


# ==============================
# 🔥 CORRECT EFFICIENCY FUNCTION
# ==============================
def _calc_efficiency(study_time_hours, break_time_minutes):
    study_h = _safe_float(study_time_hours, 0.0)
    break_m = _safe_float(break_time_minutes, 0.0)

    # ✅ Convert minutes → hours
    break_h = break_m / 60.0

    total_h = study_h + break_h
    if total_h <= 0:
        return 0.0

    efficiency = (study_h / total_h) * 100

    # Clamp between 0–100
    return round(min(max(efficiency, 0.0), 100.0), 2)


# ==============================
# ADD STUDY SESSION
# ==============================
def append_study_session(data_file, username, date, subject,
                         study_time, break_time, start_time, difficulty, mood):

    study_time = _safe_float(study_time, 0.0)  # hours
    break_time = _safe_float(break_time, 0.0)  # minutes

    # ✅ Correct efficiency calculation
    efficiency = _calc_efficiency(study_time, break_time)

    row = pd.DataFrame([{
        "username": username,
        "date": date,
        "subject": subject,
        "study_time": study_time,
        "break_time": break_time,
        "start_time": start_time,
        "difficulty": difficulty,
        "mood": mood,
        "efficiency": efficiency
    }])

    df = pd.read_csv(data_file)
    df = pd.concat([df, row], ignore_index=True)
    df.to_csv(data_file, index=False)


# ==============================
# LOAD USER DATA
# ==============================
def load_user_data(data_file, username, start_date=None, end_date=None):
    df = pd.read_csv(data_file)

    if df.empty:
        return df

    df = df[df["username"] == username].copy()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["study_time"] = pd.to_numeric(df["study_time"], errors="coerce").fillna(0)
    df["break_time"] = pd.to_numeric(df["break_time"], errors="coerce").fillna(0)
    df["efficiency"] = pd.to_numeric(df["efficiency"], errors="coerce").fillna(0)

    df = df.dropna(subset=["date"])

    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]

    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    return df


# ==============================
# 🔥 FIX OLD WRONG DATA
# ==============================
def recalculate_efficiency_for_existing_rows(data_file, username=None):
    df = pd.read_csv(data_file)

    if df.empty:
        return 0

    df["study_time"] = pd.to_numeric(df["study_time"], errors="coerce").fillna(0)
    df["break_time"] = pd.to_numeric(df["break_time"], errors="coerce").fillna(0)

    if username:
        mask = df["username"].astype(str) == str(username)
    else:
        mask = pd.Series([True] * len(df))

    df.loc[mask, "efficiency"] = df.loc[mask].apply(
        lambda r: _calc_efficiency(r["study_time"], r["break_time"]),
        axis=1
    )

    df.to_csv(data_file, index=False)

    return int(mask.sum())


# ==============================
# DASHBOARD METRICS
# ==============================
def get_dashboard_metrics(df):
    if df.empty:
        return {
            "total_hours": 0,
            "most_subject": "N/A",
            "avg_break": 0,
            "avg_efficiency": 0
        }

    total_hours = round(df["study_time"].sum(), 2)

    most_subject = (
        df["subject"].mode().iloc[0]
        if not df["subject"].mode().empty else "N/A"
    )

    avg_break = round(df["break_time"].mean(), 2)
    avg_efficiency = round(df["efficiency"].mean(), 2)

    return {
        "total_hours": total_hours,
        "most_subject": most_subject,
        "avg_break": avg_break,
        "avg_efficiency": avg_efficiency
    }


# ==============================
# GOAL PROGRESS
# ==============================
def get_goal_progress(df, daily_goal, end_date=None):
    target_date = end_date if end_date else datetime.now().strftime("%Y-%m-%d")

    daily_goal = _safe_float(daily_goal, 0.0) 

    if df.empty:
        return {
            "today_hours": 0,  
            "daily_goal": daily_goal,
            "percent": 0,
            "target_date": target_date
        }      

    target_ts = pd.Timestamp(target_date)

    today_df = df[df["date"] == target_ts]
    today_hours = round(today_df["study_time"].sum(), 2)

    percent = (
        round((today_hours / daily_goal) * 100, 2)
        if daily_goal > 0 else 0         
    )

    percent = min(percent, 100)

    return {
        "today_hours": today_hours,
        "daily_goal": daily_goal,
        "percent": percent,
        "target_date": target_date
    }


# ==============================
# ADVANCED ANALYTICS
# ==============================
def get_advanced_analytics(df):
    if df.empty:
        return {
            "weekly_trend": "N/A",
            "monthly_trend": "N/A",
            "mood_correlation": 0,
            "best_study_time": "N/A"
        }

    dfx = df.copy()

    dfx["week"] = dfx["date"].dt.to_period("W").astype(str)
    dfx["month"] = dfx["date"].dt.to_period("M").astype(str)

    weekly = dfx.groupby("week")["study_time"].sum()
    monthly = dfx.groupby("month")["study_time"].sum()

    weekly_trend = (
        "Increasing"
        if len(weekly) > 1 and weekly.iloc[-1] >= weekly.iloc[-2]
        else "Needs Improvement"
    )

    monthly_trend = (
        "Increasing"
        if len(monthly) > 1 and monthly.iloc[-1] >= monthly.iloc[-2]
        else "Needs Improvement"
    )

    mood_map = {"Tired": 1, "Neutral": 2, "Focused": 3, "Motivated": 4}
    dfx["mood_score"] = dfx["mood"].map(mood_map).fillna(2)

    mood_correlation = (
        round(dfx["mood_score"].corr(dfx["study_time"]), 2)
        if len(dfx) > 1 else 0
    )

    time_group = dfx.groupby("start_time")["efficiency"].mean()
    best_study_time = time_group.idxmax() if not time_group.empty else "N/A"

    return {
        "weekly_trend": weekly_trend,
        "monthly_trend": monthly_trend,
        "mood_correlation": mood_correlation,
        "best_study_time": best_study_time
    }


# ==============================
# GRAPH GENERATION
# ==============================
def generate_graphs(df, username, graph_dir):
    paths = {}

    if df.empty:
        return paths

    plt.style.use("seaborn-v0_8-darkgrid")

    # Line Chart
    daily = df.groupby("date")["study_time"].sum().sort_index()
    moving_avg = daily.rolling(window=3).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(daily.index, daily.values, marker="o", label="Daily Hours")
    plt.plot(moving_avg.index, moving_avg.values, linestyle="--", label="3-Day Avg")
    plt.title("Study Trend")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    line_path = os.path.join(graph_dir, f"{username}_line_trend.png")
    plt.savefig(line_path)
    plt.close()

    paths["line_trend"] = line_path.replace("\\", "/")

    # Pie Chart
    subj = df.groupby("subject")["study_time"].sum()

    plt.figure()
    plt.pie(subj.values, labels=subj.index, autopct="%1.1f%%")
    plt.title("Subject Distribution")

    pie_path = os.path.join(graph_dir, f"{username}_subject_pie.png")
    plt.savefig(pie_path)
    plt.close()

    paths["subject_pie"] = pie_path.replace("\\", "/")

    # Bar Chart
    plt.figure()
    plt.bar(daily.index.astype(str), daily.values)
    plt.xticks(rotation=45)
    plt.title("Daily Study Time")

    bar_path = os.path.join(graph_dir, f"{username}_daily_bar.png")
    plt.savefig(bar_path)
    plt.close()

    paths["daily_bar"] = bar_path.replace("\\", "/")

    return paths


# ==============================
# EXPORT CSV
# ==============================
def export_filtered_report(data_file, username, start_date=None, end_date=None):
    df = load_user_data(data_file, username, start_date, end_date)

    out_name = f"report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(out_name, index=False)

    return out_name