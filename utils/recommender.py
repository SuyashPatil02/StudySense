def generate_recommendations(df):
    recommendations = []

    # ✅ 1. If no data
    if df.empty:
        return ["No study data available. Start logging your study sessions."]

    # ✅ 2. Basic metrics
    avg_break = df["break_time"].mean()
    avg_study = df["study_time"].mean()

    mood_mode = df["mood"].mode()
    mood_mode = mood_mode.iloc[0] if not mood_mode.empty else "Neutral"

    subject_mode = df["subject"].mode()
    top_subject = subject_mode.iloc[0] if not subject_mode.empty else None

    total_sessions = len(df)

    # ✅ 3. Rules-based recommendations

    # 🔹 High break time
    if avg_break > 20:
        recommendations.append("Reduce your break time to improve focus continuity.")

    # 🔹 Low study time
    if avg_study < 2:
        recommendations.append("Increase your daily study duration for better progress.")

    # 🔹 Mood-based suggestion
    if mood_mode == "Tired":
        recommendations.append("You often feel tired. Start with light subjects and shorter sessions.")

    # 🔹 Subject repetition
    if top_subject:
        subject_count = (df["subject"] == top_subject).sum()
        if subject_count > total_sessions * 0.6:
            recommendations.append("You are focusing too much on one subject. Try rotating subjects.")

    # ✅ 4. If everything is balanced
    if not recommendations:
        recommendations.append("Great job! Your study pattern is balanced. Keep it up!")

    return recommendations