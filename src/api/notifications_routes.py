from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from api.models import db, Notification, User, Appointment
from datetime import datetime
from api.utils import send_email  # ya lo estás usando

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notify_appointment_complete/<int:appointment_id>', methods=['POST'])
@jwt_required()
def notify_appointment_complete(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        # 📌 1. Crear notificación interna
        admin_notification = Notification(
            title="Trabajo Completado",
            message=f"El trabajo del vehículo {appointment.car.license_plate} ha sido completado",
            user_id=1,  # ID del admin
            appointment_id=appointment_id,
            type="internal"
        )
        db.session.add(admin_notification)

        # 📩 2. Enviar notificación externa (correo)
        client = User.query.get(appointment.user_id)
        if client and client.email:
            subject = "Su vehículo está listo"
            body = f"""
            Estimado/a {client.name},

            Le informamos que su vehículo {appointment.car.license_plate} está listo para ser retirado.
            
            Servicio realizado: {appointment.service.name}
            Fecha de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M')}

            Saludos cordiales,
            El equipo del taller
            """
            send_email(client.email, subject, body)

            # Guardamos también esta notificación en la base
            email_notification = Notification(
                title="Correo enviado al cliente",
                message=f"Correo enviado a {client.email} sobre el trabajo completado.",
                user_id=1,
                appointment_id=appointment_id,
                type="email"
            )
            db.session.add(email_notification)

        db.session.commit()
        return jsonify({"message": "Appointment completed and notifications sent"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 📬 Obtener todas las notificaciones (solo admin)
@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    payload = get_jwt()
    if payload.get("role_id") != 1:
        return jsonify({"error": "Access denied"}), 403

    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    return jsonify([notif.serialize() for notif in notifications]), 200
