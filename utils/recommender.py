def generate_recommendations(df):
    recommendations = []

    if df.empty:
        return ["No study data available. Start by logging your first session!"]

    avg_break = df["break_time"].mean()
    avg_study = df["study_time"].mean()
    mood_mode = df["mood"].mode().iloc[0] if not df["mood"].mode().empty else "Neutral"
    top_subject = df["subject"].mode().iloc[0] if not df["subject"].mode().empty else None

    if avg_break > 20:
        recommendations.append("Your average break time is high. Try reducing breaks for better continuity.")
    if avg_study < 2:
        recommendations.append("Your average study session is low. Add more focused sessions daily.")
    if mood_mode == "Tired":
        recommendations.append("You often feel tired. Start with light subjects and shorter sessions.")
    if top_subject and (df["subject"] == top_subject).sum() > len(df) * 0.6:
        recommendations.append("You are repeatedly studying one subject. Rotate subjects for balanced learning.")

    if not recommendations:
        recommendations.append("Great work! Your study pattern looks balanced. Keep it up!")

    return recommendations