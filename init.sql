\c fitness_db;

-- User table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INTEGER,
    height_cm FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weight records table
CREATE TABLE weight_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    weight_kg FLOAT NOT NULL,
    recorded_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exercise types table
CREATE TABLE exercise_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),
    calories_per_minute FLOAT
);

-- Workout sessions table
CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_type_id INTEGER REFERENCES exercise_types(id),
    duration_minutes INTEGER NOT NULL,
    calories_burned INTEGER,
    intensity_level VARCHAR(20),
    workout_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goals table
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    goal_type VARCHAR(50) NOT NULL,
    target_value FLOAT,
    current_value FLOAT DEFAULT 0,
    target_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email, age, height_cm) VALUES
('john_doe', 'john@example.com', 28, 175),
('jane_smith', 'jane@example.com', 25, 165),
('mike_johnson', 'mike@example.com', 32, 180);

INSERT INTO exercise_types (name, category, calories_per_minute) VALUES
('Running', 'Cardio', 12.0),
('Walking', 'Cardio', 5.0),
('Cycling', 'Cardio', 8.0),
('Push-ups', 'Strength', 7.0),
('Pull-ups', 'Strength', 9.0),
('Squats', 'Strength', 6.0),
('Yoga', 'Flexibility', 3.0),
('Swimming', 'Cardio', 11.0);

INSERT INTO weight_records (user_id, weight_kg, recorded_date, notes) VALUES
(1, 75.2, '2024-08-01', 'Starting weight'),
(1, 74.8, '2024-08-08', 'Down 0.4kg'),
(1, 74.5, '2024-08-15', 'Good progress'),
(1, 74.1, '2024-08-22', 'Feeling great'),
(2, 60.5, '2024-08-01', 'Starting weight'),
(2, 60.2, '2024-08-08', 'Slight decrease'),
(2, 59.8, '2024-08-15', 'On track'),
(3, 82.0, '2024-08-01', 'Starting weight'),
(3, 81.5, '2024-08-08', 'Good start');

INSERT INTO workout_sessions (user_id, exercise_type_id, duration_minutes, calories_burned, intensity_level, workout_date) VALUES
(1, 1, 30, 360, 'high', '2024-08-20'),
(1, 4, 15, 105, 'medium', '2024-08-21'),
(1, 6, 20, 120, 'medium', '2024-08-22'),
(2, 2, 45, 225, 'low', '2024-08-20'),
(2, 7, 60, 180, 'low', '2024-08-21'),
(3, 3, 40, 320, 'medium', '2024-08-20'),
(3, 5, 10, 90, 'high', '2024-08-21');

INSERT INTO goals (user_id, goal_type, target_value, current_value, target_date) VALUES
(1, 'weight_loss', 72.0, 74.1, '2024-12-31'),
(2, 'weight_maintenance', 60.0, 59.8, '2024-12-31'),
(3, 'muscle_gain', 85.0, 81.5, '2025-03-31');