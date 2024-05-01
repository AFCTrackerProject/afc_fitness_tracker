--AFC Fitness Offical Schema (last updated 4/30)

-- User Table
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female', 'Other')),
    Height FLOAT,
    Weight FLOAT,
    JoinDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    confirmation_token VARCHAR(255),
    profilepicture VARCHAR(255),
    confirmation_token_fp VARCHAR(255)
);

-- User Stats Table
CREATE TABLE UserStats (
    UserID INT PRIMARY KEY,
    DailyCaloriesIntake INT,
    TotalSteps INT,
    TotalDistance FLOAT,
    TotalWorkouts INT,
    LastActiveDate TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE WorkoutHistory (
    WorkoutID SERIAL PRIMARY KEY,
    UserID INT,
    ExerciseName VARCHAR(255),  -- From the API: Name of the exercise
    BodyPart VARCHAR(50),       -- From the API: Targeted body part, corresponds to "bodyPart"
    Equipment VARCHAR(100),     -- From the API: Equipment used
    TargetMuscle VARCHAR(100),  -- From the API: Main muscle group targeted
    Duration INT,
    CaloriesBurned FLOAT,
    StartDateTime TIME,
    EndDateTime TIME,
    ExerciseGIF VARCHAR(255),   -- URL to a GIF from the API demonstrating the exercise
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);


-- MacroTracker Table
CREATE TYPE meal_type AS ENUM ('Breakfast', 'Lunch', 'Dinner', 'Snack');

CREATE TABLE MacroTracker (
    TrackerID SERIAL PRIMARY KEY,
    UserID INT,
    LogTime TIME,
    name VARCHAR(100),
    CaloriesConsumed INT,
    ProteinConsumed FLOAT,
    CarbsConsumed FLOAT,
    FatsConsumed FLOAT,
    Meal_Type meal_type,
    Target_caloriesconsumed FLOAT,
    Target_proteinconsumed FLOAT,
    Target_carbsconsumed FLOAT,
    Target_fatconsumed FLOAT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);