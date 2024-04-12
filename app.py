from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workouts')
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

@app.get('/forum')
def forum():
    return render_template('forum.html')

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/about')
def about():
    return render_template('about.html')

@app.post('/user-registration')
def userregistration():
    
    return render_template('user-registration.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        # Validate form data
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #Check if email is valid

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return 'Invalid email address'
       
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Email already exists'
       
        # Create new user
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
       
        # Store user's id in session
        if new_user.id:
            session['user_id'] = new_user.id
            return 'User registered successfully'
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
       
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
          # Store user's id in session
            session['user_id'] = user.id
            return 'Logged in successfully'

    return render_template('login.html')

@app.route('/chest')
def chest():
    return redirect('https://www.muscleandstrength.com/workouts/chest')

@app.route('/back')
def back():
    return redirect('https://www.muscleandstrength.com/workouts/back')

@app.route('/bicep')
def bicep():
    return redirect('https://www.muscleandstrength.com/workouts/biceps')

@app.route('/legs')
def legs():
    return redirect('https://www.muscleandstrength.com/workouts/legs')

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