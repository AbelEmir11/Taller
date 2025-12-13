"""
Servicio de email usando Resend API
Implementación profesional para envío de correos del taller mecánico
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
    print("⚠️ Warning: resend module not installed. Email functionality will be limited.")


def send_email_resend(to_email, subject, body=None, html=None):
    """
    Envía un email usando el servicio Resend
    
    Args:
        to_email (str): Email del destinatario
        subject (str): Asunto del email
        body (str, optional): Contenido en texto plano
        html (str, optional): Contenido en HTML (tiene prioridad sobre body)
    
    Returns:
        dict: Respuesta de Resend con el ID del email enviado
        
    Raises:
        Exception: Si falla el envío del email
    """
    try:
        # Verificar que resend esté disponible
        if not RESEND_AVAILABLE:
            raise Exception("Resend module is not installed. Please run: pip install resend")
        
        # Obtener API key del entorno
        api_key = os.getenv('RESEND_API_KEY')
        if not api_key:
            raise Exception("RESEND_API_KEY no está configurada en las variables de entorno")
        
        # Obtener email del remitente
        sender_email = os.getenv('MAIL_DEFAULT_SENDER', 'onboarding@resend.dev')
        
        # Configurar API key de Resend
        resend.api_key = api_key
        
        # Preparar parámetros del email
        params = {
            "from": f"AutoAgenda <{sender_email}>",
            "to": [to_email],
            "subject": subject,
        }
        
        # Agregar contenido (priorizar HTML sobre texto plano)
        if html:
            params["html"] = html
        elif body:
            params["html"] = f"<p>{body}</p>"
        else:
            raise Exception("Debe proporcionar 'body' o 'html' para el email")
        
        # Enviar email
        print(f"📧 Enviando email a {to_email} con asunto: '{subject}'")
        email = resend.Emails.send(params)
        
        print(f"✅ Email enviado exitosamente. ID: {email.get('id', 'N/A')}")
        return email
        
    except Exception as e:
        error_msg = f"Error al enviar email a {to_email}: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        raise Exception(error_msg)


def send_vehicle_ready_email(client_email, client_name, car_model, license_plate, service_name):
    """
    Envía notificación de que el vehículo está listo para retiro
    
    Args:
        client_email (str): Email del cliente
        client_name (str): Nombre del cliente
        car_model (str): Modelo del vehículo
        license_plate (str): Patente del vehículo
        service_name (str): Nombre del servicio realizado
        
    Returns:
        dict: Respuesta de Resend
    """
    from .email_templates import get_vehicle_ready_template
    
    subject = "✅ Su vehículo está listo para ser retirado"
    html_content = get_vehicle_ready_template(
        client_name=client_name,
        car_model=car_model,
        license_plate=license_plate,
        service_name=service_name
    )
    
    return send_email_resend(
        to_email=client_email,
        subject=subject,
        html=html_content
    )


def send_appointment_confirmation_email(client_email, client_name, car_model, license_plate, service_name, appointment_date):
    """
    Envía confirmación de cita agendada
    
    Args:
        client_email (str): Email del cliente
        client_name (str): Nombre del cliente
        car_model (str): Modelo del vehículo
        license_plate (str): Patente del vehículo
        service_name (str): Nombre del servicio
        appointment_date (str): Fecha y hora de la cita
        
    Returns:
        dict: Respuesta de Resend
    """
    from .email_templates import get_appointment_confirmation_template
    
    subject = "📅 Confirmación de tu cita - AutoAgenda"
    html_content = get_appointment_confirmation_template(
        client_name=client_name,
        car_model=car_model,
        license_plate=license_plate,
        service_name=service_name,
        appointment_date=appointment_date
    )
    
    return send_email_resend(
        to_email=client_email,
        subject=subject,
        html=html_content
    )
