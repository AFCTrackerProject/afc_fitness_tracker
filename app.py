import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash, get_flashed_messages, jsonify, session
from dotenv import load_dotenv
from database import fitness_repo
from database.fitness_repo import get_confirmation_token, verify_confirmation_token, get_user_by_id, generate_confirmation_token
from flask_bcrypt import Bcrypt
import googlemaps
import openai
from botocore.exceptions import NoCredentialsError
from flask_mail import Mail, Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from werkzeug.utils import secure_filename
import boto3
import requests 
import secrets
from macrotracker import get_macros_by_meal_type, get_all_macros, create_macros, save_target, clear_logs
from database.workouttracker import insert_workout_log, get_workout_logs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize SQLAlchemy with your Flask app
load_dotenv()

# Define your models after initializing `db`
class Topic(db.Model):
    __tablename__ = 'topics'  # Good practice to explicitly name your tables
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(1024))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    topic = db.relationship('Topic', backref=db.backref('comments', lazy='dynamic'))

mail = Mail(app)
sg = SendGridAPIClient(os.getenv('SENDGRIDKEY'))



#client = Client("str", "str")


# Amazon SES SMTP configuration
'''
app.config['MAIL_SERVER'] = 'email-smtp.us-east-1.amazonaws.com'  # Replace <region> with your AWS region, e.g., 'us-west-2'
app.config['MAIL_PORT'] = 465  # Use 465 for SSL/TLS or 587 for STARTTLS
app.config['MAIL_USE_SSL'] = True  # Set to True if using SSL/TLS
app.config['MAIL_USE_TLS'] = False  # Set to False if using SSL/TLS
app.config['MAIL_USERNAME'] = 'AKIAYS2NRIK4A6SRWMHW'  # SMTP username generated in the previous step
app.config['MAIL_PASSWORD'] = 'BDaeEdgCboEir98hOfE5wsNiQlqShsuvs9FD1d7tty1Z'  # SMTP password generated in the previous step
app.config['MAIL_DEFAULT_SENDER'] = 'camcope247@gmail.com'  # Replace with your verified email address
'''

app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'  # SMTP server for SendGrid
app.config['MAIL_PORT'] = 587  # Port for TLS connections
app.config['MAIL_USE_TLS'] = True  # Enable TLS encryption
app.config['MAIL_USERNAME'] = 'apikey'  # SendGrid username
app.config['MAIL_PASSWORD'] = os.getenv('SENDGRIDKEY')  # SendGrid API key as password
app.config['MAIL_DEFAULT_SENDER'] = 'camcope247@gmail.com'  # Your verified sender email address

# Initialize Flask-Mail
mail = Mail(app)
ses_client = boto3.client('ses', region_name='us-east-1')

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

# memes
# Forum homepage
@app.route("/forum", methods=["GET", "POST"])
def forum_home():
    if request.method == "POST":
        # Add a new topic
        title = request.form.get("title")
        description = request.form.get("description")
        if title and description:  # Ensure non-empty submissions
            topic = Topic(title=title, description=description)
            db.session.add(topic)
            db.session.commit()
            flash("Topic added successfully!", "success")
        else:
            flash("Both title and description must be provided.", "error")

    topics = Topic.query.all()  # Fetch all topics
    return render_template("forumhome.html", topics=topics)

# Specific topic and comments page
@app.route("/forum/topic/<int:id>", methods=["GET", "POST"])
def forum_topic(id):
    topic = Topic.query.get_or_404(id)
    if request.method == "POST":
        # Add a new comment to the topic
        comment_text = request.form.get("comment")
        if comment_text:  # Ensure non-empty comment
            comment = Comment(text=comment_text, topicId=id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added successfully!", "success")
        else:
            flash("Comment cannot be empty.", "error")

    comments = Comment.query.filter_by(topicId=id).all()
    return render_template("forumpost.html", topic=topic, comments=comments)

def calculate_progress(total, target):
    # Ensure target is a float
    if isinstance(target, str):
        target = float(target)
    
    # Calculate progress
    if target == 0:
        return 0
    progress = min(total / target * 100, 100)
    
    # Round the progress to the nearest integer
    progress = round(progress)
    
    return progress



@app.route('/macrotracker', methods=['GET', 'POST'])
def macrotracker():
    if 'userid' not in session:
        flash('You need to log in to use the macrotracker.', 'error')
        return redirect('/login')

    userid = session['userid']
    targets = session.get(f'targets_{userid}', None)    

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
    
    
    progress_calories = None
    progress_protein = None
    progress_carbs = None
    progress_fats = None

    if targets:
        progress_calories = calculate_progress(total_calories, targets['calories'])
        progress_protein = calculate_progress(total_protein, targets['protein'])
        progress_carbs = calculate_progress(total_carbs, targets['carbs'])
        progress_fats = calculate_progress(total_fats, targets['fats'])
    
    # Check if targets are set and if each macro's total is greater than or equal to its target
    if targets:
        if total_calories >= float(targets['calories']):
            flash('Congrats! You hit your calorie goal for today', 'success')

        if total_protein >= float(targets['protein']):
            flash('Congrats! You hit your protein goal for today', 'success')

        if total_carbs >= float(targets['carbs']):
            flash('Congrats! You hit your carbs goal for today', 'success')

        if total_fats >= float(targets['fats']):
            flash('Congrats! You hit your fats goal for today', 'success')
                
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
                           total_calories=total_calories,total_protein=total_protein,total_fats=total_fats,total_carbs=total_carbs, targets=targets,
                           progress_calories=progress_calories, progress_protein=progress_protein, progress_carbs=progress_carbs, progress_fats=progress_fats)

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

