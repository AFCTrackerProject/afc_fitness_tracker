from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Placeholder for storing macro targets and daily intake
user_macros = {
    'targets': {'protein': 0, 'carbs': 0, 'fats': 0},
    'daily_intake': {'protein': 0, 'carbs': 0, 'fats': 0}
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workouts')
def workouts():
    return render_template('workouts.html')

@app.route('/macrotracker', methods=['GET', 'POST'])
def macrotracker():
    if request.method == 'POST':
        if 'set_targets' in request.form:
            # Logic for setting targets remains the same
            user_macros['targets'] = {
                'protein': int(request.form.get('target_protein', 0)),
                'carbs': int(request.form.get('target_carbs', 0)),
                'fats': int(request.form.get('target_fats', 0))
            }
        elif 'log_intake' in request.form:
            # Adjusted logic for accumulating daily intake
            user_macros['daily_intake']['protein'] += int(request.form.get('daily_protein', 0))
            user_macros['daily_intake']['carbs'] += int(request.form.get('daily_carbs', 0))
            user_macros['daily_intake']['fats'] += int(request.form.get('daily_fats', 0))
        return redirect(url_for('macrotracker'))
    
    return render_template('macrotracker.html', user_macros=user_macros)


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