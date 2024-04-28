import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash, get_flashed_messages, jsonify, session
from dotenv import load_dotenv
from database import fitness_repo
from flask_bcrypt import Bcrypt
import googlemaps
import openai
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename
import boto3
import requests 
from macrotracker import get_macros_by_meal_type, get_all_macros, create_macros, save_target


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')
api_key = os.getenv('GMAPS_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')
#openai.api_key = 'sk-proj-cnWNuIs8QKyamOPfaS6ST3BlbkFJJlzrYZgmbd1y3VtwXPi0'

s3_access_key = os.getenv('S3_ACCESS_KEY')
s3_secret_key = os.getenv('S3_SECRET_KEY')
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

s3 = boto3.client('s3',
                  aws_access_key_id=s3_access_key,
                  aws_secret_access_key=s3_secret_key)


gmaps = googlemaps.Client(key=api_key)

# gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))


bcrypt = Bcrypt(app)


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workouts')
def workouts():
    return render_template('workouts.html')

@app.get('/secret')
def secret():
    if 'userid' not in session:
        return redirect('/login')
    userid = session.get('userid')
    user = fitness_repo.get_user_by_id(userid)
    return render_template('secret.html', user=user)

@app.route('/macrotracker', methods=['GET', 'POST'])
def macrotracker():
    if 'userid' not in session:
        flash('You need to log in to use the macrotracker.', 'error')
        return redirect('/login')

    userid = session['userid']
    targets = session.get(f'targets_{userid}', None)

    """
    target_caloriesconsumed = session.get('target_caloriesconsumed', None)
    target_proteinconsumed = session.get('target_proteinconsumed', None)
    target_carbsconsumed = session.get('target_carbsconsumed', None)
    target_fatsconsumed = session.get('target_fatsconsumed', None)
    """
    

    if request.method == 'POST':
        # Retrieve form data
        meal_type = request.form.get('meal_type') 
        name = request.form.get(f'name_{meal_type.lower()}')
        caloriesconsumed = request.form.get(f'calories_{meal_type.lower()}')
        proteinconsumed = request.form.get(f'protein_{meal_type.lower()}')
        carbsconsumed = request.form.get(f'carbs_{meal_type.lower()}')
        fatsconsumed = request.form.get(f'fat_{meal_type.lower()}')
        quantity = request.form.get(f'quantity_{meal_type.lower()}')

        # Convert quantities to floats for multiplication
        caloriesconsumed = float(caloriesconsumed) * float(quantity)
        proteinconsumed = float(proteinconsumed) * float(quantity)
        carbsconsumed = float(carbsconsumed) * float(quantity)
        fatsconsumed = float(fatsconsumed) * float(quantity)

        # Call create_macros function to add a new entry
        if create_macros(userid, name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type):
            print("Insertion successful") # PROVES MACRO CREATION IS SUCCESSFUL
        else:
            print("Insertion failed")
            

    # Fetch all macros for display based on meal type
    all_breakfast_macros = get_macros_by_meal_type('Breakfast')
    all_lunch_macros = get_macros_by_meal_type('Lunch')
    all_dinner_macros = get_macros_by_meal_type('Dinner')
    all_snack_macros = get_macros_by_meal_type('Snack')

    

    # Calculate totals for each meal type
    total_breakfast_calories = sum([macro['caloriesconsumed'] for macro in all_breakfast_macros])
    total_breakfast_protein = sum([macro['proteinconsumed'] for macro in all_breakfast_macros])
    total_breakfast_carbs = sum([macro['carbsconsumed'] for macro in all_breakfast_macros])
    total_breakfast_fats = sum([macro['fatsconsumed'] for macro in all_breakfast_macros])

    total_lunch_calories = sum([macro['caloriesconsumed'] for macro in all_lunch_macros])
    total_lunch_protein = sum([macro['proteinconsumed'] for macro in all_lunch_macros])
    total_lunch_carbs = sum([macro['carbsconsumed'] for macro in all_lunch_macros])
    total_lunch_fats = sum([macro['fatsconsumed'] for macro in all_lunch_macros])

    total_dinner_calories = sum([macro['caloriesconsumed'] for macro in all_dinner_macros])
    total_dinner_protein = sum([macro['proteinconsumed'] for macro in all_dinner_macros])
    total_dinner_carbs = sum([macro['carbsconsumed'] for macro in all_dinner_macros])
    total_dinner_fats = sum([macro['fatsconsumed'] for macro in all_dinner_macros])

    total_snack_calories = sum([macro['caloriesconsumed'] for macro in all_snack_macros])
    total_snack_protein = sum([macro['proteinconsumed'] for macro in all_snack_macros])
    total_snack_carbs = sum([macro['carbsconsumed'] for macro in all_snack_macros])
    total_snack_fats = sum([macro['fatsconsumed'] for macro in all_snack_macros])

    # Collect totals for the day
    total_calories = (total_breakfast_calories + total_lunch_calories +
                          total_dinner_calories + total_snack_calories)
    total_protein = (total_breakfast_protein + total_lunch_protein +
                         total_dinner_protein + total_snack_protein)
    total_carbs = (total_breakfast_carbs + total_lunch_carbs +
                       total_dinner_carbs + total_snack_carbs)
    total_fats = (total_breakfast_fats + total_lunch_fats +
                      total_dinner_fats + total_snack_fats)
      
    return render_template('macrotracker.html',
                       all_breakfast_macros=all_breakfast_macros,
                       all_lunch_macros=all_lunch_macros,
                       all_dinner_macros=all_dinner_macros,
                           all_snack_macros=all_snack_macros,total_breakfast_calories=total_breakfast_calories,
                           total_breakfast_protein=total_breakfast_protein,
                           total_breakfast_carbs=total_breakfast_carbs,
                           total_breakfast_fats=total_breakfast_fats,
                           total_lunch_calories=total_lunch_calories,
                           total_lunch_protein=total_lunch_protein,
                           total_lunch_carbs=total_lunch_carbs,
                           total_lunch_fats=total_lunch_fats,
                           total_dinner_calories=total_dinner_calories,
                           total_dinner_protein=total_dinner_protein,
                           total_dinner_carbs=total_dinner_carbs,
                           total_dinner_fats=total_dinner_fats,
                           total_snack_calories=total_snack_calories,
                           total_snack_protein=total_snack_protein,
                           total_snack_carbs=total_snack_carbs,
                           total_snack_fats=total_snack_fats,
                           total_calories=total_calories,total_protein=total_protein,total_fats=total_fats,total_carbs=total_carbs, targets=targets)