@app.route('/clear_breakfast_logs', methods=['POST'])
def clear_breakfast_logs_route():
    if clear_logs("Breakfast"):
        flash('Breakfast logs cleared successfully', 'info')
    else:
        flash('Failed to clear breakfast logs', 'error')
    return redirect(url_for('macrotracker'))

@app.route('/clear_lunch_logs', methods=['POST'])
def clear_lunch_logs_route():
    if clear_logs("Lunch"):
        flash('Lunch logs cleared successfully', 'info')
    else:
        flash('Failed to clear lunch logs', 'error')
    return redirect(url_for('macrotracker'))

@app.route('/clear_dinner_logs', methods=['POST'])
def clear_dinner_logs_route():
    if clear_logs("Dinner"):
        flash('Dinner logs cleared successfully', 'info')
    else:
        flash('Failed to clear dinner logs', 'error')
    return redirect(url_for('macrotracker'))

@app.route('/clear_snack_logs', methods=['POST'])
def clear_snack_logs_route():
    if clear_logs("Snack"):
        flash('Snack logs cleared successfully', 'info')
    else:
        flash('Failed to clear snack logs', 'error')
    return redirect(url_for('macrotracker'))

@app.route('/workouttracker', methods=['GET'])
def workouttracker():
    if 'userid' not in session:
            flash('You need to log in to use the workout tracker.', 'error')
            return redirect('/login')  
    return render_template('workouttracker.html')



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
        confirmation_token = get_confirmation_token(email)  # Pass email to get_confirmation_token
        
        # Check that username and password are not empty
        if not username or not password:
            flash('Username/password cannot be empty', 'error')
            return render_template('signup.html', show_popup=True)
        
        # Check that the passwords on the form match
        if password != confirmpassword:
            flash('Passwords do not match', 'error')
            return render_template('signup.html', show_popup=True)

        # Check if the provided username and email already exist in the database
        if not fitness_repo.is_username_available(username):
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('signup.html', show_popup=True)

        if not fitness_repo.is_email_available(email):
            flash('Email address already exists. Please choose a different email.', 'error')
            return render_template('signup.html', show_popup=True)

        # Encrypts password and stores it as a hashed password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Executes the SQL code and flashes a message to indicate it was successful
        if fitness_repo.create_user(firstname, lastname, email, username, hashed_password, confirmation_token):
            flash('User account successfully created!', 'info')
            
            # Retrieve the newly created user's details and set session user ID
            user = fitness_repo.get_user_by_username(username)
            session['userid'] = user['userid']

            # Send confirmation email to the user
            send_confirmation_email(email, firstname)

        # Render the verification page with user's email
        return render_template('verification.html', user_email=email)

    # Render the signup form template for GET requests
    return render_template('signup.html')





