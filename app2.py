from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random
import pickle
import os
from sqlalchemy import create_engine
import psycopg2
from sklearn.linear_model import LogisticRegression
from joblib import dump
from mysql import connector
from savings import app
from savings import routs

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Database and Mail Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://neondb_owner:npg_WbBu08ndNvmL@ep-noisy-dust-a8k2z0xf-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mrshreyash08@gmail.com'
app.config['MAIL_PASSWORD'] = 'npyn kbyd ufbt otrc'
mail = Mail(app)

model = pickle.load(open('diabetes_model.pkl', 'rb'))


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6), nullable=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(20), nullable=False)    

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        otp = str(random.randint(100000, 999999))  # Generate OTP

        # Save user with OTP
        user = User(name=name, address=address, email=email, password=password, otp=otp)
        db.session.add(user)
        db.session.commit()

        # Send OTP to email
        msg = Message('Your OTP for Signup', sender='your_email@gmail.com', recipients=[email])
        msg.body = f'Your OTP is: {otp}'
        mail.send(msg)

        flash('An OTP has been sent to your email. Please verify.', 'info')
        session['user_email'] = email  # Store email in session for verification
        return redirect(url_for('verify_otp'))
    return render_template('signup.html')

# OTP Verification Route
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('user_email')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User session expired. Please sign up again.', 'danger')
        return redirect(url_for('signup'))

    if request.method == 'POST':
        otp = request.form['otp']

        if user.otp == otp:
            user.otp = None  # Clear OTP after successful verification
            db.session.commit()
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html', user=user)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Collect user inputs
        inputs = [float(request.form[key]) for key in ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]

        # Get the prediction and confidence level (probability)
        prediction = model.predict([inputs])[0]
        prediction_prob = model.predict_proba([inputs])[0][prediction]  # Confidence/probability for the predicted class
        
        # Format confidence to 2 decimal places
        formatted_confidence = round(prediction_prob * 100, 2)  # Convert to percentage and round to 2 decimal places

        result = 'Positive' if prediction == 1 else 'Negative'

        # Store prediction in DB
        prediction_entry = Prediction(user_id=session['user_id'], result=result)
        db.session.add(prediction_entry)
        db.session.commit()

        # Friendly message based on the result
        if result == 'Positive':
            flash("Don't worry, early detection helps! Consult a doctor for better management.", 'warning')
        else:
            flash("Great! Keep maintaining a healthy lifestyle. You're doing awesome!", 'success')

        # Pass prediction, confidence, and result to the template
        return render_template('result.html', result=result, confidence=formatted_confidence)

    return render_template('predict.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))  # Redirect to home page after logout



# Home Route
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures the database tables are created within the application context
    app.run(debug=True)

