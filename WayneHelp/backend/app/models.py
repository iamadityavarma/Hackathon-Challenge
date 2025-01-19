# # from datetime import datetime, date, time
# # from . import db

# # # User Model
# # class User(db.Model):
# #     __tablename__ = 'users'

# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(50), unique=True, nullable=False)
# #     email = db.Column(db.String(120), unique=True, nullable=False)
# #     password = db.Column(db.String(200), nullable=False)
# #     role = db.Column(db.String(20), nullable=False)  # "student" or "professional"
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# #     # Relationships
# #     appointments = db.relationship('Appointment', back_populates='student', foreign_keys='Appointment.user_id')
# #     availability = db.relationship('Availability', back_populates='professional', foreign_keys='Availability.professional_id')

# #     def __repr__(self):
# #         return f"<User {self.username}, Role: {self.role}>"

# # # Availability Model
# # class Availability(db.Model):
# #     __tablename__ = 'availability'

# #     id = db.Column(db.Integer, primary_key=True)
# #     professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     date = db.Column(db.Date, nullable=False)
# #     start_time = db.Column(db.Time, nullable=False)
# #     end_time = db.Column(db.Time, nullable=False)

# #     # Relationships
# #     professional = db.relationship('User', back_populates='availability', foreign_keys=[professional_id])

# #     def __repr__(self):
# #         return f"<Availability Professional: {self.professional_id}, Date: {self.date}, Time: {self.start_time}-{self.end_time}>"

# # # Appointment Model
# # class Appointment(db.Model):
# #     __tablename__ = 'appointments'

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Student
# #     professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Professional
# #     appointment_time = db.Column(db.DateTime, nullable=False)
# #     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# #     # Relationships
# #     student = db.relationship('User', back_populates='appointments', foreign_keys=[user_id])
# #     professional = db.relationship('User', foreign_keys=[professional_id])

# #     def __repr__(self):
# #         return f"<Appointment Student: {self.user_id}, Professional: {self.professional_id}, Time: {self.appointment_time}>"

# # # Chat Model
# # class Chat(db.Model):
# #     __tablename__ = 'chats'

# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     message = db.Column(db.Text, nullable=False)
# #     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# #     is_temp = db.Column(db.Boolean, default=False)  # For temporary (incognito) chats

# #     # Relationships
# #     user = db.relationship('User', foreign_keys=[user_id])

# #     def __repr__(self):
# #         return f"<Chat User: {self.user_id}, Timestamp: {self.timestamp}, Temp: {self.is_temp}>"


# from datetime import datetime, date, time
# from . import db

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     appointments = db.relationship('Appointment',
#                                  backref='student',
#                                  primaryjoin="User.id==Appointment.user_id")
#     availability = db.relationship('Availability',
#                                  backref='professional',
#                                  foreign_keys='Availability.professional_id')

#     def __repr__(self):
#         return f"<User {self.username}, Role: {self.role}>"

# # Availability Model
# class Availability(db.Model):
#     __tablename__ = 'availability'

#     id = db.Column(db.Integer, primary_key=True)
#     professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     start_time = db.Column(db.Time, nullable=False)
#     end_time = db.Column(db.Time, nullable=False)

#     # Relationships
#     professional = db.relationship('User', back_populates='availability', foreign_keys=[professional_id])

#     def __repr__(self):
#         return f"<Availability Professional: {self.professional_id}, Date: {self.date}, Time: {self.start_time}-{self.end_time}>"

# # Appointment Model
# class Appointment(db.Model):
#     __tablename__ = 'appointments'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     professional_id = db.Column(db.Integer, nullable=False)
#     appointment_time = db.Column(db.DateTime, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<Appointment Student: {self.user_id}, Professional: {self.professional_id}, Time: {self.appointment_time}>"

# # Chat Model
# class Chat(db.Model):
#     __tablename__ = 'chats'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     is_temp = db.Column(db.Boolean, default=False)  # For temporary (incognito) chats

#     # Relationships
#     user = db.relationship('User', foreign_keys=[user_id])

#     def __repr__(self):
#         return f"<Chat User: {self.user_id}, Timestamp: {self.timestamp}, Temp: {self.is_temp}>"


from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Text, nullable=False)
    end_time = db.Column(db.Text, nullable=False)


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    professional_id = db.Column(db.Integer, nullable=False)
    appointment_time = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_temp = db.Column(db.Boolean, default=False)