# Function to send confirmation email
def send_confirmation_email(email, firstname):
    confirmation_token = get_confirmation_token(email)

    message = Mail(
        from_email='camcope247@gmail.com',  
        to_emails=email,
        subject='Welcome to AFC Fitness!',
        html_content=f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .confirmation-code {{
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Dear {firstname},</h2>
                    <p>Thank you for signing up on our website!</p>
                </div>
                <div>
                    <p>Your confirmation code is: <span class="confirmation-code">{confirmation_token}</span></p>
                </div>
                <div class="footer">
                    <p>Best Regards,<br>The AFC Fitness Team</p>
                </div>
            </div>
        </body>
        </html>
        """
    )

    try:
        # Send the email using the SendGrid API
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

# Route to verify token
@app.route('/verify_token', methods=['POST'])
def verify_token():
    # Get user ID from session
    user_id = session.get('userid')
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login page if user ID not found in session
    
    # Fetch user from the database based on user ID
    user = fitness_repo.get_user_by_id(user_id)
    print(user.get('email'))
    print(user.get('email'))
    if not user:
        return "User not found"  # Handle case where user is not found in the database
    
    # Check if the request method is POST
    if request.method == 'POST':
        token_entered = request.form['token']
        if verify_confirmation_token(user['email'], token_entered):
            # If the token matches, render the profile page
            return render_template('profile.html', user=user)
        else:
            # If the token doesn't match, render an error message or redirect back to the form
            flash('Invalid token. Please try again', 'error')
            return render_template('verification.html')

    # Render the verification form template with the user object
    return render_template('verification.html', user=user)

# Route to display verification form
@app.route('/verification_form')
def verification_form():
    # Check if user ID is in session
    if 'userid' not in session:
        flash('You need to log in to see your profile.', 'error')
        return redirect('/login')
    
    # Get user ID from session
    userid = session.get('userid')
    
    # Fetch user from the database based on user ID
    user = fitness_repo.get_user_by_id(userid)
    
    # Check if user exists
    if not user:
        return "User not found"  # Handle case where user is not found in the database
    
    # Render the verification form template with the user object
    return render_template('verification.html', user=user)



@app.route('/send_reset_email', methods=['POST'])
def send_reset_email():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Generate a confirmation token for password reset
        confirmation_token_fp = generate_confirmation_token()
        fitness_repo.update_confirmation_token(email, confirmation_token_fp)
        print(email)
        print(confirmation_token_fp)
        
        # Update the user's confirmation token in the database
        if fitness_repo.update_confirmation_token(email, confirmation_token_fp):
            # Get user details from the database using email
            user = fitness_repo.get_user_by_email(email)
            
            # Check if user exists and retrieve firstname
            if user:
                firstname = user.get('firstname')
                username = user.get('username')
                userid = user.get('userid')
                
                message = Mail(
                    from_email='camcope247@gmail.com',  
                    to_emails=email,
                    subject='Password Reset',
                    html_content=f"""
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: 0 auto;
                                    padding: 20px;
                                    background-color: #f9f9f9;
                                    border-radius: 5px;
                                }}
                                .header {{
                                    text-align: center;
                                    margin-bottom: 20px;
                                }}
                                .confirmation-code {{
                                    font-weight: bold;
                                }}
                                .footer {{
                                    margin-top: 20px;
                                    text-align: center;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="header">
                                    <h2>Dear {firstname},</h2>
                                    <p>In case you forgot, your username is: {username}</p>
                                    <p>To reset your password, please use the code below!</p>
                                </div>
                                <div>
                                    <p>Your confirmation code is: <span class="confirmation-code">{confirmation_token_fp}</span></p>
                                    <p>Please be advised that this token is valid only once and must be entered</p>
                                    <p>correctly on your first attempt exactly as it appears above!</p>
                                </div>
                                <div class="footer">
                                    <p>Best Regards,<br>The AFC Fitness Team</p>
                                </div>
                            </div>
                        </body>
                        </html>
                    """
                )

                try:
                    # Send the email using the SendGrid API
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(str(e))
                    flash('Error sending email. Please try again.', 'error')
                    return render_template('forgotpassword.html')
                
                # Render a page similar to verification.html
                print(f"Passing ***{email}*** to verify_token_fp")
                return redirect(url_for('verify_token_fp', email=email))
        
        flash('User not found.', 'error')
        return redirect(url_for('login'))

        
@app.route('/verify_token_fp', methods=['GET', 'POST'])
def verify_token_fp():
    # Get user email from form data for POST requests
    #email = request.form.get('email')
    #confirmation_token_fp = request.form.get('token')
    #print("confirmation_token_fp: " ,confirmation_token_fp)
    #email = fitness_repo.get_useremail_by_tokenfp(confirmation_token_fp)
    email = request.args.get('email')
    print("Received email:", email)

    # Check if the request method is POST
    if request.method == 'POST':
        email = request.form.get('email')
        print("Received email:", email)
        token_entered = request.form['token']
        print("Token entered:", token_entered)
        print("Email:", email)
        if email is None:
            # Handle the case where email is not found in form data
            flash('Email parameter is missing', 'error')
            return redirect(url_for('login'))  # Redirect to login page or appropriate page
        if fitness_repo.verify_confirmation_token_fp(email, token_entered):
            # If the token matches, render the reset password page
            return redirect(url_for('reset_password', confirmation_token_fp=token_entered))
            #return render_template('reset.html', confirmation_token_fp=token_entered)
        else:
            # If the token doesn't match, render an error message or redirect back to the form
            flash('Invalid token. Please try again', 'error')
            return redirect(url_for('login'))

    # Render the verification form template with the user's email
    return render_template('verificationreset.html', user_email=email)





@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        # Retrieve the confirmation token from the query parameters
        confirmation_token_fp = request.args.get('confirmation_token_fp')
        print("confirmation_token_fp: ", confirmation_token_fp)

        # Store the confirmation token in the session
        session['confirmation_token_fp'] = confirmation_token_fp

        # Render the reset password form template
        return render_template('reset.html')

    elif request.method == 'POST':
        # Retrieve the confirmation token from the session
        confirmation_token_fp = session.get('confirmation_token_fp')
        print("confirmation_token_fp: ", confirmation_token_fp)

        # Retrieve email associated with the confirmation token
        email = fitness_repo.get_useremail_by_tokenfp(confirmation_token_fp)
        print('email is below')
        print(email)

        # Retrieve user ID associated with the email
        user_id = fitness_repo.get_userid_by_email(email)
        print('user_id: ', user_id)

        # Retrieve password and confirm password from the form
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset.html')

        # Hash the new password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Update the password in the database
        if fitness_repo.update_password(user_id, hashed_password):
            flash('Password successfully updated!', 'success')
        else:
            flash('Failed to update password', 'error')

        # Redirect to login page
        return redirect(url_for('login'))

    # Render the reset password form template for other HTTP methods
    return render_template('reset.html')



'''
@app.route('/verify_phone', methods=['GET', 'POST'])
def verify_phone():
    if request.method == 'POST':
        # Retrieve the phone number and verification code from the form
        #phone_number = request.form.get('phone_number')
        print(phone_number)
        verification_code = request.form.get('verification_code')
        
        # Verify the phone number and code (you should implement this logic using Twilio)
        if verify_phone_number(phone_number, verification_code):
            flash('Phone number verified successfully!', 'success')
            # Redirect to profile page upon successful verification
            return redirect(url_for('profile'))
        else:
            flash('Phone number verification failed. Please try again.', 'error')
            return render_template('verification.html')

    # Render the verification page for GET requests
    return render_template('verification.html')

def verify_phone_number(phone_number, verification_code):
    try:
        verification_check = client.verify.services('VA11676748fbdd2f113ed0bab0b96f1cc5') \
            .verification_checks \
            .create(to=phone_number, code=verification_code)

        # Check if the verification check was successful
        if verification_check.status == 'approved':
            return True
        else:
            return False
    except Exception as e:
        print(f"Error verifying phone number: {e}")
        return False
'''

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


@app.route('/forgotpassword')
def forgot_password():
    return render_template('forgotpassword.html')

@app.post('/logout')
def logout():
    session.pop('userid', None)
    flash('You have been logged out.','info')
    return redirect('/')
    

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
    if 'userid' not in session:
        flash('You need to log in to use the Finder feature.','error')
        return redirect('/login')
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
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        dateofbirth = request.form.get('dateofbirth')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        profile_picture = request.files['profilepicture']

        # Fetch user data
        user = fitness_repo.get_user_by_id(session['userid'])

        # Check if the provided username and email are different from the current ones
        if user['username'] != username and not fitness_repo.is_username_available(username):
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(request.url)
        
        if user['email'] != email and not fitness_repo.is_email_available(email):
            flash('Email address already exists. Please choose a different email.', 'error')
            return redirect(request.url)

        # Validate profile picture
        if profile_picture:
            # Secure filename to prevent directory traversal
            filename = secure_filename(profile_picture.filename)
            try:
                # Upload profile picture to S3 bucket
                s3.upload_fileobj(profile_picture, s3_bucket_name, filename)
                # Get S3 URL for uploaded profile picture
                profile_picture_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{filename}"
            except NoCredentialsError:
                flash('AWS credentials not available. Profile picture upload failed.', 'error')
                return redirect(request.url)
        else:
            # If no profile picture is provided, retain the existing profile picture URL
            profile_picture_url = user['profilepicture']

        # Update user profile in the database
        success = fitness_repo.update_user_profile(
            userid=session['userid'],
            email=email,
            firstname=firstname,
            lastname=lastname,
            username=username,
            dateofbirth=dateofbirth,
            gender=gender,
            height=height,
            weight=weight,
            profilepicture=profile_picture_url  # Use existing URL or the new one if provided
        )

        if success:
            flash('Profile updated successfully!', 'success')
        else:
            flash('Failed to update profile. Please try again.', 'error')

        return redirect(url_for('updateprofile'))

    # Fetch user data for rendering the profile page
    user = fitness_repo.get_user_by_id(session['userid'])
    return render_template('updateprofile.html', user=user)



@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    user = fitness_repo.get_user_by_id((session['userid']))
    if request.method == 'POST':
        # Delete the user's account and redirect to signup page
        success = fitness_repo.remove_user_data(session['userid'])
        if success:
            flash('Account successfully deleted! Please LOGOUT', 'success')
            return redirect(url_for('signup'))
        else:
            flash('Failed to delete account. Please try again.', 'error')
            return redirect(url_for('profile'))  # Redirect back to profile page if deletion fails

    # If the request method is GET, render the confirmation template
    return render_template('profile.html', user=user)






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

