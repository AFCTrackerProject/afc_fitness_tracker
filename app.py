from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workouts')
def workouts():
    return render_template('workouts.html')

@app.route('/macrotracker')
def macrotracker():
    return render_template('macrotracker.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user-registration')
def userregistration():
    return render_template('user-registration.html')

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