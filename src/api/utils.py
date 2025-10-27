import traceback
from flask import jsonify, url_for, current_app
import os
import smtplib
from flask_mail import Message
from flask import current_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/full-stack" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

def send_email(to_email, subject, body):
    try:
        # Intentar usar la extensión Flask-Mail si está inicializada
        mail_ext = current_app.extensions.get('mail')
        if mail_ext:
            try:
                msg = Message(
                    subject=subject,
                    recipients=[to_email],
                    body=body,
                    sender=current_app.config.get('MAIL_DEFAULT_SENDER')
                )
                mail_ext.send(msg)
                print(f"✅ Email enviado correctamente a {to_email} via Flask-Mail")
                return True
            except Exception as e:
                # Si falla Flask-Mail, mostrar detalle y luego intentar fallback SMTP
                print("❌ Flask-Mail error:", str(e))
                print(traceback.format_exc())
                # No retornar False: intentar fallback
        else:
            print("ℹ️ Flask-Mail no inicializado, intentando fallback SMTP")

        # Fallback a smtplib con configuración desde app.config / environment
        smtp_server = current_app.config.get('MAIL_SERVER') or os.getenv('MAIL_SERVER')
        smtp_port = int(current_app.config.get('MAIL_PORT') or os.getenv('MAIL_PORT', 587))
        username = current_app.config.get('MAIL_USERNAME') or os.getenv('MAIL_USERNAME')
        password = current_app.config.get('MAIL_PASSWORD') or os.getenv('MAIL_PASSWORD')
        use_tls = current_app.config.get('MAIL_USE_TLS', True)
        sender = current_app.config.get('MAIL_DEFAULT_SENDER') or os.getenv('MAIL_DEFAULT_SENDER')

        if not smtp_server or not username or not password:
            raise Exception("SMTP configuration incomplete (MAIL_SERVER/MAIL_USERNAME/MAIL_PASSWORD)")

        context = ssl.create_default_context()
        if use_tls:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
            server.ehlo()
            server.starttls(context=context)
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context, timeout=15)

        server.login(username, password)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server.sendmail(sender, [to_email], msg.as_string())
        server.quit()
        print(f"✅ Email enviado correctamente a {to_email} via smtplib ({smtp_server}:{smtp_port})")
        return True

    except Exception as e:
        # Devolver información detallada para logs y para que el endpoint la incluya en la respuesta
        err_msg = f"Error sending email: {str(e)}"
        print("❌", err_msg)
        print(traceback.format_exc())
        # Lanzar excepción para que el controlador la capture y devuelva 502 con detalles
        raise Exception(err_msg)