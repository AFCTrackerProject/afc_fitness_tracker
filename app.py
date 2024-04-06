from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Add other fields as needed

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workouts')
def workouts():
    return render_template('workouts.html')

@app.get('/macrotracker')
def macrotracker():
    return render_template('macrotracker.html')

@app.get('/forum')
def forum():
    return render_template('forum.html')

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/about')
def about():
    return render_template('about.html')

@app.get('/user-registration')
def userregistration():
    return render_template('user-registration.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

'''
   
def add_exercise(self, exercise_name, duration, calories_burned):
    """
    Add a new exercise entry to the tracking system.

    :param exercise_name: Name of the exercise.
    :type exercise_name: str
    :param duration: Duration of the exercise in minutes.
    :type duration: int
    :param calories_burned: Calories burned during the exercise.
    :type calories_burned: float
    """
    pass
   
def remove_exercise(self, exercise_name):
    """
    Remove an exercise entry from the tracking system.

    :param exercise_name: Name of the exercise to be removed.
    :type exercise_name: str
    """
    pass
   
def view_exercises(self):
    """
    View all recorded exercises.
    """
    pass
   
def calculate_total_calories(self):
    """
    Calculate the total calories burned from all recorded exercises.

    :return: Total calories burned.
    :rtype: float
    """
    pass
   
def suggest_exercise(self):
    """
    Suggest an exercise based on user preferences or goals.
    """
    pass

'''


if __name__ == "__main__":
    app.run(debug=True)