import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib


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


def append_study_session(data_file, username, date, subject, study_time, break_time, start_time, difficulty, mood):
    eff = (study_time / (study_time + break_time) * 100) if (study_time + break_time) > 0 else 0
    row = pd.DataFrame([{
        "username": username,
        "date": date,
        "subject": subject,
        "study_time": study_time,
        "break_time": break_time,
        "start_time": start_time,
        "difficulty": difficulty,
        "mood": mood,
        "efficiency": round(eff, 2)
    }])

    df = pd.read_csv(data_file)
    df = pd.concat([df, row], ignore_index=True)
    df.to_csv(data_file, index=False)


def load_user_data(data_file, username, start_date=None, end_date=None):
    df = pd.read_csv(data_file)
    if df.empty:
        return df

    df = df[df["username"] == username].copy()
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    return df


def get_dashboard_metrics(df):
    if df.empty:
        return {
            "total_hours": 0,
            "most_subject": "N/A",
            "avg_break": 0,
            "avg_efficiency": 0
        }

    total_hours = round(df["study_time"].sum(), 2)
    most_subject = df["subject"].mode().iloc[0] if not df["subject"].mode().empty else "N/A"
    avg_break = round(df["break_time"].mean(), 2)
    avg_efficiency = round(df["efficiency"].mean(), 2)

    return {
        "total_hours": total_hours,
        "most_subject": most_subject,
        "avg_break": avg_break,
        "avg_efficiency": avg_efficiency
    }


def get_goal_progress(df, daily_goal):
    if df.empty:
        return {"today_hours": 0, "daily_goal": daily_goal, "percent": 0}

    today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))
    today_df = df[df["date"] == today]
    today_hours = round(today_df["study_time"].sum(), 2)
    percent = round(min((today_hours / daily_goal) * 100, 100), 2) if daily_goal > 0 else 0

    return {"today_hours": today_hours, "daily_goal": daily_goal, "percent": percent}


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

    weekly_trend = "Increasing" if len(weekly) > 1 and weekly.iloc[-1] >= weekly.iloc[-2] else "Needs Improvement"
    monthly_trend = "Increasing" if len(monthly) > 1 and monthly.iloc[-1] >= monthly.iloc[-2] else "Needs Improvement"

    mood_map = {"Tired": 1, "Neutral": 2, "Focused": 3, "Motivated": 4}
    dfx["mood_score"] = dfx["mood"].map(mood_map).fillna(2)
    mood_correlation = round(dfx["mood_score"].corr(dfx["study_time"]), 2) if len(dfx) > 1 else 0

    time_group = dfx.groupby("start_time")["efficiency"].mean()
    best_study_time = time_group.idxmax() if not time_group.empty else "N/A"

    return {
        "weekly_trend": weekly_trend,
        "monthly_trend": monthly_trend,
        "mood_correlation": mood_correlation,
        "best_study_time": best_study_time
    }


def generate_graphs(df, username, graph_dir):
    paths = {}
    if df.empty:
        return paths

    plt.style.use("seaborn-v0_8-darkgrid")

    # 1) Line chart - study over time + moving average
    daily = df.groupby("date")["study_time"].sum().sort_index()
    moving_avg = daily.rolling(window=3).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(daily.index, daily.values, marker="o", linewidth=2, label="Daily Hours")
    plt.plot(moving_avg.index, moving_avg.values, linestyle="--", linewidth=2, label="3-Day Moving Avg")
    plt.title("Study Hours Over Time", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    line_path = os.path.join(graph_dir, f"{username}_line_trend.png")
    plt.savefig(line_path)
    plt.close()
    paths["line_trend"] = line_path.replace("\\", "/")

    # 2) Pie chart - subject distribution
    subj = df.groupby("subject")["study_time"].sum()
    plt.figure(figsize=(7, 7))
    plt.pie(subj.values, labels=subj.index, autopct="%1.1f%%", startangle=140)
    plt.title("Subject Distribution", fontsize=14, fontweight="bold")
    pie_path = os.path.join(graph_dir, f"{username}_subject_pie.png")
    plt.savefig(pie_path)
    plt.close()
    paths["subject_pie"] = pie_path.replace("\\", "/")

    # 3) Bar chart - daily study time
    plt.figure(figsize=(10, 5))
    plt.bar(daily.index.astype(str), daily.values)
    plt.title("Daily Study Time", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.xticks(rotation=45)
    plt.tight_layout()
    bar_path = os.path.join(graph_dir, f"{username}_daily_bar.png")
    plt.savefig(bar_path)
    plt.close()
    paths["daily_bar"] = bar_path.replace("\\", "/")

    return paths


def export_filtered_report(data_file, username, start_date=None, end_date=None):
    df = load_user_data(data_file, username, start_date, end_date)
    out_name = f"weekly_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(out_name, index=False)
    return out_name