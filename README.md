
### Auto Agenda Taller

Auto Agenda Taller es una plataforma web diseñada para facilitar la gestión de citas en talleres automotrices, permitiendo a los clientes y al personal del taller organizar servicios, citas y comunicación de manera eficiente. La plataforma busca optimizar la eficiencia operativa y mejorar la experiencia del cliente.

### Descripción General

El objetivo principal de Auto Agenda Taller es simplificar la forma en que los talleres manejan las citas y los servicios, brindando a los clientes una forma fácil de reservar citas mientras el personal del taller gestiona de manera eficiente el flujo de trabajo. La aplicación está estructurada en tres roles principales: **Administrador**, **Mecánico** y **Cliente**, cada uno con su propio panel de control y funcionalidades específicas.

### Tecnologías Utilizadas

1. Frontend:
   - React.js: Para construir una interfaz de usuario dinámica y responsiva.
   - Bootstrap: Asegura un diseño responsivo y pulido en cualquier dispositivo.

2. Backend:
   - Flask: Microframework en Python que gestiona la lógica del servidor y las interacciones con el cliente.
   - SQLAlchemy: ORM que simplifica las interacciones con la base de datos.
   - Flask-Bcrypt: Garantiza la encriptación segura de las contraseñas.

3. Base de Datos:
   - PostgreSQL: Base de datos relacional utilizada para almacenar información relacionada con usuarios, citas, vehículos y servicios.

4. Seguridad y Autenticación:
   - **JWT (JSON Web Tokens)**: Implementado para la autenticación segura de usuarios, permitiendo el acceso autorizado.
   - **Flask-Bcrypt**: Encripta las contraseñas para proteger los datos sensibles.

5. Integraciones Actuales:
   - Brevo API (anteriormente Sendinblue): Envío de confirmaciones y recordatorios de citas por **email** y **SMS** para una comunicación eficiente con los clientes.

6. Integraciones Futuras:
   - **Google Calendar API**: Para sincronizar automáticamente las citas con los calendarios personales de los usuarios, facilitando la gestión de horarios.

7. Despliegue y Hosting:
   - **Render**: Asegura una disponibilidad continua y escalabilidad automática.
   - **Heroku**: Utilizado como una opción adicional para el despliegue, proporcionando flexibilidad en la gestión de servidores y recursos.

8. **Control de Versiones:**
   - **Git/GitHub**: Herramienta utilizada para el control de versiones y la colaboración, permitiendo un trabajo coordinado entre los miembros del equipo.

---

### Cómo Funciona Cada Sección

#### 1. Cliente (Panel del Cliente)

Los **clientes** pueden:
- **Registrarse y gestionar su perfil**: Crear una cuenta, actualizar información personal y gestionar los vehículos asociados.
- **Reservar citas**: Seleccionar un vehículo, un servicio (cambio de aceite, revisión general) y reservar un horario disponible. Las citas se confirman automáticamente si hay disponibilidad.
- **Historial de citas**: Revisar citas pasadas, servicios realizados y comentarios asociados.
- **Comentarios y comunicación**: Dejar preguntas o comentarios antes o después de las citas, que serán respondidos por el taller.

#### 2. Mecánico (Panel del Mecánico)

Los **mecánicos** pueden:
- **Ver y gestionar las citas asignadas**: Acceder a una lista de citas programadas con detalles del servicio y vehículo.
- **Actualizar el estado de las citas**: Marcar citas como "en progreso" o "completadas" y dejar comentarios.
- **Comunicación con los clientes**: Responder a preguntas o comentarios de los clientes sobre sus citas.
- **Historial de trabajo**: Revisar su historial de tareas completadas y citas.

#### 3. Administrador (Panel del Administrador)

El **administrador** tiene control total sobre la plataforma y puede:
- **Gestionar usuarios**: Añadir, eliminar o modificar la información de usuarios (clientes o mecánicos) y asignar roles.
- **Gestionar citas y servicios**: Ver, modificar o reasignar citas, y gestionar los servicios ofrecidos (ajustando tiempos, agregando nuevos servicios).
- **Configurar parámetros del taller**: Ajustar el número máximo de citas por hora y otros parámetros operativos.
- **Reportes y estadísticas**: Acceso a estadísticas sobre citas realizadas, servicios completados y el rendimiento general del taller.

---

### Resumen

**Auto Agenda Taller** es una solución completa para la gestión de citas en talleres automotrices, proporcionando una experiencia fluida tanto para clientes como para el personal del taller. Con una interfaz amigable y un backend robusto, la plataforma optimiza el uso del tiempo y los recursos del taller, permitiendo a los clientes gestionar sus citas de manera fácil. El uso de tecnologías modernas como **React.js**, **Flask**, **PostgreSQL** y la integración con **Brevo** para notificaciones por **email** y **SMS** asegura que la aplicación sea rápida, segura y escalable para mejoras futuras. La plataforma está desplegada utilizando **Render** y **Heroku**, garantizando flexibilidad y disponibilidad óptima.
