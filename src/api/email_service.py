"""
Servicio de email usando Flask-Mail (fallback con Resend)
Prioriza Flask-Mail para dominios gratuitos como Gmail
"""

import os
from flask import current_app
import traceback

# Importar resend solo si está disponible
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    print("⚠️ Warning: resend module not installed. Email functionality will use Flask-Mail.")


def send_vehicle_ready_email(client_email, client_name, car_model, license_plate, service_name):
    """
    Envía email de vehículo listo usando Flask-Mail
    """
    from api.email_templates import get_vehicle_ready_template
    from flask_mail import Message
    
    try:
        print(f"📧 Enviando email a {client_email} usando Flask-Mail...")
        
        # Verificar que Flask-Mail esté configurado
        if 'mail' not in current_app.extensions:
            raise Exception("Flask-Mail no está configurado. Verifique las variables MAIL_* en Render.")
        
        mail = current_app.extensions['mail']
        sender = os.getenv('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_DEFAULT_SENDER'))
        
        # Generar HTML del email
        html = get_vehicle_ready_template(
            client_name=client_name,
            car_model=car_model,
            license_plate=license_plate,
            service_name=service_name
        )
        
        # Crear mensaje
        msg = Message(
            subject="✅ Su vehículo está listo para ser retirado",
            recipients=[client_email],
            html=html,
            sender=sender
        )
        
        # Enviar
        mail.send(msg)
        print(f"✅ Email enviado exitosamente via Flask-Mail/Gmail a {client_email}")
        return True
        
    except Exception as e:
        error_msg = f"Error al enviar email a {client_email}: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        raise Exception(error_msg)


def send_appointment_confirmation_email(client_email, client_name, appointment_date, service_name, car_model):
    """
    Envía email de confirmación de cita usando Flask-Mail
    """
    from api.email_templates import get_appointment_confirmation_template
    from flask_mail import Message
    
    try:
        print(f"📧 Enviando confirmación de cita a {client_email}...")
        
        if 'mail' not in current_app.extensions:
            raise Exception("Flask-Mail no está configurado.")
        
        mail = current_app.extensions['mail']
        sender = os.getenv('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_DEFAULT_SENDER'))
        
        html = get_appointment_confirmation_template(
            client_name=client_name,
            appointment_date=appointment_date,
            service_name=service_name,
            car_model=car_model
        )
        
        msg = Message(
            subject="✅ Confirmación de cita - AutoAgenda",
            recipients=[client_email],
            html=html,
            sender=sender
        )
        
        mail.send(msg)
        print(f"✅ Email de confirmación enviado a {client_email}")
        return True
        
    except Exception as e:
        error_msg = f"Error al enviar confirmación a {client_email}: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        raise Exception(error_msg)
