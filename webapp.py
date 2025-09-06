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


def load_goals(user_id):
    """Load goals for a specific user"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = """
    SELECT goal_type, target_value, current_value, target_date, status
    FROM goals 
    WHERE user_id = %s
    """
    df = pd.read_sql(query, conn, params=[user_id])
    conn.close()
    return df


def load_exercise_types():
    """Load all exercise types"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = "SELECT id, name, category, calories_per_minute FROM exercise_types"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def add_weight_record(user_id, weight, date_recorded, notes=""):
    """Add a new weight record"""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO weight_records (user_id, weight_kg, recorded_date, notes)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, weight, date_recorded, notes))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error adding weight record: {e}")
        conn.close()
        return False


def add_workout_session(
    user_id, exercise_type_id, duration, calories, intensity, workout_date, notes=""
):
    """Add a new workout session"""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO workout_sessions (user_id, exercise_type_id, duration_minutes, 
                                    calories_burned, intensity_level, workout_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                user_id,
                exercise_type_id,
                duration,
                calories,
                intensity,
                workout_date,
                notes,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error adding workout session: {e}")
        conn.close()
        return False


def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Fitness Tracker", page_icon="💪", layout="wide")

    st.title("💪 Fitness Tracker Dashboard")
    st.markdown("---")

    # Load users
    users_df = load_users()
    if users_df.empty:
        st.error("No users found in database")
        return

    # User selection
    st.sidebar.header("👤 User Selection")
    user_options = {
        f"{row['username']} ({row['email']})": row["id"]
        for _, row in users_df.iterrows()
    }
    selected_user = st.sidebar.selectbox("Select User", list(user_options.keys()))
    user_id = user_options[selected_user]

    # Get user info
    user_info = users_df[users_df["id"] == user_id].iloc[0]
    st.sidebar.markdown(f"**Age:** {user_info['age']}")
    st.sidebar.markdown(f"**Height:** {user_info['height_cm']} cm")

    # Navigation
    st.sidebar.header("📊 Navigation")
    tab = st.sidebar.radio(
        "Choose Section",
        ["Dashboard", "Weight Tracking", "Workout Log", "Goals", "Add Records"],
    )

    if tab == "Dashboard":
        show_dashboard(user_id)
    elif tab == "Weight Tracking":
        show_weight_tracking(user_id)
    elif tab == "Workout Log":
        show_workout_log(user_id)
    elif tab == "Goals":
        show_goals(user_id)
    elif tab == "Add Records":
        show_add_records(user_id)


def show_dashboard(user_id):
    """Show main dashboard"""
    st.header("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    # Load data
    weight_df = load_weight_data(user_id)
    workout_df = load_workout_data(user_id)
    goals_df = load_goals(user_id)

    # Metrics
    with col1:
        if not weight_df.empty:
            current_weight = weight_df.iloc[-1]["weight_kg"]
            st.metric("Current Weight", f"{current_weight} kg")
        else:
            st.metric("Current Weight", "No data")

    with col2:
        if not workout_df.empty:
            total_workouts = len(workout_df)
            st.metric("Total Workouts", total_workouts)
        else:
            st.metric("Total Workouts", "0")

    with col3:
        if not workout_df.empty:
            total_calories = workout_df["calories_burned"].sum()
            st.metric("Total Calories Burned", f"{total_calories:,}")
        else:
            st.metric("Total Calories Burned", "0")

    with col4:
        active_goals = len(goals_df[goals_df["status"] == "active"])
        st.metric("Active Goals", active_goals)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        if not weight_df.empty:
            st.subheader("📈 Weight Progress")
            fig = px.line(
                weight_df, x="recorded_date", y="weight_kg", title="Weight Over Time"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No weight data available")

    with col2:
        if not workout_df.empty:
            st.subheader("🏃‍♂️ Workout Categories")
            category_counts = workout_df["category"].value_counts()
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Workout Distribution by Category",
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workout data available")


def show_weight_tracking(user_id):
    """Show weight tracking section"""
    st.header("⚖️ Weight Tracking")

    weight_df = load_weight_data(user_id)

    if not weight_df.empty:
        # Weight progress chart
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=weight_df["recorded_date"],
                y=weight_df["weight_kg"],
                mode="lines+markers",
                name="Weight",
                line=dict(color="#1f77b4", width=3),
                marker=dict(size=8),
            )
        )

        fig.update_layout(
            title="Weight Progress Over Time",
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Weight statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            min_weight = weight_df["weight_kg"].min()
            st.metric("Minimum Weight", f"{min_weight} kg")

        with col2:
            max_weight = weight_df["weight_kg"].max()
            st.metric("Maximum Weight", f"{max_weight} kg")

        with col3:
            weight_change = (
                weight_df.iloc[-1]["weight_kg"] - weight_df.iloc[0]["weight_kg"]
            )
            st.metric("Total Change", f"{weight_change:+.1f} kg")

        # Weight records table
        st.subheader("📋 Weight Records")
        st.dataframe(
            weight_df.sort_values("recorded_date", ascending=False),
            use_container_width=True,
        )

    else:
        st.info("No weight data available. Add some records to see your progress!")


def show_workout_log(user_id):
    """Show workout log section"""
    st.header("🏋️‍♀️ Workout Log")

    workout_df = load_workout_data(user_id)

    if not workout_df.empty:
        # Recent workouts
        st.subheader("📅 Recent Workouts")
        recent_workouts = workout_df.head(10)
        st.dataframe(recent_workouts, use_container_width=True)

        # Workout analytics
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔥 Calories by Exercise")
            calories_by_exercise = (
                workout_df.groupby("exercise_name")["calories_burned"]
                .sum()
                .sort_values(ascending=True)
            )
            fig = px.bar(
                x=calories_by_exercise.values,
                y=calories_by_exercise.index,
                orientation="h",
                title="Total Calories Burned by Exercise Type",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("⏱️ Workout Duration Trends")
            daily_duration = (
                workout_df.groupby("workout_date")["duration_minutes"]
                .sum()
                .reset_index()
            )
            fig = px.bar(
                daily_duration,
                x="workout_date",
                y="duration_minutes",
                title="Daily Workout Duration",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Intensity distribution
        st.subheader("💪 Workout Intensity Distribution")
        intensity_counts = workout_df["intensity_level"].value_counts()
        fig = px.pie(
            values=intensity_counts.values,
            names=intensity_counts.index,
            title="Workout Intensity Levels",
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No workout data available. Start logging your workouts!")


def show_goals(user_id):
    """Show goals section"""
    st.header("🎯 Goals")

    goals_df = load_goals(user_id)

    if not goals_df.empty:
        for _, goal in goals_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.subheader(f"{goal['goal_type'].replace('_', ' ').title()}")
                    progress = (
                        (goal["current_value"] / goal["target_value"]) * 100
                        if goal["target_value"] > 0
                        else 0
                    )
                    st.progress(min(progress / 100, 1.0))
                    st.text(
                        f"Progress: {goal['current_value']:.1f} / {goal['target_value']:.1f}"
                    )

                with col2:
                    st.metric(
                        "Target Date",
                        (
                            goal["target_date"].strftime("%Y-%m-%d")
                            if goal["target_date"]
                            else "No date"
                        ),
                    )

                with col3:
                    status_color = "🟢" if goal["status"] == "active" else "🔴"
                    st.metric("Status", f"{status_color} {goal['status'].title()}")

                st.markdown("---")
    else:
        st.info("No goals set. Set some goals to track your progress!")


def show_add_records(user_id):
    """Show add records section"""
    st.header("➕ Add New Records")

    tab1, tab2 = st.tabs(["Add Weight Record", "Add Workout Session"])

    with tab1:
        st.subheader("⚖️ Add Weight Record")

        with st.form("weight_form"):
            col1, col2 = st.columns(2)

            with col1:
                weight = st.number_input(
                    "Weight (kg)", min_value=0.0, max_value=300.0, step=0.1
                )
                date_recorded = st.date_input("Date", value=date.today())

            with col2:
                notes = st.text_area("Notes (optional)")

            submitted = st.form_submit_button("Add Weight Record")

            if submitted and weight > 0:
                if add_weight_record(user_id, weight, date_recorded, notes):
                    st.success("Weight record added successfully!")
                    st.experimental_rerun()

    with tab2:
        st.subheader("🏋️‍♀️ Add Workout Session")

        exercise_types_df = load_exercise_types()

        if not exercise_types_df.empty:
            with st.form("workout_form"):
                col1, col2 = st.columns(2)

                with col1:
                    exercise_options = {
                        f"{row['name']} ({row['category']})": row["id"]
                        for _, row in exercise_types_df.iterrows()
                    }
                    selected_exercise = st.selectbox(
                        "Exercise Type", list(exercise_options.keys())
                    )
                    exercise_id = exercise_options[selected_exercise]

                    duration = st.number_input(
                        "Duration (minutes)", min_value=1, max_value=300, value=30
                    )
                    calories = st.number_input(
                        "Calories Burned", min_value=0, max_value=2000, value=100
                    )

                with col2:
                    intensity = st.selectbox(
                        "Intensity Level", ["low", "medium", "high"]
                    )
                    workout_date = st.date_input("Workout Date", value=date.today())
                    notes = st.text_area("Notes (optional)")

                submitted = st.form_submit_button("Add Workout Session")

                if submitted:
                    if add_workout_session(
                        user_id,
                        exercise_id,
                        duration,
                        calories,
                        intensity,
                        workout_date,
                        notes,
                    ):
                        st.success("Workout session added successfully!")
                        st.experimental_rerun()
        else:
            st.error("No exercise types found in database")


if __name__ == "__main__":
    main()
