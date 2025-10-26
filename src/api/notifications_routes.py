from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from api.models import db, Notification, User, Appointment, Car, Service
from datetime import datetime
from api.utils import send_email  # ya lo estás usando
import traceback

notifications_bp = Blueprint('notifications', __name__)

# Añadir alias con prefijo "notifications" para compatibilidad con frontend antiguo
@notifications_bp.route('/notifications/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@notifications_bp.route('/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@jwt_required()
def notify_appointment_complete(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Obtener datos relacionados de forma segura
        car = Car.query.get(appointment.car_id) if appointment.car_id else None
        service = Service.query.get(appointment.service_id) if appointment.service_id else None
        license_plate = car.license_plate if car else 'N/A'

        # Verificar si ya existe una notificación para este appointment
        existing_notification = Notification.query.filter_by(
            appointment_id=appointment_id,
            type='internal'
        ).first()
        
        if existing_notification:
            return jsonify({"message": "Notification already exists"}), 200

        admin_notification = Notification(
            title="Trabajo Completado",
            message=f"El trabajo del vehículo {license_plate} ha sido completado",
            user_id=1,
            appointment_id=appointment_id,
            type="internal",
            read=False
        )
        db.session.add(admin_notification)
        db.session.commit()
        return jsonify({"message": "Internal notification created"}), 200

    except Exception as e:
        print("Error en notify_appointment_complete:", str(e))
        print(traceback.format_exc())
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Nuevo endpoint: el admin puede enviar el email al cliente desde la notificación
@notifications_bp.route('/notifications/<int:notification_id>/send_email', methods=['POST'])
@jwt_required()
def send_email_from_notification(notification_id):
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Acceso denegado"}), 403

    try:
        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({"error": "Notificación no encontrada"}), 404

        if not notification.appointment_id:
            return jsonify({"error": "No hay turno asociado a esta notificación"}), 400

        appointment = Appointment.query.get(notification.appointment_id)
        if not appointment:
            return jsonify({"error": "Turno no encontrado"}), 404

        client = User.query.get(appointment.user_id)
        if not client or not client.email:
            return jsonify({"error": "Email del cliente no disponible"}), 400

        # Obtener car y service de forma segura
        car = Car.query.get(appointment.car_id) if appointment.car_id else None
        service = Service.query.get(appointment.service_id) if appointment.service_id else None
        license_plate = car.license_plate if car else 'N/A'
        service_name = service.name if service else 'Servicio'

        subject = "Su vehículo está listo"
        body = f"""
        Estimado/a {client.name},

        Le informamos que su vehículo {license_plate} está listo para ser retirado.
        
        Servicio realizado: {service_name}
        Fecha de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        Saludos cordiales,
        El equipo del taller
        """

        # Intentar enviar el email
        try:
            sent = send_email(client.email, subject, body)
            if not sent:
                return jsonify({"error": "Failed to send email", "details": "Mail service returned failure"}), 502
        except Exception as send_err:
            print("Error sending email via send_email():", str(send_err))
            return jsonify({"error": "Failed to send email", "details": str(send_err)}), 502

        # Guardar notificación de tipo email en la base
        email_notification = Notification(
            title="Correo enviado al cliente",
            message=f"Correo enviado a {client.email} sobre el trabajo completado.",
            user_id=1,
            appointment_id=appointment.id,
            type="email"
        )
        db.session.add(email_notification)

        # Marcar la notificación original como leída si existe el campo
        try:
            if hasattr(notification, 'read'):
                notification.read = True
        except:
            pass

        db.session.commit()
        return jsonify({"message": "Email sent to client and notification stored", "email": client.email}), 200

    except Exception as e:
        db.session.rollback()
        print("Unexpected error in send_email_from_notification:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# 📬 Obtener todas las notificaciones (solo admin)
@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Access denied"}), 403

        notifications = Notification.query.order_by(Notification.created_at.desc()).all()
        return jsonify([notif.serialize() for notif in notifications]), 200
    except Exception as e:
        print("Error en get_notifications:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500
