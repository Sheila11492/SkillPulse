import pandas as pd


def activities_to_dataframe(activities):
    df = pd.DataFrame(
        activities,
        columns=["date", "activity_type", "duration", "energy", "notes"]
    )
    df["date"] = pd.to_datetime(df["date"])
    return df

def generate_insights(df):
    insights = []

    # Actividad con más tiempo total
    top_activity = df.groupby("activity_type")["duration"].sum().idxmax()
    insights.append(f"⏱️ Pasas más tiempo en: {top_activity}")

    # Actividad con mayor energía promedio
    top_energy = df.groupby("activity_type")["energy"].mean().idxmax()
    insights.append(f"⚡ Te sientes más enérgica haciendo: {top_energy}")

    # Día más productivo
    day_productive = df.groupby("date")["duration"].sum().idxmax()
    insights.append(f"📅 Tu día más productivo fue: {day_productive}")

    return insights