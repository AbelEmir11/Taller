"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User, Role, Car, Appointment, Service, Comment, Setting, TokenBlockList, Income, Expense, FinancialGoal, Notification

from flask import Flask
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import traceback

app = Flask(__name__)
bcrypt = Bcrypt(app)

api = Blueprint('api', __name__)
CORS(api)


# // post en /create users from admin
@api.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')
    role_id = data.get('role_id')

    if not email or not password or not name or not phone_number or not role_id:
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, name=name, phone_number=phone_number, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "user": new_user.serialize(),
    }
    return jsonify(response_body), 201

# // post en /signup
@api.route('/signupuser', methods=['POST'])
def create_signupusers():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')

    if not email or not password or not name or not phone_number:
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, name=name, phone_number=phone_number, role_id=3)
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "phone_number": new_user.phone_number,
    }
    return jsonify(response_body), 201


# // post en /login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    role = Role.query.filter_by(id=user.role_id).first()
    access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id})
    return jsonify(access_token=access_token, role_id=role.id, user_id=user.id), 200
# @api.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({"error": "Email and password are required"}), 400

#     email = data.get('email')
#     password = data.get('password')

#     user = User.query.filter_by(email=email).first()
#     if not user or not bcrypt.check_password_hash(user.password, password):
#         # Incrementar el contador de intentos fallidos
#         # user.failed_login_attempts += 1
#         # if user.failed_login_attempts >= 5:
#         #     # Bloquear la cuenta temporalmente
#         #     user.is_blocked = True
#         #     db.session.commit()
#         #     return jsonify({"error": "Account blocked due to excessive login attempts"}), 401
#         # return jsonify({"error": "Invalid credentials"}), 401

#     role = Role.query.filter_by(id=user.role_id).first()
#     if not role:
#         return jsonify({"error": "Invalid role"}), 401

#     access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id})
#     # access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id}, expires_in=3600)
#     return jsonify(access_token=access_token, role_id=role.id, user_id=user.id), 200

# / post en /ping user
@api.route('/pinguser', methods=['GET'])
@jwt_required()
def ping_user():
    print("Iniciando ping_user")
    current_user_id = get_jwt_identity()
    payload = get_jwt()
    
    print("current_user_id:", current_user_id)
    print("JWT Payload:", payload)
    
    if "role_id" not in payload:
        print("Role ID no encontrado en el token")
        return jsonify({"error": "Role ID not found in token"}), 400
    
    role_id = payload["role_id"]
    print("Role ID:", role_id)

    response = jsonify({"message": "User is authenticated", "user_id": current_user_id, "role_id": role_id})
    print("Respuesta enviada:", response)
    
    return response, 200


# // post en /logout
@api.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    token_blocked = TokenBlockList(jti=jti)
    db.session.add(token_blocked)
    db.session.commit()
    return jsonify({"msg": "Logout successful"})

# / get a /users con id
@api.route('/users/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user(user_id):
    user_query = User.query.filter_by(id=user_id).first()
    if user_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": user_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No existe" 
        }
        return jsonify(response_body), 404
    
#// DELETE a /users con id
@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"error": "User not found"}), 404

    appointments = Appointment.query.filter_by(user_id=user_id).all()
    if not appointments:
        return jsonify({"error": "No appointments found for this user"}), 404

    for appointment in appointments:
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(appointment)

    cars = Car.query.filter_by(owner_id=user_id).all()
    if not cars:
        return jsonify({"error": "No cars found for this user"}), 404

    for car in cars:
        db.session.delete(car)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User and related data deleted successfully"}), 200

   
#////////////// get a /services con id
@api.route('/services/<int:services_id>', methods=['GET'])
@jwt_required()
def get_service(services_id):
    service_query = Service.query.filter_by(id=services_id).first()
    if service_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": service_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "Service no exist" 
        }
        return jsonify(response_body), 404

# //////////////////////// GET a /cars 
@api.route('/cars', methods=['GET'])
@jwt_required()
def get_all_cars():
    cars = Car.query.all()
    car_list = [car.serialize() for car in cars]
    return jsonify(car_list), 200

    
# ////////////////////// get a /cars con id
@api.route('/cars/<int:car_id>', methods=['GET'])
@jwt_required()
def get_cars(car_id):
    car_query = Car.query.filter_by(id=car_id).first()
    if car_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": car_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "Car no exist" 
        }
        return jsonify(response_body), 404
    