# Define the route for the Targets page
@app.route('/targets', methods=['GET', 'POST'])
def save_targets():
    if 'userid' not in session:
        flash('You need to log in to set a target.', 'error')
        return redirect('/login')
    
    userid = session['userid']

    if request.method == 'POST':
        # Retrieve form data
        target_caloriesconsumed = request.form.get('target_caloriesconsumed')
        target_proteinconsumed = request.form.get('target_proteinconsumed')
        target_carbsconsumed = request.form.get('target_carbsconsumed')
        target_fatsconsumed = request.form.get('target_fatsconsumed')

        session[f'targets_{userid}'] = {
            'calories': target_caloriesconsumed,
            'protein': target_proteinconsumed,
            'carbs': target_carbsconsumed,
            'fats': target_fatsconsumed
        }

        # Call save_target function with userid as the first argument
        save_target(userid, target_caloriesconsumed, target_proteinconsumed, target_carbsconsumed, target_fatsconsumed)
        return redirect(url_for('macrotracker'))    

    return render_template('targets.html')

    

@app.get('/forum')
def forum():
    if 'userid' not in session:
        flash('You need to log in to use the forum feature.','error')
        return redirect('/login')
    return render_template('forum.html')

@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        # Retrieve form data from what the user just submitted
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        # Check that username and password are not empty
        if not username or not password:
            flash('Username/password cannot be empty', 'error')
            return render_template('signup.html', show_popup=True)
        
        # Check that the passwords on the form match
        if password != confirmpassword:
            flash('Passwords do not match', 'error')
            return render_template('signup.html', show_popup=True)

        # Encrypts password and stores it as a hashed password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Executes the SQL code and flashes a message to indicate it was successful
        if fitness_repo.create_user(firstname, lastname, email, username, hashed_password):
            flash('User account successfully created!', 'info')
            return render_template('signup.html', show_popup=True)

    # Render the signup form template for GET requests
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Retrieve form data from what the user just submitted
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate username and password
        if not username or not password:
            abort(400, 'Both username and password are required!')
        
        # Retrieve user from repository/database
        user = fitness_repo.get_user_by_username(username)
        
        # Check if user exists
        if user is None:
            flash('Username does not exist! Create an account!', 'error')
            return render_template('login.html', show_popup=True)
    
        # Verify password
        if not bcrypt.check_password_hash(user['password'], password):
            flash('Username and password do not match!', 'error')
            return render_template('login.html', show_popup=True)
        
        # Set userid and username in session
        session['userid'] = user['userid']
        session['username'] = user['username']
        
        # Flash login successful message
        flash('Login successful!', 'success')
        
        # Check if user is logging in for the first time
        if 'first_login' not in session:
            # Store the first login flag in the session
            session['first_login'] = True
            return redirect(url_for('secret'))  # Redirect to secret page for first-time login
        else:
            # Redirect to profile page for subsequent logins
            return redirect(url_for('profile'))
    
    # If GET request (i.e., accessing the login page)
    return render_template('login.html')


