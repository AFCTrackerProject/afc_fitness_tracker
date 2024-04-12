CREATE TABLE UserTable (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Height FLOAT,
    Weight FLOAT,
    JoinDate TIMESTAMP
);

-- User Stats Table
CREATE TABLE UserStats (
    UserID INT PRIMARY KEY,
    DailyCaloriesIntake INT,
    TotalSteps INT,
    TotalDistance FLOAT,
    TotalWorkouts INT,
    LastActiveDate TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

-- Workout History Table
CREATE TABLE WorkoutHistory (
    WorkoutID INT PRIMARY KEY,
    UserID INT,
    WorkoutType VARCHAR(50),
    Duration INT,
    CaloriesBurned FLOAT,
    StartDateTime TIMESTAMP,
    EndDateTime TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

-- Nutrition Log Table
CREATE TABLE NutritionLog (
    LogID INT PRIMARY KEY,
    UserID INT,
    FoodItem VARCHAR(100),
    Quantity FLOAT,
    CaloriesConsumed INT,
    LogDate DATE,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

-- Friends Table
CREATE TABLE Friends (
    FriendshipID INT PRIMARY KEY,
    UserID1 INT,
    UserID2 INT,
    FOREIGN KEY (UserID1) REFERENCES UserTable(UserID),
    FOREIGN KEY (UserID2) REFERENCES UserTable(UserID)
);

-- Messages Table
CREATE TABLE Messages (
    MessageID INT PRIMARY KEY,
    SenderUserID INT,
    ReceiverUserID INT,
    MessageContent TEXT,
    Timestamp TIMESTAMP,
    FOREIGN KEY (SenderUserID) REFERENCES UserTable(UserID),
    FOREIGN KEY (ReceiverUserID) REFERENCES UserTable(UserID)
);

-- Achievements Table
CREATE TABLE Achievements (
    AchievementID INT PRIMARY KEY,
    UserID INT,
    AchievementName VARCHAR(100),
    AchievementDescription TEXT,
    AchievementDate DATE,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);