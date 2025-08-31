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
