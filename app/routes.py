# Flask imports
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message

# Database and models
from . import db
from .models import User, Chat, Appointment, Availability

# Security
from werkzeug.security import generate_password_hash, check_password_hash

# AI and API clients
import openai
from openai import OpenAI
import anthropic

# System imports
import sys
import requests



def get_openai_client():
    api_key = current_app.config['OPENAI_API_KEY']
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    return OpenAI(api_key=api_key)

def get_anthropic_client():
    ant_api_key = current_app.config['ANTHROPIC_API_KEY']
    if not ant_api_key:
        raise ValueError("ANTHROPIC API key not configured")
    return anthropic.Anthropic(api_key=ant_api_key)


######################################-----REGISTRATION-----######################################
main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    # Get data from the request
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')  # Default to "student" if not provided

    # Input validation
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    if role not in ['student', 'professional']:
        return jsonify({'error': 'Invalid role. Must be "student" or "professional"'}), 400

    # Check if the user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )

    # Add to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

######################################-----lOGIN-----######################################

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password, password):
        # Generate a JWT token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'role': user.role
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


######################################-----GET APPOINTMENTS-----######################################

# @main_bp.route('/professionals', methods=['GET'])
# @jwt_required()
# def get_professionals():
#     try:
#         print("Starting get_professionals endpoint")
#         sys.stdout.flush()
#         print("Getting JWT identity...")
#         user_identity = get_jwt_identity()
#         print(f"JWT identity received: {user_identity}")
        
#         print("Querying user from database...")
#         user = User.query.get(user_identity['id'])
#         print(f"User found: {user}")
#         print(f"User role: {user.role if user else 'No user found'}")

#         if not user or user.role != 'student':
#             print("Authorization check failed")
#             return jsonify({'error': 'Unauthorized'}), 401

#         print("Getting professionals from database...")
#         professionals = User.query.filter_by(role='professional').all()
#         print(f"Found {len(professionals)} professionals")

#         result = []
#         print("Processing each professional...")
#         for idx, professional in enumerate(professionals):
#             print(f"Processing professional {idx + 1}: ID={professional.id}")
            
#             print("Getting availability for professional...")
#             availability = Availability.query.filter_by(professional_id=professional.id).all()
#             print(f"Found {len(availability)} availability slots")
            
#             slots = []
#             for slot in availability:
#                 print(f"Processing slot: date={slot.date}, start={slot.start_time}, end={slot.end_time}")
#                 slots.append({
#                     'date': str(slot.date),
#                     'start_time': str(slot.start_time),
#                     'end_time': str(slot.end_time)
#                 })
            
#             prof_data = {
#                 'id': str(professional.id),
#                 'name': professional.username,
#                 'email': professional.email,
#                 'availability': slots
#             }
#             print(f"Created professional data: {prof_data}")
#             result.append(prof_data)

#         print("Preparing final response...")
#         print(f"Final result: {result}")
#         return jsonify(result), 200

#     except Exception as e:
#         print(f"ERROR OCCURRED: {str(e)}")
#         print(f"Error type: {type(e)}")
#         import traceback
#         print(f"Traceback: {traceback.format_exc()}")
#         return jsonify({'error': str(e)}), 500



@main_bp.route('/professionals', methods=['GET'])
def get_professionals():
    try:
        # Fetch all professionals
        professionals = User.query.filter_by(role='professional').all()

        # Format the response
        result = []
        for professional in professionals:
            availability = Availability.query.filter_by(professional_id=professional.id).all()
            slots = [
                {
                    'date': str(slot.date),
                    'start_time': str(slot.start_time),
                    'end_time': str(slot.end_time)
                }
                for slot in availability
            ]
            result.append({
                'id': str(professional.id),
                'name': professional.username,
                'email': professional.email,
                'availability': slots
            })

        return jsonify(result), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500



######################################-----BOOK APPOINTMENTS-----######################################

# @main_bp.route('/book_appointment', methods=['POST'])
# @jwt_required()
# def book_appointment():
#     data = request.json
#     user_identity = get_jwt_identity()
#     user = User.query.get(user_identity['id'])

#     # Ensure the user is a student
#     if not user or user.role != 'student':
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Validate input data
#     professional_id = data.get('professional_id')
#     appointment_date = data.get('appointment_date')
#     appointment_time = data.get('appointment_time')

#     if not professional_id or not appointment_date or not appointment_time:
#         return jsonify({'error': 'Professional, date, and time are required'}), 400

#     # Validate professional
#     professional = User.query.get(professional_id)
#     if not professional or professional.role != 'professional':
#         return jsonify({'error': 'Invalid professional ID'}), 400

#     # Validate appointment time against availability
#     from datetime import time

