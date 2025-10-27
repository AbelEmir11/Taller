from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from api.models import db, Notification, User, Appointment, Car, Service
from datetime import datetime
from api.utils import send_email
import traceback

notifications_bp = Blueprint('notifications', __name__)

# Compatibilidad: exponer ruta con y sin el prefijo "notifications" para el notify
@notifications_bp.route('/notifications/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@notifications_bp.route('/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@jwt_required()
def notify_appointment_complete(appointment_id):
    """
    Crea una notificación interna para el admin cuando un trabajo es completado
    """
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Obtener datos relacionados de forma segura
        car = Car.query.get(appointment.car_id) if appointment.car_id else None
        service = Service.query.get(appointment.service_id) if appointment.service_id else None
        license_plate = car.license_plate if car else 'N/A'
        service_name = service.name if service else 'Servicio'

        # Verificar si ya existe una notificación para este appointment
        existing_notification = Notification.query.filter_by(
            appointment_id=appointment_id
        ).first()
        
        if existing_notification:
            print(f"⚠️ Ya existe notificación para appointment {appointment_id}")
            return jsonify({"message": "Notification already exists"}), 200

        # Crear notificación interna para el admin
        admin_notification = Notification(
            title="🔧 Trabajo Completado",
            message=f"El trabajo del vehículo {license_plate} ({service_name}) ha sido completado y está listo para ser retirado.",
            user_id=16,  # Admin
            appointment_id=appointment_id,
            read=False
        )
        db.session.add(admin_notification)
        db.session.commit()
        
        print(f"✅ Notificación creada exitosamente para appointment {appointment_id}")
        return jsonify({
            "message": "Internal notification created successfully",
            "notification_id": admin_notification.id
        }), 200

    except Exception as e:
        print("❌ Error en notify_appointment_complete:", str(e))
        print(traceback.format_exc())
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Exponer POST /api/notifications/<id>/send_email (frontend lo llama así)
@notifications_bp.route('/notifications/<int:notification_id>/send_email', methods=['POST'])
@notifications_bp.route('/<int:notification_id>/send_email', methods=['POST'])  # alias antiguo
@jwt_required()
def send_email_from_notification(notification_id):
    """
    Envía un email al cliente desde una notificación (solo admin)
    """
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Acceso denegado. Solo administradores."}), 403

    try:
        # Obtener la notificación
        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({"error": "Notificación no encontrada"}), 404

        if not notification.appointment_id:
            return jsonify({"error": "No hay turno asociado a esta notificación"}), 400

        # Obtener el appointment
        appointment = Appointment.query.get(notification.appointment_id)
        if not appointment:
            return jsonify({"error": "Turno no encontrado"}), 404

        # Obtener el cliente
        client = User.query.get(appointment.user_id)
        if not client or not client.email:
            return jsonify({"error": "Email del cliente no disponible"}), 400

        # Obtener datos del vehículo y servicio
        car = Car.query.get(appointment.car_id) if appointment.car_id else None
        service = Service.query.get(appointment.service_id) if appointment.service_id else None
        license_plate = car.license_plate if car else 'N/A'
        car_model = car.car_model if car else 'Vehículo'
        service_name = service.name if service else 'Servicio'

        # Preparar el email
        subject = "✅ Su vehículo está listo para ser retirado"
        body = f"""
Estimado/a {client.name},

Le informamos que su vehículo ya está listo para ser retirado.

📋 Detalles del servicio:
   • Vehículo: {car_model}
   • Patente: {license_plate}
   • Servicio realizado: {service_name}
   • Fecha de finalización: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Puede pasar a retirarlo en nuestro horario de atención.

¡Gracias por confiar en nosotros!

Saludos cordiales,
El equipo de AutoAgenda
        """

        # Intentar enviar el email
        print(f"📧 Intentando enviar email a {client.email}...")
        # Ahora send_email lanzará excepción con detalle si falla
        send_email(client.email, subject, body)

        # Marcar la notificación como leída y guardar confirmación
        notification.read = True
        email_confirmation = Notification(
            title="📧 Email enviado",
            message=f"Correo enviado exitosamente a {client.email} ({client.name}) sobre el vehículo {license_plate}.",
            user_id=16,
            appointment_id=appointment.id,
            read=True
        )
        db.session.add(email_confirmation)
        db.session.commit()

        print(f"✅ Email enviado exitosamente a {client.email}")
        return jsonify({
            "message": "Email sent successfully",
            "email": client.email,
            "client_name": client.name
        }), 200

    except Exception as e:
        db.session.rollback()
        print("❌ Error inesperado en send_email_from_notification:", str(e))
        print(traceback.format_exc())
        # Devolver detalle (el mensaje viene de send_email al lanzar)
        return jsonify({"error": str(e)}), 502


# Exponer GET /api/notifications para que el frontend admin lo consuma correctamente
@notifications_bp.route('/notifications', methods=['GET'])
@notifications_bp.route('', methods=['GET'])  # alias: raiz del blueprint también responde
@jwt_required()
def get_notifications():
    """
    Obtener todas las notificaciones (solo admin)
    """
    try:
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Acceso denegado"}), 403

        # Obtener notificaciones ordenadas por fecha (más recientes primero)
        notifications = Notification.query.order_by(
            Notification.read.asc(),  # No leídas primero
            Notification.created_at.desc()
        ).all()
        
        return jsonify([notif.serialize() for notif in notifications]), 200
        
    except Exception as e:
        print("❌ Error en get_notifications:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


# Marcar notificación como leída
@notifications_bp.route('/notifications/<int:notification_id>/mark_read', methods=['PATCH'])
@notifications_bp.route('/<int:notification_id>/mark_read', methods=['PATCH'])  # alias antiguo
@jwt_required()
def mark_notification_read(notification_id):
    """
    Marcar una notificación como leída
    """
    try:
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Acceso denegado"}), 403

        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({"error": "Notificación no encontrada"}), 404

        notification.read = True
        db.session.commit()

        return jsonify({
            "message": "Notification marked as read",
            "notification": notification.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        print("❌ Error en mark_notification_read:", str(e))
        return jsonify({"error": str(e)}), 500