@app.post('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')
    flash('You have been logged out.','info')

@app.get('/profile')
def profile():
    if 'userid' not in session:
        flash('You need to log in to see your profile.','error')
        return redirect('/login')
    userid = session.get('userid')
    user = fitness_repo.get_user_by_id(userid)
    print(user.get('weight'))
    print(user.get('profilepicture'))
    return render_template('profile.html', user=user)

@app.route('/finder.html')
def finder():
    if 'userid' not in session:
        flash('You need to log in to use the Finder feature.','error')
        return redirect('/login')
    return render_template('finder.html')

@app.route('/find_places', methods=['POST'])
def find_places():
    try:
        # Get ZIP code and place type from form data
        zip_code = request.form['zip_code']
        place_type = request.form['category']

        # Log the received form data for debugging
        print("Received form data - ZIP code:", zip_code)
        print("Received form data - Place type:", place_type)

        # Use Google Maps Geocoding API to convert ZIP code to coordinates
        geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={api_key}"
        geocoding_response = requests.get(geocoding_api_url)
        geocoding_data = geocoding_response.json()

        # Log the geocoding response for debugging
        print("Geocoding response:", geocoding_data)

        # Extract latitude and longitude from the geocoding response
        if geocoding_data['status'] == 'OK':
            location = geocoding_data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']

            # Log the extracted coordinates for debugging
            print("Extracted latitude:", latitude)
            print("Extracted longitude:", longitude)

            # Define the request body with the extracted coordinates
            request_body = {
                "includedTypes": [place_type],
                "maxResultCount": 10,
                "locationRestriction": {
                    "circle": {
                        "center": {
                            "latitude": latitude,
                            "longitude": longitude
                        },
                        "radius": 5000.0
                    }
                }
            }

            # Define headers
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": "AIzaSyAKDHnR80au2cURkbiCZyKg061A1cZt3MY",
                "X-Goog-FieldMask": "places.displayName,places.location"  # Specify the fields you want in the response
            }

            # Make POST request to Google Places API
            response = requests.post("https://places.googleapis.com/v1/places:searchNearby", json=request_body, headers=headers)
            response_data = response.json()

            # Log the response from Google Places API for debugging
            print("Google Places API response:", response_data)

            # Extract places from the response
            places = response_data.get('places', [])

            # Return places as JSON response
            return jsonify(places)
        else:
            return jsonify({'error': 'Failed to geocode ZIP code'}), 500

    except Exception as e:
        # Handle API error
        return jsonify({'error': str(e)}), 500
    
@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')

