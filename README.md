# Fitness Tracker

This is a simple web application for tracking fitness data, including weight, workouts, and goals. The application is built with Python using the Streamlit framework and uses a PostgreSQL database to store data.

## Features

*   **User Management:** Supports multiple users.
*   **Weight Tracking:** Log and visualize weight changes over time.
*   **Workout Logging:** Record workout sessions, including exercise type, duration, calories burned, and intensity.
*   **Goal Setting:** Set and track fitness goals (e.g., weight loss, muscle gain).
*   **Dashboard:** A comprehensive dashboard to visualize key fitness metrics and progress.
*   **Data Persistence:** Data is stored in a PostgreSQL database.

## Technologies Used

*   **Backend:** Python
*   **Web Framework:** Streamlit
*   **Database:** PostgreSQL
*   **Containerization:** Docker, Docker Compose
*   **Libraries:**
    *   `pandas` for data manipulation
    *   `psycopg2-binary` for PostgreSQL connection
    *   `plotly` for interactive charts

## Prerequisites

*   Docker
*   Docker Compose

## Installation and Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd fitness-tracker
    ```

2.  **Run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image for the web application, start the PostgreSQL database, and run the application.

3.  **Access the application:**
    *   **Fitness Tracker App:** Open your web browser and go to `http://localhost:8501`
    *   **pgAdmin (Database Management):** Open your web browser and go to `http://localhost:8080`
        *   **Email:** `admin@example.com`
        *   **Password:** `admin`

    When setting up the server in pgAdmin, use `db` as the hostname.

## Database Schema

The database consists of the following tables:

*   `users`: Stores user information.
*   `weight_records`: Stores weight records for each user.
*   `exercise_types`: Stores different types of exercises.
*   `workout_sessions`: Stores workout session details.
*   `goals`: Stores user-defined fitness goals.

For more details, see the `init.sql` file.