#     selected_time = time.fromisoformat(appointment_time)
#     availability = Availability.query.filter_by(professional_id=professional.id, date=appointment_date).all()
#     is_valid_time = any(
#         slot.start_time <= selected_time <= slot.end_time
#         for slot in availability
#     )
#     if not is_valid_time:
#         return jsonify({'error': 'Selected time slot is not available'}), 400

#     # Save the appointment
#     appointment = Appointment(
#         user_id=user.id,
#         professional_id=professional.id,
#         appointment_time=f"{appointment_date}T{appointment_time}"
#     )
#     db.session.add(appointment)
#     db.session.commit()


@main_bp.route('/book_appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.json
        
        # Get required data from request
        professional_id = data.get('professional_id')
        date = data.get('date')
        start_time = data.get('start_time')
        
        if not professional_id or not date or not start_time:
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if slot is available
        availability = Availability.query.filter_by(
            professional_id=professional_id,
            date=date,
            start_time=start_time
        ).first()

        if not availability:
            return jsonify({'error': 'Slot not available'}), 400

        # Create appointment using the correct table structure
        from datetime import datetime
        appointment = Appointment(  # Note: Use your actual model name
            user_id=1,  # Hardcoded for now
            professional_id=professional_id,
            appointment_time=f"{date}T{start_time}",
            created_at=datetime.utcnow()
        )

        # Save appointment and delete availability
        db.session.add(appointment)
        db.session.delete(availability)
        db.session.commit()

        return jsonify({'message': 'Appointment booked successfully'}), 201

    except Exception as e:
        print("Error:", str(e))
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

######################################-----add AVAILABILITY----######################################

@main_bp.route('/availability/add', methods=['POST'])
@jwt_required()
def add_availability():
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity['id'])

    # Ensure the user is a professional
    if not user or user.role != 'professional':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not date or not start_time or not end_time:
        return jsonify({'error': 'Date, start time, and end time are required'}), 400

    # Add availability slot
    availability = Availability(
        professional_id=user.id,
        date=date,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(availability)
    db.session.commit()

    return jsonify({'message': 'Availability added successfully'}), 201


####################---chat test----##############################

@main_bp.route('/chat/send', methods=['POST'])
def send_message():
    try:
        client = get_anthropic_client()
        # Step 1: Get the message from the request
        data = request.json
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Step 2: Call the Anthropic API with the wellness guide system prompt
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system="""You are Wayne Wellness Guide, a counselor specializing in student wellness. 
            Your primary role is to support students' mental health and academic well-being.
            
            TRIGGER WORDS AND PHRASES TO MONITOR:
            - Self-harm related: "cut myself", "hurt myself", "end it all", "don't want to be here"
            - Depression indicators: "worthless", "hopeless", "can't go on", "giving up"
            - Anxiety triggers: "panic attack", "can't breathe", "overwhelming fear", "constant worry"
            - Suicidal thoughts: "want to die", "better off dead", "no point in living"
            - Academic distress: "can't handle the pressure", "want to quit school", "complete failure"
            - Eating disorders: "hate my body", "not eating", "purging"
            - Substance use: "drinking to cope", "need drugs to function"
            - Trauma: "flashbacks", "nightmares", "can't get over it"

            WHEN THESE TRIGGERS ARE DETECTED, RESPOND WITH:
            1. IMMEDIATE EMPATHY:
            "I hear how much pain/difficulty you're experiencing. What you're going through is really challenging, 
            and it takes courage to talk about it."

            2. VALIDATE FEELINGS:
            "It's completely understandable to feel this way. Many students face similar struggles, 
            and it's okay to need support."

            3. PROFESSIONAL RECOMMENDATION:
            "I want to make sure you get the best possible support. We have caring professionals 
            who specialize in helping students through exactly these kinds of situations. They're here 
            to listen without judgment and can provide you with effective strategies and support."

            4. ENCOURAGE BOOKING:
            "Would you be open to booking a session with one of our professional counselors? 
            They have extensive experience helping students navigate these challenges and can provide 
            you with personalized support and coping strategies. You can easily book a session through 
            our platform, and everything remains completely confidential."

            5. IMMEDIATE CRISIS RESOURCES:
            If the situation seems urgent, also provide:
            "If you need immediate support, the National Crisis Helpline is available 24/7 at 988, 
            and your campus counseling center has emergency services available."

            Always maintain a warm, supportive tone while gently but firmly encouraging professional help.
            For non-crisis situations, provide practical advice and coping strategies alongside the 
            recommendation for professional support.""",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        }
                    ]
                }
            ]
        )

        # Step 3: Extract the response
        claude_response = response.content[0].text

        # Step 4: Return the response to the user
        return jsonify({'message': claude_response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500