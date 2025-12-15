"""
Servicio de email usando Flask-Mail con envío asíncrono
Optimizado para entornos con memoria limitada como Render
"""

import os
import threading
from flask import current_app
import traceback


def send_async_email(app, msg):
    """
    Función auxiliar para enviar emails en segundo plano
    """
    try:
        with app.app_context():
            mail = app.extensions['mail']
            mail.send(msg)
            print(f"✅ Email enviado exitosamente")
    except Exception as e:
        print(f"❌ Error enviando email en thread: {str(e)}")
        print(traceback.format_exc())


def send_vehicle_ready_email(client_email, client_name, car_model, license_plate, service_name):
    """
    Envía email de vehículo listo de forma asíncrona
    """
    from flask_mail import Message
    
    try:
        print(f"📧 Preparando email para {client_email}...")
        
        # Verificar Flask-Mail
        if 'mail' not in current_app.extensions:
            raise Exception("Flask-Mail no está configurado.")
        
        sender = os.getenv('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_DEFAULT_SENDER'))
        
        # HTML simplificado para reducir memoria
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #4a5568;">✅ Su vehículo está listo</h2>
                <p>Estimado/a <strong>{client_name}</strong>,</p>
                <p>Le informamos que su vehículo ya está listo para ser retirado.</p>
                <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Vehículo:</strong> {car_model}</p>
                    <p><strong>Patente:</strong> {license_plate}</p>
                    <p><strong>Servicio:</strong> {service_name}</p>
                </div>
                <p>Puede pasar a retirarlo en nuestro horario de atención.</p>
                <p>¡Gracias por confiar en nosotros!</p>
                <p style="color: #718096;">Saludos,<br>El equipo de AutoAgenda</p>
            </body>
        </html>
        """
        
        # Crear mensaje
        msg = Message(
            subject="✅ Su vehículo está listo para ser retirado",
            recipients=[client_email],
            html=html,
            sender=sender
        )
        
        # Enviar en segundo plano usando threading
        app = current_app._get_current_object()
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        
        print(f"📨 Email programado para envío asíncrono a {client_email}")
        return True
        
    except Exception as e:
        error_msg = f"Error preparando email a {client_email}: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        raise Exception(error_msg)


def send_appointment_confirmation_email(client_email, client_name, appointment_date, service_name, car_model):
    """
    Envía email de confirmación de cita de forma asíncrona
    """
    from flask_mail import Message
    
    try:
        print(f"📧 Preparando confirmación de cita para {client_email}...")
        
        if 'mail' not in current_app.extensions:
            raise Exception("Flask-Mail no está configurado.")
        
        sender = os.getenv('MAIL_DEFAULT_SENDER', current_app.config.get('MAIL_DEFAULT_SENDER'))
        
        # HTML simplificado
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #4a5568;">✅ Confirmación de cita</h2>
                <p>Estimado/a <strong>{client_name}</strong>,</p>
                <p>Su cita ha sido confirmada exitosamente.</p>
                <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Fecha:</strong> {appointment_date}</p>
                    <p><strong>Servicio:</strong> {service_name}</p>
                    <p><strong>Vehículo:</strong> {car_model}</p>
                </div>
                <p>Nos vemos pronto!</p>
                <p style="color: #718096;">Saludos,<br>El equipo de AutoAgenda</p>
            </body>
        </html>
        """
        
        msg = Message(
            subject="✅ Confirmación de cita - AutoAgenda",
            recipients=[client_email],
            html=html,
            sender=sender
        )
        
        # Enviar en segundo plano
        app = current_app._get_current_object()
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        
        print(f"📨 Email de confirmación programado para {client_email}")
        return True
        
    except Exception as e:
        error_msg = f"Error preparando confirmación a {client_email}: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        raise Exception(error_msg)
