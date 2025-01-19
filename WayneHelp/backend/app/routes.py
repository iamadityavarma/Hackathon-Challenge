from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import db
from .models import User, Chat, Appointment, Availability
from flask_mail import Message
import openai
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db

# from .models import Chat
from openai import OpenAI
import anthropic


def get_openai_client():
    api_key = current_app.config["OPENAI_API_KEY"]
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    return OpenAI(api_key=api_key)


def get_anthropic_client():
    ant_api_key = current_app.config["ANTHROPIC_API_KEY"]
    if not ant_api_key:
        raise ValueError("ANTHROPIC API key not configured")
    return anthropic.Anthropic(api_key=ant_api_key)


######################################-----REGISTRATION-----######################################
main_bp = Blueprint("main", __name__)


# @main_bp.route("/register", methods=["POST"])
# def register():
#     # Get data from the request
#     data = request.json
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")
#     role = data.get("role", "student")  # Default to "student" if not provided

#     # Input validation
#     if not username or not email or not password:
#         return jsonify({"error": "Username, email, and password are required"}), 400

#     if role not in ["student", "professional"]:
#         return (
#             jsonify({"error": 'Invalid role. Must be "student" or "professional"'}),
#             400,
#         )

#     # Check if the user already exists
#     existing_user = User.query.filter(
#         (User.username == username) | (User.email == email)
#     ).first()
#     if existing_user:
#         return jsonify({"error": "Username or email already exists"}), 409

#     # Hash the password
#     hashed_password = generate_password_hash(password)

#     # Create a new user
#     new_user = User(username=username, email=email, password=hashed_password, role=role)

#     # Add to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({"message": "Registration successful"}), 201


@main_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")  # Default role is 'student'

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if role not in ["student", "professional"]:
        return (
            jsonify({"error": 'Invalid role. Must be "student" or "professional"'}),
            400,
        )

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


######################################-----lOGIN-----######################################


@main_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password, password):
        # Generate a JWT token
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "role": user.role,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Invalid username or password"}), 401


##############--------CHAT---------####################

# @main_bp.route('/chat/send', methods=['POST'])
# @jwt_required()
# def send_message():
#    client = get_openai_client()
#    user_identity = get_jwt_identity()
#    data = request.json
#    user_message = data.get('message')

#    if not user_message:
#        return jsonify({'error': 'Message is required'}), 400

#    # Get previous messages from database for this user
#    previous_chats = Chat.query.filter_by(
#        user_id=user_identity['id']
#    ).order_by(Chat.timestamp.desc()).limit(5).all()  # Last 5 messagess

#    # Build conversation with all messages
#    messages=[
#             {"role": "system", "content": "You are a wellness counselor."},
#             {"role": "user", "content": user_message}
#         ]

#    # Add previous messages to context
#    for chat in reversed(previous_chats):
#        if not chat.is_temp:  # If it's a user message
#            messages.append({"role": "user", "content": chat.message})
#        else:  # If it's an AI response
#            messages.append({"role": "assistant", "content": chat.message})

#    # Add new message
#    messages.append({"role": "user", "content": user_message})

#    try:
#        # Call OpenAI API with your custom instructions
#        response = client.chat.completions.create(
#            model="gpt-4",
#            messages=messages
#        )

#        gpt_response = response.choices[0].message.content

#        # Save the chat in the database
#        chat = Chat(user_id=user_identity['id'], message=user_message, is_temp=False)
#        db.session.add(chat)

#        # Save GPT response
#        chat_response = Chat(user_id=user_identity['id'], message=gpt_response, is_temp=True)
#        db.session.add(chat_response)

#        db.session.commit()

#        return jsonify({'message': gpt_response}), 200

#    except Exception as e:
#        return jsonify({'error': f'Error processing chat: {str(e)}'}), 500

######################################-----GET APPOINTMENTS-----######################################


@main_bp.route("/professionals", methods=["GET"])
@jwt_required()
def get_professionals():
    # Ensure the user is a student
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity["id"])
    if not user or user.role != "student":
        return jsonify({"error": "Unauthorized"}), 401

    # Fetch all professionals and their availability
    professionals = User.query.filter_by(role="professional").all()

    # Format the response
    result = []
    for professional in professionals:
        availability = Availability.query.filter_by(
            professional_id=professional.id
        ).all()
        slots = [
            {
                "date": str(slot.date),
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
            for slot in availability
        ]
        result.append(
            {
                "id": professional.id,
                "name": professional.username,
                "email": professional.email,
                "availability": slots,
            }
        )

    return jsonify(result), 200


######################################-----BOOK APPOINTMENTS-----######################################


@main_bp.route("/book_appointment", methods=["POST"])
@jwt_required()
def book_appointment():
    data = request.json
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity["id"])

    # Ensure the user is a student
    if not user or user.role != "student":
        return jsonify({"error": "Unauthorized"}), 401

    # Validate input data
    professional_id = data.get("professional_id")
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")

    if not professional_id or not appointment_date or not appointment_time:
        return jsonify({"error": "Professional, date, and time are required"}), 400

    # Validate professional
    professional = User.query.get(professional_id)
    if not professional or professional.role != "professional":
        return jsonify({"error": "Invalid professional ID"}), 400

    # Validate appointment time against availability
    from datetime import time

    selected_time = time.fromisoformat(appointment_time)
    availability = Availability.query.filter_by(
        professional_id=professional.id, date=appointment_date
    ).all()
    is_valid_time = any(
        slot.start_time <= selected_time <= slot.end_time for slot in availability
    )
    if not is_valid_time:
        return jsonify({"error": "Selected time slot is not available"}), 400

    # Save the appointment
    appointment = Appointment(
        user_id=user.id,
        professional_id=professional.id,
        appointment_time=f"{appointment_date}T{appointment_time}",
    )
    db.session.add(appointment)
    db.session.commit()

    # Send email notification

    # try:
    #     msg = Message(
    #         subject="New Appointment Booking",
    #         recipients=[professional.email],
    #         body=f"Appointment Details:\nStudent: {user.username}\nDate: {appointment_date}\nTime: {appointment_time}"
    #     )
    #     mail.send(msg)
    # except Exception as e:
    #     return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

    # return jsonify({'message': 'Appointment booked successfully'}), 201


######################################-----AVAILABILITY----######################################


@main_bp.route("/availability/add", methods=["POST"])
@jwt_required()
def add_availability():
    user_identity = get_jwt_identity()
    user = User.query.get(user_identity["id"])

    # Ensure the user is a professional
    if not user or user.role != "professional":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not date or not start_time or not end_time:
        return jsonify({"error": "Date, start time, and end time are required"}), 400

    # Add availability slot
    availability = Availability(
        professional_id=user.id, date=date, start_time=start_time, end_time=end_time
    )
    db.session.add(availability)
    db.session.commit()

    return jsonify({"message": "Availability added successfully"}), 201


####################---chat test----##############################


@main_bp.route("/chat/send", methods=["POST"])
def send_message():
    try:
        client = get_anthropic_client()
        # Step 1: Get the message from the request
        data = request.json
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

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
                {"role": "user", "content": [{"type": "text", "text": user_message}]}
            ],
        )

        # Step 3: Extract the response
        claude_response = response.content[0].text

        # Step 4: Return the response to the user
        return jsonify({"message": claude_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