# Route to handle user input and get bot response
@app.route('/chatbot', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data['message']

    # Call OpenAI API to get bot response
    response = get_bot_response(message)
    print(response)

    return jsonify({'response': response})

# Function to get bot response using OpenAI API
def get_bot_response(message):
    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=message,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

@app.route('/submit_question', methods=['POST'])
def handle_question_submission():
    # Check if userid and username are stored in the session
    if 'userid' not in session or 'username' not in session:
        return redirect('/')  # Redirect to home page or login page if user is not logged in

    # Retrieve userid and username from session
    userid = session['userid']
    username = session['username']

    # Retrieve form data (weight, height, gender)
    weight = request.form.get('weight')
    height = request.form.get('height')
    gender = request.form.get('gender')
    dateofbirth = request.form.get('dateofbirth')

    # Validate and convert weight to float
    try:
        weight_float = float(weight)
    except ValueError:
        flash('Invalid weight value. Please enter a valid number.', 'error')
        return redirect(url_for('secret'))

    # Validate and convert height to float
    try:
        height_float = float(height)
    except ValueError:
        flash('Invalid height value. Please enter a valid number.', 'error')
        return redirect(url_for('secret'))

    # Call the fitness_repo function to update the user's weight, height, and gender
    success = fitness_repo.submit_question(username, weight_float, height_float, gender, dateofbirth)

    if success:
        flash('Welcome to your new profile! Click the icon at the top right at any time while logged in to view it! You can always update your profile at the bottom. ', 'success')
    else:
        flash('Failed to update one of the following: weight, height, gender, DOB. Please try again.', 'error')

    return redirect(url_for('profile'))

@app.route('/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    if 'userid' not in session:
        flash('You need to log in to update your profile.', 'error')
        return redirect('/login')
    
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        dateofbirth = request.form.get('dateofbirth')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        profile_picture = request.files['profilepicture']

        # Validate profile picture
        if profile_picture:
            # Secure filename to prevent directory traversal
            filename = secure_filename(profile_picture.filename)
            try:
                # Upload profile picture to S3 bucket
                s3.upload_fileobj(profile_picture, s3_bucket_name, filename)
                # Get S3 URL for uploaded profile picture
                profile_picture_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{filename}"
                
                # Update user profile in the database with the S3 URL
                success = fitness_repo.update_user_profile(
                    userid=session['userid'],
                    email=email,
                    dateofbirth=dateofbirth,
                    gender=gender,
                    height=height,
                    weight=weight,
                    profilepicture=profile_picture_url  # Pass S3 URL to function
                )

                if success:
                    flash('Profile updated successfully!', 'success')
                else:
                    flash('Failed to update profile. Please try again.', 'error')

            except NoCredentialsError:
                flash('AWS credentials not available. Profile picture upload failed.', 'error')

    # Fetch user data for rendering the profile page
    user = fitness_repo.get_user_by_id(session['userid'])
    #print(user.profilepicture)
    return render_template('updateprofile.html', user=user)


@app.context_processor
def inject_logged_in():
    # Check if user is logged in
    logged_in = 'userid' in session
    return dict(logged_in=logged_in)

# Exercises API
def get_exercises_by_muscle(muscle):
    url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/" + muscle

    querystring = {"limit":"200"} # High number to get the max amount out of the API

    headers = {
        'x-rapidapi-host': "exercisedb.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('EXERCISE_DB_API_KEY')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def search_youtube(query):
    url = "https://youtube-search-and-download.p.rapidapi.com/search"
    querystring = {"query": query}
    headers = {
        'x-rapidapi-host': "youtube-search-and-download.p.rapidapi.com",
        'x-rapidapi-key': os.getenv('YOUTUBE_API_KEY')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


@app.route('/exercises/<muscle>')
def exercises(muscle):
#    print(f"Fetching exercises for muscle: {muscle}")  # Console log
    try:
        exercises = get_exercises_by_muscle(muscle)
        videos = search_youtube(muscle + ' exercises')
        return jsonify({'exercises': exercises, 'videos': videos})
    except Exception as e:
#        print(f"Error: {e}")  # Console log for the error
        return jsonify({'error': str(e)}), 500



# End Exercises API


if __name__ == "__main__":
    app.run(debug=True) 