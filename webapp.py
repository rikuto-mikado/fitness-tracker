import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import pandas as pd
import os
from datetime import datetime, date

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:password@localhost:5432/fitness_db"
)


def get_db_connection():
    """Get PostgreSQL connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None


def load_users():
    """Load all users"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = "SELECT id, username, email, age, height_cm FROM users"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def load_weight_data(user_id):
    """Load weight data for a specific user"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = """
    SELECT weight_kg, recorded_date, notes 
    FROM weight_records 
    WHERE user_id = %s 
    ORDER BY recorded_date
    """
    df = pd.read_sql(query, conn, params=[user_id])
    conn.close()
    return df


def load_workout_data(user_id):
    """Load workout data for a specific user"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = """
    SELECT ws.workout_date, et.name as exercise_name, ws.duration_minutes, 
           ws.calories_burned, ws.intensity_level, et.category
    FROM workout_sessions ws
    JOIN exercise_types et ON ws.exercise_type_id = et.id
    WHERE ws.user_id = %s
    ORDER BY ws.workout_date DESC
    """
    df = pd.read_sql(query, conn, params=[user_id])
    conn.close()
    return df
