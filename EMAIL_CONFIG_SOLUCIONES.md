# Configuración de Resend para Emails

## ❌ Error Actual en Producción

```
Error: The gmail.com domain is not verified. 
Please, add and verify your domain on https://resend.com/domains
```

## 📧 ¿Por qué falla?

Resend NO permite enviar emails desde dominios gratuitos como `@gmail.com`, `@hotmail.com`, etc. 
**Debes usar tu propio dominio verificado**.

## ✅ Solución 1: Usar Dominio Propio (Recomendado)

### Pasos:

1. **Ve a https://resend.com/domains**
2. **Agrega tu dominio** (ej: `autoagenda.com`, `tudominio.com`)
3. **Verifica el dominio** siguiendo las instrucciones (agregar registros DNS)
4. **Una vez verificado**, actualiza en Render:
   ```
   MAIL_DEFAULT_SENDER=noreply@tudominio.com
   ```

## ✅ Solución 2: Usar Dominio de Prueba de Resend (Temporal)

Para **PRUEBAS**, Resend proporciona un dominio temporal:

```bash
MAIL_DEFAULT_SENDER=onboarding@resend.dev
```

> ⚠️ **IMPORTANTE**: Este dominio solo sirve para pruebas, los emails pueden ir a spam.

## ✅ Solución 3: Usar Flask-Mail con Gmail (Ya tienes instalado)

Si NO quieres usar Resend, puedes usar Flask-Mail con un App Password de Gmail:

### En Render, configura:

```bash
# Elimina estas (si las tienes):
# RESEND_API_KEY
# Agrega estas:
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # App Password de 16 caracteres
MAIL_DEFAULT_SENDER=tu_email@gmail.com
```

### Cómo obtener App Password de Gmail:

1. Ve a https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Busca "Contraseñas de aplicaciones"
4. Genera una para "Mail"
5. Usa esa contraseña de 16 caracteres

---

## 🔧 Error en Local: "Error de red al cargar notificaciones"

Esto es porque el backend Flask no está corriendo o hay un problema de CORS.

**Asegúrate de que:**
1. Backend Flask esté corriendo en `http://localhost:5000`
2. Verifica el archivo `.env` tenga: `BACKEND_URL=http://localhost:5000`

---

## 📝 Recomendación Final

Para producción, la mejor opción es:
- Usar tu propio dominio verificado en Resend, O
- Usar Flask-Mail con Gmail App Password (más fácil de configurar)
