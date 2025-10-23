from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from api.models import db, Notification, User, Appointment
from datetime import datetime
import traceback
from api.utils import send_email  # ya lo estás usando

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@jwt_required()
def notify_appointment_complete(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # Verificar si ya existe una notificación para este appointment
        existing_notification = Notification.query.filter_by(
            appointment_id=appointment_id,
            type='internal'
        ).first()
        
        if existing_notification:
            return jsonify({"message": "Notification already exists"}), 200

        admin_notification = Notification(
            title="Trabajo Completado",
            message=f"El trabajo del vehículo {appointment.car.license_plate if appointment.car else 'N/A'} ha sido completado",
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

        subject = "Su vehículo está listo"
        body = f"""
        Estimado/a {client.name},

        Le informamos que su vehículo {appointment.car.license_plate} está listo para ser retirado.
        
        Servicio realizado: {appointment.service.name if appointment.service else 'Servicio'}
        Fecha de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        Saludos cordiales,
        El equipo del taller
        """

        # Intentar enviar el email
        email_sent = send_email(client.email, subject, body)
        if not email_sent:
            return jsonify({
                "error": "No se pudo enviar el email",
                "details": "Error en el servicio de email"
            }), 502

        # Si el email se envió correctamente, guardar la notificación
        email_notification = Notification(
            title="Correo enviado al cliente",
            message=f"Correo enviado a {client.email} sobre el trabajo completado.",
            user_id=1,
            appointment_id=appointment.id,
            type="email"
        )
        db.session.add(email_notification)

        # Marcar la notificación original como leída
        notification.read = True
        
        db.session.commit()
        return jsonify({
            "message": "Email enviado y notificación guardada",
            "email": client.email
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error en send_email_from_notification: {str(e)}")
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
        print(traceback.format_exc())  # Imprimir stack trace completo
        return jsonify({"error": "Internal server error"}), 500