# // get a /cars/user con id del user
@api.route('/cars/user/<int:owner_id>', methods=['GET'])
@jwt_required()
def get_user_cars(owner_id):
    cars_query = Car.query.filter_by(owner_id=owner_id).all()
    if cars_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": [car.serialize() for car in cars_query]
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No cars found for this user" 
        }
        return jsonify(response_body), 404

# / post a /cars 
@api.route('/cars', methods=['POST'])
@jwt_required()
def create_car():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    car_model = data.get('car_model')
    license_plate = data.get('license_plate')
    user_id = data.get('user_id')
    if not car_model or not license_plate or not user_id:
        return jsonify({"error": "Car model, license plate, and user ID are required"}), 400
    existing_user = User.query.filter_by(id=user_id).first()
    if not existing_user:
        return jsonify({"error": "Bad user_id"}), 400

    new_car = Car(car_model=car_model, license_plate=license_plate, owner_id=user_id)
    db.session.add(new_car)
    db.session.commit()

    response_body = new_car.serialize()
    return jsonify(response_body), 201

#// PATCH a /cars + id 
@api.route('/cars/<int:car_id>', methods=['PATCH'])
@jwt_required()
def update_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    data = request.get_json()
    car_model = data.get('car_model')
    license_plate = data.get('license_plate')

    if car_model:
        car.car_model = car_model
    if license_plate:
        car.license_plate = license_plate

    db.session.commit()
    return jsonify(car.serialize()), 200

