import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash, jsonify, session
from dotenv import load_dotenv
from database import fitness_repo
from flask_bcrypt import Bcrypt
import googlemaps
import requests 


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

api_key = 'AIzaSyAKDHnR80au2cURkbiCZyKg061A1cZt3MY'
gmaps = googlemaps.Client(key='AIzaSyAKDHnR80au2cURkbiCZyKg061A1cZt3MY')

bcrypt = Bcrypt(app)

user_macros = {
    'targets': {
        'protein': 0,
        'carbs': 0,
        'fats': 0
    },
    'daily_intake': {
        'protein': 0,
        'carbs': 0,
        'fats': 0
    }
}

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workouts')
def workouts():
    if 'userid' not in session:
        return redirect('/')
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
        # Retrieve form data from request
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are not empty
        if not username or not password:
            return 'Username or password cannot be empty'

        # Further processing (e.g., validate inputs, create user)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Create user in the database or perform other actions
        # Example:
        fitness_repo.create_user(firstname, lastname, email, username, hashed_password)

        return 'User created successfully'
    

    # Render the signup form template for GET requests
    return render_template('signup.html')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:    
            abort(400, 'Both username and password are required!')
        
        user = fitness_repo.get_user_by_username(username)
        print(user)
        if not user:
             abort(401, 'Invalid username or password.')        

        validated_password = bcrypt.check_password_hash(user["password"],password)
        
        if not validated_password:
            flash('Username and password do not match!', 'error')
            return render_template('login.html', show_popup=True)
        
        flash('Login successful!', 'success')
        session['userid'] = user['userid']
        return redirect(url_for('workouts'))


    return render_template('login.html')

@app.post('/logout')
def logout():
    session.pop('userid', None)
    print('userid' in session)
    return redirect('/')

@app.get('/profile')
def profile():
    # Simply render the profile.html template
    return render_template('profile.html')

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

@app.route('/finder.html')
def finder():
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
        geocoding_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key=AIzaSyAKDHnR80au2cURkbiCZyKg061A1cZt3MY"
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



if __name__ == "__main__":
    app.run(debug=True) 
