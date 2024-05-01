# AFC Fitness Tracker

Welcome to the AFC Fitness Tracker project, a comprehensive solution developed for the ITSC-3155 Software Engineering course at the University of North Carolina at Charlotte. This application assists users in effectively monitoring and managing their fitness routines, with features like workout tracking, nutritional monitoring, and a community-driven fitness forum.

## Course

- **Course**: ITSC - 3155 Software Engineering
- **Instructor**: Prof. Jacob Krevat
- **Semester**: Spring 2024
- **Institution:** UNC Charlotte


## Team Members

- **Shubi Gaur** - Team Lead & Database/Backend Developer
- **Cameron Copenhaver** - Back-end Developer & API Specialist
- **Tommy-Nam Nguyen** -  Front-end Developer & API Specialist
- **Andrew Schmal** - Front-end Developer & DevOps for Docker Deployment

Each member contributed to specific project components, collaborating to ensure good version control and effective team development.


## Features

- **Workout Tracking**: Log workouts, track calories burned, and progress over time.
- **Macro Tracker**: Monitor daily protein, carb, and fat intake for dietary balance.
- **Fitness Forum**: Exchange tips, seek advice, and engage with the fitness community.
- **Personal Profile**: Set and track fitness goals within a personalized user profile.
- **Fitness Finder**: Find nearby fitness centers and parks via Google Maps integration.
- **Workouts Page**: Access over 1300 exercises with data and demonstrations through ExerciseDB.
- **Fitness Chat Bot**: Get fitness advice from an AI chatbot powered by OpenAI API.


## Getting Started

Follow these instructions to set up the project locally for development and testing:

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Flask
- An active internet connection for accessing third-party APIs (Google Maps)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TommyNam/afc_fitness_tracker

2. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
```

3. **Setup your PostgreSQL database:**
Follow the steps outlined in 'schema.sql' to configure and create the database.

4. **Environment setup:**
Duplicate '.env.sample' to '.env' and update it with the appropriate credentials and API keys.
```bash
cp .env.sample .env
```

5. **Run the application:**
```bash
flask run
```


## Contributions

This project is an academic exercise and is closed for external contributions. It serves as a learning tool and should not replace professional fitness advice. Feedback and suggestions from instructors and peer reviews are welcomed.

## License
This project is licensed under the University of North Carolina at Charlotte’s academic policies. All codebase is for educational purposes and may not be used for commercial intent without proper permissions.


## Docker
docker build -t rob-server:latest 
docker run -p 5001:8000 rob-server:latest