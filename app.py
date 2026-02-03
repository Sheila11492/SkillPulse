import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from database import create_tables, insert_activity, get_activities
from models import Activity
from analytics import activities_to_dataframe, generate_insights

# --- Configuración inicial ---
st.set_page_config(page_title="SkillPulse", layout="centered")
create_tables()

# --- Logo ---
logo = Image.open("skillpulse-logo.png")
st.image(logo, width=150)  # Ajusta el tamaño si quieres más grande o más pequeño

# --- Encabezado estilo portfolio ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>SkillPulse</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Analizador de hábitos y productividad</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>Proyecto en Python para portfolio junior 🚀</p>", unsafe_allow_html=True)

# --- Formulario ---
st.divider()
st.header("➕ Añadir actividad")

with st.form("activity_form"):
    date = st.date_input("Fecha")
    activity_type = st.selectbox(
        "Tipo de actividad",
        ["Estudio", "Ejercicio", "Lectura", "Trabajo", "Otro"]
    )
    duration = st.number_input("Duración (minutos)", min_value=1)
    energy = st.slider("Nivel de energía", 1, 5)
    notes = st.text_area("Notas")

    submitted = st.form_submit_button("Guardar actividad")

    if submitted:
        activity = Activity(
            date=str(date),
            activity_type=activity_type,
            duration=duration,
            energy=energy,
            notes=notes
        )
        insert_activity(activity)
        st.success("Actividad guardada correctamente ✅")

# --- Leer actividades ---
activities = get_activities()

if activities:
    df = activities_to_dataframe(activities)

    # --- Insights automáticos ---
    st.divider()
    st.header("💡 Insights automáticos")
    insights = generate_insights(df)
    for i in insights:
        st.markdown(
            f"<div style='background-color:#E3F2FD; padding:10px; border-radius:8px; margin-bottom:5px;'>{i}</div>",
            unsafe_allow_html=True
        )

    # --- Dashboard en columnas ---
    st.divider()
    st.header("📊 Dashboard de actividades")
    col1, col2 = st.columns(2)

    # Gráfico 1: Tiempo total por actividad
    with col1:
        st.subheader("⏱️ Tiempo total")
        grouped = df.groupby("activity_type")["duration"].sum()
        grouped.index.name = "Actividad"
        fig, ax = plt.subplots(figsize=(4, 3))
        grouped.plot(kind="bar", ax=ax, color="#4CAF50")
        ax.set_ylabel("Minutos", fontsize=10)
        ax.set_xlabel("Actividad", fontsize=10)
        ax.tick_params(axis='x', rotation=30)
        ax.set_title("Tiempo total por actividad", fontsize=12, color="#333")
        st.pyplot(fig)

    # Gráfico 2: Energía media por actividad
    with col2:
        st.subheader("⚡ Energía media")
        energy_avg = df.groupby("activity_type")["energy"].mean()
        energy_avg.index.name = "Actividad"
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        energy_avg.plot(kind="bar", ax=ax2, color="#FF9800")
        ax2.set_ylabel("Nivel medio de energía", fontsize=10)
        ax2.set_xlabel("Actividad", fontsize=10)
        ax2.tick_params(axis='x', rotation=30)
        ax2.set_title("Energía media por actividad", fontsize=12, color="#333")
        st.pyplot(fig2)

    # --- Listado de actividades en tarjetas ---
    st.divider()
    st.header("📋 Actividades registradas")

    for activity in activities:
        with st.container():
            st.markdown(
                f"""
                <div style='
                    border:1px solid #ddd; 
                    border-radius:12px; 
                    padding:12px; 
                    margin-bottom:8px; 
                    background-color:#fefefe;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                '>
                <strong>📅 Fecha:</strong> {activity[0]} <br>
                <strong>🧩 Actividad:</strong> {activity[1]} <br>
                <strong>⏱️ Duración:</strong> {activity[2]} min <br>
                <strong>⚡ Energía:</strong> {activity[3]}/5 <br>
                <strong>📝 Notas:</strong> {activity[4] if activity[4] else "-"}
                </div>
                """,
                unsafe_allow_html=True
            )

else:
    st.info("Aún no hay actividades registradas.")