# / DELETE a /cars + id 
@api.route('/cars/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    associated_appointments = Appointment.query.filter_by(car_id=car_id).all()
    if associated_appointments:
        return jsonify({"error": "Cannot delete car because it is associated with an appointment"}), 400

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200


# / GET a /comments?appointment_id=
@api.route('/comments', methods=['GET'])
@jwt_required()
def get_comments():
    appointment_id = request.args.get('appointment_id')
    if appointment_id:
        comments_query = Comment.query.filter_by(appointment_id=appointment_id).all()
        comments_list = list(map(lambda comment: comment.serialize(), comments_query))
        return jsonify(comments_list), 200
    else:
        return jsonify({"msg": "No appointment_id provided"}), 400


# // post a /comments 
@api.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    comment_content = data.get('comment')
    user_id = data.get('user_id')
    appointment_id = data.get('appointment_id')
    is_mechanic = data.get('is_mechanic', False) 

    if not comment_content or not user_id or not appointment_id:
        return jsonify({"error": "Comment, user ID, and appointment ID are required"}), 400

    new_comment = Comment(
        content=comment_content,
        author_id=user_id,
        appointment_id=appointment_id,
        is_mechanic=is_mechanic
    )
    db.session.add(new_comment)
    db.session.commit()

    response_body = new_comment.serialize()
    return jsonify(response_body), 201



# // post a /services 
@api.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    name = data.get('name')
    description = data.get('description')
    duration = data.get('duration')
    slots_required = data.get('slots_required')
    if not name or not description or not duration or not slots_required:
        return jsonify({"error": "Name, description,slots_required and duration are required"}), 400

    new_service = Service(name=name, description=description, duration=duration, slots_required=slots_required)
    db.session.add(new_service)
    db.session.commit()

    response_body = new_service.serialize()
    return jsonify(response_body), 201

# /// get a /services 
@api.route('/services', methods=['GET'])
def get_services():
    services_query = Service.query.all()
    services_list = list(map(lambda service: service.serialize(), services_query))
    return jsonify(services_list), 200


# //// post a /settings 
@api.route('/settings', methods=['POST'])
@jwt_required()
def create_setting():
    data = request.get_json()
    max_appointments_per_hour = data.get('max_appointments_per_hour')
    if max_appointments_per_hour is None:
        return jsonify({"error": "Max appointments per hour is required"}), 400

    setting = Setting.query.first()
    if setting:
        setting.max_appointments_per_hour = max_appointments_per_hour
    else:
        setting = Setting(max_appointments_per_hour=max_appointments_per_hour)
        db.session.add(setting)
    db.session.commit()

    response_body = setting.serialize()
    return jsonify(response_body), 201


# / get a /settings 
@api.route('/settings', methods=['GET'])
# @jwt_required()
def get_setting():
    setting = Setting.query.first()
    if setting:
        response_body = setting.serialize()
        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Settings not configured"}), 404
    
# // get a /users 
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users_query = User.query.all()
    users_list = list(map(lambda user: user.serialize(), users_query))
    return jsonify(users_list), 200

# ///// post a /appointments 
@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    date = data.get('date')
    user_id = data.get('user_id')
    car_id = data.get('car_id')
    service_id = data.get('service_id')
    comment = data.get('comment')
    
    if not date or not user_id or not car_id or not service_id:
        return jsonify({"error": "Date, user ID, car ID, and service ID are required"}), 400
    
    existing_user = User.query.filter_by(id=user_id).first()
    if not existing_user:
        return jsonify({"error": "Bad user_id"}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    max_appointments_per_hour = Setting.query.first().max_appointments_per_hour   

    # Verificar citas existentes en la misma hora
    start_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    start_time = start_time.replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    appointments_in_hour = Appointment.query.filter(  
        Appointment.date >= start_time,  
        Appointment.date < end_time  
    ).all()

    total_slots_booked = sum([app.service.slots_required for app in appointments_in_hour])  

    if (total_slots_booked + service.slots_required) <= max_appointments_per_hour:  
        new_appointment = Appointment(
            date=start_time,
            user_id=user_id,
            car_id=car_id,
            service_id=service_id,
            status="pending"
        )
        db.session.add(new_appointment)
        db.session.commit()

        if comment:
            new_comment = Comment(
                content=comment,
                author_id=user_id,
                appointment_id=new_appointment.id,
                is_mechanic=False
            )
            db.session.add(new_comment)
            db.session.commit()

        response_body = new_appointment.serialize()
        return jsonify(response_body), 201
    else:
        return jsonify({"error": "No available slots for this time"}), 400

# /// PATCH a /appointments con id - VERSIÓN CORREGIDA
@api.route('/appointments/<int:appointment_id>', methods=['PATCH'])
@jwt_required()
def update_appointment(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        status = data.get('status')
        created_notification = False
        
        if status:
            appointment.status = status

            # Si el estado cambia a completed -> crear notificación interna para admin
            if status and status.lower() == "completed":
                try:
                    # Verificar si ya existe una notificación para este appointment
                    existing_notification = Notification.query.filter_by(
                        appointment_id=appointment_id
                    ).first()
                    
                    if not existing_notification:
                        # Obtener datos relacionados de forma segura
                        car = Car.query.get(appointment.car_id) if appointment.car_id else None
                        service = Service.query.get(appointment.service_id) if appointment.service_id else None
                        license_plate = car.license_plate if car else 'N/A'
                        service_name = service.name if service else 'Servicio'

                        admin_notification = Notification(
                            title="🔧 Trabajo Completado",
                            message=f"El trabajo del vehículo {license_plate} ({service_name}) ha sido completado y está listo para ser retirado.",
                            user_id=16,  # admin por defecto
                            appointment_id=appointment.id,
                            read=False
                        )
                        db.session.add(admin_notification)
                        created_notification = True
                        print(f"✅ Notificación creada para appointment {appointment_id}")
                    else:
                        print(f"⚠️ Ya existe notificación para appointment {appointment_id}")
                        
                except Exception as notif_err:
                    # No bloquear la actualización por un fallo en la notificación
                    print(f"❌ Error creando notificación al actualizar cita: {str(notif_err)}")
                    import traceback
                    print(traceback.format_exc())

        db.session.commit()
        
        resp = {
            "msg": "Appointment updated successfully",
            "appointment": appointment.serialize()
        }
        if created_notification:
            resp["notification"] = "created"
            
        return jsonify(resp), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR en update_appointment: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# ////// get a /appointments con id
@api.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment_query = Appointment.query.filter_by(id=appointment_id).first()
    if appointment_query:
        response_body = {
            "msg": "Resultado exitoso",
            "result": appointment_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No existe"
        }
        return jsonify(response_body), 404

#/// delete a /appointments con id
@api.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404
    
    comments = Comment.query.filter_by(appointment_id=appointment_id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(appointment)
    db.session.commit()

    return jsonify({"msg": "Cita cancelada exitosamente"}), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /appointments
@api.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments_query = Appointment.query.all()
    
    appointments_list = []
    for appointment in appointments_query:
        appointment_data = appointment.serialize()
        
        user = User.query.get(appointment.user_id)
        car = Car.query.get(appointment.car_id)
        service = Service.query.get(appointment.service_id)
        
        # Obtener comentarios asociados a la cita
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        comments_data = [comment.serialize() for comment in comments]

        # Agregar los datos adicionales a appointment_data
        appointment_data['user'] = user.serialize() if user else None
        appointment_data['car'] = car.serialize() if car else None
        appointment_data['service'] = service.serialize() if service else None
        appointment_data['comments'] = comments_data 

        appointments_list.append(appointment_data)
    
    return jsonify(appointments_list), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// get a /appointmentsuser
@api.route('/appointmentsuser/<int:user_id>', methods=['GET'])
@jwt_required()
def get_appointmentsuser(user_id):
    appointments_query  = Appointment.query.filter_by(user_id=user_id).all()

    if not appointments_query:
        return jsonify({"error": "No appointments found for this user"}), 404
    
    appointments_list = []
    for appointment in appointments_query:
        appointment_data = appointment.serialize()
        
        user = User.query.get(appointment.user_id)
        car = Car.query.get(appointment.car_id)
        service = Service.query.get(appointment.service_id)
        
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        comments_data = [comment.serialize() for comment in comments]

        appointment_data['user'] = user.serialize() if user else None
        appointment_data['car'] = car.serialize() if car else None
        appointment_data['service'] = service.serialize() if service else None
        appointment_data['comments'] = comments_data 

        appointments_list.append(appointment_data)
    
    return jsonify(appointments_list), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// GET a /cars/count
@api.route('/totalcount', methods=['GET'])
@jwt_required()
def total_count():
    total_appointments = Appointment.query.count()
    total_clients = User.query.filter_by(role_id=3).count()
    total_services = Service.query.count()
    total_cars = Car.query.count()
    return jsonify({'total_clients': total_clients, 'total_appointments': total_appointments, 'total_cars': total_cars, 'total_services': total_services}), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /slots-taken
@api.route('/slots-taken', methods=['GET'])
def get_slots_taken():
    now = datetime.now()
    end_date = now + timedelta(days=30) 

    appointments = Appointment.query.filter(
        Appointment.date >= now,
        Appointment.date <= end_date
    ).all()

    slots = [
        {
            'date': app.date.strftime('%Y-%m-%d'),
            'start_time': app.date.strftime('%H:%M:%S'),
            'end_time': (app.date + timedelta(hours=1)).strftime('%H:%M:%S'),
        } for app in appointments
    ]

    return jsonify(slots), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// PATCH a /update_profile
@api.route('/update_profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    user = User.query.get(user_id)
    
    if not user or not bcrypt.check_password_hash(user.password, current_password):
        return jsonify({"error": "Invalid current password"}), 401

    if name:
        user.name = name
    if email:
        user.email = email
    if phone_number:
        user.phone_number = phone_number
    if new_password:
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    db.session.commit()
    return jsonify({"msg": "Profile updated successfully", "email": user.email}), 200

# ================================ RUTAS ECONÓMICAS ================================

# ///////////////////////////////////////////////////////////////////////////////////////////// POST /incomes
@api.route('/incomes', methods=['POST'])
@jwt_required()
def create_income():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    amount = data.get('amount')
    description = data.get('description')
    client_name = data.get('client_name')
    car_license_plate = data.get('car_license_plate')
    appointment_id = data.get('appointment_id')
    date = data.get('date')
    
    if not amount or not description:
        return jsonify({"error": "Amount and description are required"}), 400
    
    user_id = get_jwt_identity()
    
    # Si se proporciona una fecha específica, usarla; sino usar la fecha actual
    if date:
        try:
            income_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    else:
        income_date = datetime.utcnow()
    
    new_income = Income(
        amount=amount,
        description=description,
        client_name=client_name,
        car_license_plate=car_license_plate,
        appointment_id=appointment_id,
        date=income_date,
        created_by=user_id
    )
    
    db.session.add(new_income)
    db.session.commit()
    
    return jsonify(new_income.serialize()), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /incomes
@api.route('/incomes', methods=['GET'])
@jwt_required()
def get_incomes():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    # Filtros opcionales
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Income.query
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Income.date >= start_dt)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Income.date <= end_dt)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
    
    incomes = query.order_by(Income.date.desc()).all()
    return jsonify([income.serialize() for income in incomes]), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// POST /expenses
@api.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    amount = data.get('amount')
    description = data.get('description')
    category = data.get('category')
    date = data.get('date')
    
    if not amount or not description or not category:
        return jsonify({"error": "Amount, description and category are required"}), 400
    
    user_id = get_jwt_identity()
    
    # Si se proporciona una fecha específica, usarla; sino usar la fecha actual
    if date:
        try:
            expense_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    else:
        expense_date = datetime.utcnow()
    
    new_expense = Expense(
        amount=amount,
        description=description,
        category=category,
        date=expense_date,
        created_by=user_id
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify(new_expense.serialize()), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /expenses
@api.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    # Filtros opcionales
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    query = Expense.query
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Expense.date >= start_dt)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Expense.date <= end_dt)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
    
    if category:
        query = query.filter(Expense.category == category)
    
    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify([expense.serialize() for expense in expenses]), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /financial-balance
@api.route('/financial-balance', methods=['GET'])
@jwt_required()
def get_financial_balance():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    # Filtros de fecha
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Calcular ingresos
    income_query = Income.query
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        income_query = income_query.filter(Income.date >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        income_query = income_query.filter(Income.date <= end_dt)
    
    total_income = db.session.query(db.func.sum(Income.amount)).filter(
        Income.id.in_([i.id for i in income_query.all()])
    ).scalar() or 0
    
    # Calcular egresos
    expense_query = Expense.query
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        expense_query = expense_query.filter(Expense.date >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        expense_query = expense_query.filter(Expense.date <= end_dt)
    
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.id.in_([e.id for e in expense_query.all()])
    ).scalar() or 0
    
    balance = total_income - total_expense
    
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'period': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// POST /financial-goals
@api.route('/financial-goals', methods=['POST'])
@jwt_required()
def create_financial_goal():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    title = data.get('title')
    description = data.get('description')
    target_amount = data.get('target_amount')
    target_date = data.get('target_date')
    
    if not title or not target_amount:
        return jsonify({"error": "Title and target amount are required"}), 400
    
    user_id = get_jwt_identity()
    
    # Procesar fecha objetivo si se proporciona
    goal_target_date = None
    if target_date:
        try:
            goal_target_date = datetime.strptime(target_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid target_date format. Use YYYY-MM-DD"}), 400
    
    new_goal = FinancialGoal(
        title=title,
        description=description,
        target_amount=target_amount,
        target_date=goal_target_date,
        created_by=user_id
    )
    
    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify(new_goal.serialize()), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /financial-goals
@api.route('/financial-goals', methods=['GET'])
@jwt_required()
def get_financial_goals():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    goals = FinancialGoal.query.filter_by(is_active=True).order_by(FinancialGoal.created_at.desc()).all()
    return jsonify([goal.serialize() for goal in goals]), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// PATCH /financial-goals/<id>
@api.route('/financial-goals/<int:goal_id>', methods=['PATCH'])
@jwt_required()
def update_financial_goal(goal_id):
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    goal = FinancialGoal.query.get(goal_id)
    if not goal:
        return jsonify({"error": "Goal not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Actualizar campos si se proporcionan
    if 'title' in data:
        goal.title = data['title']
    if 'description' in data:
        goal.description = data['description']
    if 'target_amount' in data:
        goal.target_amount = data['target_amount']
    if 'current_amount' in data:
        goal.current_amount = data['current_amount']
    if 'target_date' in data:
        if data['target_date']:
            try:
                goal.target_date = datetime.strptime(data['target_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Invalid target_date format. Use YYYY-MM-DD"}), 400
        else:
            goal.target_date = None
    if 'is_active' in data:
        goal.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(goal.serialize()), 200

# // GET /financial-summary
@api.route('/financial-summary', methods=['GET'])
@jwt_required()
def get_financial_summary():
    # Verificar que sea admin
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied. Admin role required"}), 403
    
    # Resumen del mes actual
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Ingresos del mes
    monthly_income = db.session.query(db.func.sum(Income.amount)).filter(
        Income.date >= start_of_month
    ).scalar() or 0
    
    # Egresos del mes
    monthly_expense = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.date >= start_of_month
    ).scalar() or 0
    
    # Balance del mes
    monthly_balance = monthly_income - monthly_expense
    
    # Metas activas
    active_goals = FinancialGoal.query.filter_by(is_active=True).all()
    
    return jsonify({
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_balance': monthly_balance,
        'active_goals': [goal.serialize() for goal in active_goals],
        'current_month': now.strftime('%Y-%m')
    }), 200

# // post en /appointments/<id>/complete
@api.route('/appointments/<int:appointment_id>/complete', methods=['PUT'])
@jwt_required()
def complete_appointment(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        appointment.status = "completed"

        # Obtener datos relacionados de forma segura
        car = Car.query.get(appointment.car_id) if appointment.car_id else None
        license_plate = car.license_plate if car else 'N/A'

        # Crear notificación interna para admin (sin 'type')
        try:
            admin_notification = Notification(
                title="Trabajo Completado",
                message=f"El trabajo del vehículo {license_plate} ha sido completado",
                user_id=1,
                appointment_id=appointment.id,
                read=False
            )
            db.session.add(admin_notification)
        except Exception as notif_err:
            print("Error creando notificación en complete_appointment:", str(notif_err))

        db.session.commit()
        return jsonify({"message": "Appointment completed and notification created"}), 200
    except Exception as e:
        db.session.rollback()
        print("Error en complete_appointment:", str(e))
        return jsonify({"error": str(e)}), 500

