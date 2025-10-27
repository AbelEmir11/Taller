import traceback
import threading
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


def send_async_email(app, msg):
    """Función que realmente envía el correo (en un hilo separado)."""
    try:
        with app.app_context():
            mail_ext = app.extensions.get('mail')
            if mail_ext:
                mail_ext.send(msg)
                print(f"✅ Email enviado correctamente a {msg.recipients[0]} via Flask-Mail")
    except Exception as e:
        print("❌ Error en hilo de envío de email:", str(e))
        print(traceback.format_exc())

def send_email(to_email, subject, body):
    """Envío de correo asíncrono (usa Flask-Mail o fallback SMTP)."""
    try:
        app = current_app._get_current_object()

        # Verificar si Flask-Mail está configurado
        mail_ext = current_app.extensions.get('mail')
        if mail_ext:
            msg = Message(
                subject=subject,
                recipients=[to_email],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            print(f"📧 Intentando enviar email a {to_email} en segundo plano...")
            threading.Thread(target=send_async_email, args=(app, msg)).start()
            return True

        # Fallback a smtplib si Flask-Mail no está disponible
        print("ℹ️ Flask-Mail no inicializado, intentando fallback SMTP (segundo plano)...")

        smtp_server = current_app.config.get('MAIL_SERVER') or os.getenv('MAIL_SERVER')
        smtp_port = int(current_app.config.get('MAIL_PORT') or os.getenv('MAIL_PORT', 587))
        username = current_app.config.get('MAIL_USERNAME') or os.getenv('MAIL_USERNAME')
        password = current_app.config.get('MAIL_PASSWORD') or os.getenv('MAIL_PASSWORD')
        use_tls = current_app.config.get('MAIL_USE_TLS', True)
        sender = current_app.config.get('MAIL_DEFAULT_SENDER') or os.getenv('MAIL_DEFAULT_SENDER')

        if not smtp_server or not username or not password:
            raise Exception("SMTP configuration incomplete (MAIL_SERVER/MAIL_USERNAME/MAIL_PASSWORD)")

        def send_with_smtp():
            try:
                context = ssl.create_default_context()
                if use_tls:
                    server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
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
            except Exception as e:
                print("❌ Error enviando email (SMTP):", str(e))
                print(traceback.format_exc())

        # Iniciar hilo separado
        threading.Thread(target=send_with_smtp).start()
        return True

    except Exception as e:
        print("❌ Error general en send_email:", str(e))
        print(traceback.format_exc())
        raise Exception(f"Error sending email: {str(e)}")