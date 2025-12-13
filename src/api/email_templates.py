"""
Templates HTML profesionales para emails del taller mecánico
"""

def get_vehicle_ready_template(client_name, car_model, license_plate, service_name):
    """
    Template para notificar que el vehículo está listo para retiro
    """
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vehículo Listo - AutoAgenda</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">
                                    🔧 AutoAgenda
                                </h1>
                                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                                    Tu Taller de Confianza
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="color: #2d3748; margin: 0 0 20px 0; font-size: 24px;">
                                    ✅ ¡Tu vehículo está listo!
                                </h2>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0 0 20px 0;">
                                    Estimado/a <strong>{client_name}</strong>,
                                </p>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0 0 30px 0;">
                                    Nos complace informarte que tu vehículo ha sido reparado exitosamente y está listo para ser retirado.
                                </p>
                                
                                <!-- Vehicle Details Card -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f7fafc; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
                                    <tr>
                                        <td>
                                            <h3 style="color: #2d3748; margin: 0 0 15px 0; font-size: 18px;">
                                                📋 Detalles del Servicio
                                            </h3>
                                            
                                            <table width="100%" cellpadding="8" cellspacing="0">
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px; width: 40%;">
                                                        <strong>Vehículo:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {car_model}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px;">
                                                        <strong>Patente:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {license_plate}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px;">
                                                        <strong>Servicio realizado:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {service_name}
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0 0 10px 0;">
                                    Puedes pasar a retirarlo en nuestro horario de atención.
                                </p>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0;">
                                    ¡Gracias por confiar en nosotros!
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #2d3748; padding: 30px; text-align: center;">
                                <p style="color: #cbd5e0; margin: 0 0 10px 0; font-size: 14px;">
                                    <strong>AutoAgenda - Tu Taller de Confianza</strong>
                                </p>
                                <p style="color: #a0aec0; margin: 0; font-size: 12px;">
                                    Este es un correo automático, por favor no respondas a este mensaje.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def get_appointment_confirmation_template(client_name, car_model, license_plate, service_name, appointment_date):
    """
    Template para confirmar una cita agendada
    """
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmación de Cita - AutoAgenda</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f4f4f4;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">
                                    📅 AutoAgenda
                                </h1>
                                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                                    Tu Taller de Confianza
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="color: #2d3748; margin: 0 0 20px 0; font-size: 24px;">
                                    ✅ Cita Confirmada
                                </h2>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0 0 20px 0;">
                                    Estimado/a <strong>{client_name}</strong>,
                                </p>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0 0 30px 0;">
                                    Tu cita ha sido confirmada exitosamente. A continuación los detalles:
                                </p>
                                
                                <!-- Appointment Details Card -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f7fafc; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
                                    <tr>
                                        <td>
                                            <h3 style="color: #2d3748; margin: 0 0 15px 0; font-size: 18px;">
                                                📋 Detalles de la Cita
                                            </h3>
                                            
                                            <table width="100%" cellpadding="8" cellspacing="0">
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px; width: 40%;">
                                                        <strong>Fecha y hora:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {appointment_date}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px;">
                                                        <strong>Vehículo:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {car_model}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px;">
                                                        <strong>Patente:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {license_plate}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #718096; font-size: 14px;">
                                                        <strong>Servicio:</strong>
                                                    </td>
                                                    <td style="color: #2d3748; font-size: 14px;">
                                                        {service_name}
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 16px; margin: 0;">
                                    Por favor, llega puntualmente para garantizar un servicio óptimo. ¡Te esperamos!
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #2d3748; padding: 30px; text-align: center;">
                                <p style="color: #cbd5e0; margin: 0 0 10px 0; font-size: 14px;">
                                    <strong>AutoAgenda - Tu Taller de Confianza</strong>
                                </p>
                                <p style="color: #a0aec0; margin: 0; font-size: 12px;">
                                    Este es un correo automático, por favor no respondas a este mensaje.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
