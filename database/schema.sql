-- User Table
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    Height FLOAT,
    Weight FLOAT,
    JoinDate DATETIME
);

-- User Stats Table
CREATE TABLE UserStats (
    UserID INT PRIMARY KEY,
    DailyCaloriesIntake INT,
    TotalSteps INT,
    TotalDistance FLOAT,
    TotalWorkouts INT,
    LastActiveDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Workout History Table
CREATE TABLE WorkoutHistory (
    WorkoutID INT PRIMARY KEY,
    UserID INT,
    WorkoutType VARCHAR(50),
    Duration INT,
    CaloriesBurned FLOAT,
    StartDateTime DATETIME,
    EndDateTime DATETIME,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Nutrition Log Table
CREATE TABLE NutritionLog (
    LogID INT PRIMARY KEY,
    UserID INT,
    FoodItem VARCHAR(100),
    Quantity FLOAT,
    CaloriesConsumed INT,
    LogDate DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Friends Table
CREATE TABLE Friends (
    FriendshipID INT PRIMARY KEY,
    UserID1 INT,
    UserID2 INT,
    FOREIGN KEY (UserID1) REFERENCES User(UserID),
    FOREIGN KEY (UserID2) REFERENCES User(UserID)
);

-- Messages Table
CREATE TABLE Messages (
    MessageID INT PRIMARY KEY,
    SenderUserID INT,
    ReceiverUserID INT,
    MessageContent TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (SenderUserID) REFERENCES User(UserID),
    FOREIGN KEY (ReceiverUserID) REFERENCES User(UserID)
);

-- Achievements Table
CREATE TABLE Achievements (
    AchievementID INT PRIMARY KEY,
    UserID INT,
    AchievementName VARCHAR(100),
    AchievementDescription TEXT,
    AchievementDate DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE UserLevel (
    UserID INT PRIMARY KEY,
    CurrentLevel INT,
    ExperiencePoints INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);