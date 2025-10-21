from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'role_name': self.role_name
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    role = db.relationship('Role')
    cars = db.relationship('Car', backref='owner', lazy=True)
    appointments = db.relationship('Appointment', backref='customer', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email,
            'role_id': self.role_id
        }

class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_model = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'car_model': self.car_model,
            'license_plate': self.license_plate,
            'owner_id': self.owner_id
        }

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # La duración es en minutos, ojo!
    slots_required = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'slots_required': self.slots_required
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service = db.relationship('Service', backref='appointments')
    status = db.Column(db.String(50), default="pending")
    
    comments = db.relationship('Comment', backref='appointment', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'user_id': self.user_id,
            'car_id': self.car_id,
            'service_id': self.service_id,
            'status': self.status
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)
    is_mechanic = db.Column(db.Boolean, nullable=False, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'author_id': self.author_id,
            'content': self.content,
            'timestamp': self.timestamp,
            'is_mechanic': self.is_mechanic
        }

class Setting(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    max_appointments_per_hour = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'max_appointments_per_hour': self.max_appointments_per_hour
        }

class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(100), nullable=False, unique=True)

# Modelos para gestión económica
class Income(db.Model):
    __tablename__ = 'incomes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client_name = db.Column(db.String(100), nullable=True)
    car_license_plate = db.Column(db.String(20), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    appointment = db.relationship('Appointment', backref='income')
    creator = db.relationship('User', backref='created_incomes')
    
    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date,
            'client_name': self.client_name,
            'car_license_plate': self.car_license_plate,
            'appointment_id': self.appointment_id,
            'created_by': self.created_by
        }

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # impuestos, alquiler, luz, gas, sueldo, etc.
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    creator = db.relationship('User', backref='created_expenses')
    
    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'date': self.date,
            'created_by': self.created_by
        }

class FinancialGoal(db.Model):
    __tablename__ = 'financial_goals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    target_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    creator = db.relationship('User', backref='created_goals')
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'start_date': self.start_date,
            'target_date': self.target_date,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'progress_percentage': (self.current_amount / self.target_amount * 100) if self.target_amount > 0 else 0
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'user_id': self.user_id,
            'appointment_id': self.appointment_id,
            'created_at': self.created_at,
            'read': self.read
        }

class EmailNotification(db.Model):
    __tablename__ = 'email_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    to_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'to_email': self.to_email,
            'subject': self.subject,
            'body': self.body,
            'status': self.status,
            'created_at': self.created_at,
            'sent_at': self.sent_at
        }