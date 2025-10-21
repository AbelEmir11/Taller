from flask import Blueprint, request, jsonify
import mercadopago
import os

mp_bp = Blueprint("mercadopago", __name__)

# ⚙️ Configura tu Access Token (usá uno de TEST por ahora)
ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "APP_USR-7860258061483961-102110-0ccc168f4a4ee59694f256329f5e205c-2938262754" )

sdk = mercadopago.SDK(ACCESS_TOKEN)


@mp_bp.route("/create_preference", methods=["POST"])
def create_preference():
    try:
        data = request.get_json()

        # Ejemplo: productos enviados desde el frontend
        # data = {
        #   "items": [
        #       {"title": "Cambio de aceite", "quantity": 1, "unit_price": 15000},
        #       {"title": "Filtro de aire", "quantity": 1, "unit_price": 8000}
        #   ],
        #   "client_email": "cliente@ejemplo.com"
        # }

        preference_data = {
            "items": data["items"],
            "payer": {
                "email": data.get("client_email", "cliente@ejemplo.com")
            },
            "back_urls": {
                "success": "http://localhost:5000/front/success.html",
                "failure": "http://localhost:5000/front/failure.html",
                "pending": "http://localhost:5000/front/pending.html"
            },
            "auto_return": "approved",
            "notification_url": "http://localhost:5000/api/mercadopago/webhook"  # 👈 para recibir notificaciones
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return jsonify({
            "id": preference["id"],
            "init_point": preference["init_point"]  # URL para redirigir al Checkout
        })

    except Exception as e:
        print(f"Error creando preferencia: {e}")
        return jsonify({"error": str(e)}), 500


# 📬 Endpoint para recibir notificaciones de Mercado Pago
@mp_bp.route("/webhook", methods=["POST"])
def webhook():
    try:
        notification = request.get_json()
        print("📩 Notificación de Mercado Pago recibida:", notification)
        # Podés guardar esta info en tu base de datos si querés
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Error procesando webhook:", e)
        return jsonify({"error": str(e)}), 500
