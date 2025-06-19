from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({'error': 'All fields are required'}), 400

    body = f"Contact Form Submission\n\nName: {name}\nEmail: {email}\nMessage: {message}"
    if send_email('New Contact Form Submission', body, 'learnzoneaz@gmail.com'):
        return jsonify({'message': 'Message sent successfully'}), 200
    return jsonify({'error': 'Failed to send message'}), 500

@app.route('/api/enroll', methods=['POST'])
def enroll():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    contact = data.get('contact')
    course = data.get('course')

    if not all([name, email, contact, course]):
        return jsonify({'error': 'All fields are required'}), 400

    body = f"Enrollment Form Submission\n\nName: {name}\nEmail: {email}\nContact: {contact}\nCourse: {course}"
    if send_email('New Enrollment', body, 'learnzoneaz@gmail.com'):
        return jsonify({'message': 'Enrollment successful'}), 200
    return jsonify({'error': 'Failed to process enrollment'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email and password:
        return jsonify({'message': 'Login successful', 'token': 'dummy-token'}), 200
    return jsonify({'error': 'Invalid credentials'}), 400

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    body = f"Password Reset Request\n\nA password reset was requested for {email}."
    if send_email('Password Reset Request', body, 'learnzoneaz@gmail.com'):
        return jsonify({'message': 'Password reset email sent'}), 200
    return jsonify({'error': 'Failed to send reset email'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
