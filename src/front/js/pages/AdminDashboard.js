import React, { useState, useContext, useEffect } from "react";
import UserList from "../component/UserList";
import UserProfileModal from "../component/UserProfileModal";
import SettingModal from "../component/SettingModal";
import NotificationList from "../component/NotificationList";
import iconUser from "../../img/icons/icon-user.png";
import iconComments from "../../img/icons/icon-comments.png";
import iconConnect from "../../img/icons/icon-connect.png";
import iconFavorites from "../../img/icons/icon-favorites.png";
import iconBriefcase from "../../img/icons/icon-briefcase.png";
import "../../styles/admindashboard.css";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

const AdminDashboard = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const [isSettingModalOpen, setIsSettingModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [maxAppointmentsPerHour, setMaxAppointmentsPerHour] = useState(null);
  const [clientCount, setClientCount] = useState(0);
  const [appointmentsCount, setAppointmentsCount] = useState(0);
  const [servicesCount, setServicesCount] = useState(0);
  const [carsCount, setCarsCount] = useState(0);
  const [statusMessage, setStatusMessage] = useState("");
  const [hasAccess, setHasAccess] = useState(false);
  const apiUrl = process.env.BACKEND_URL + "/api";
  const [profile, setProfile] = useState({
    email: "",
    password: "********",
  });
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoadingNotifications, setIsLoadingNotifications] = useState(true);

  const handleSettingModalOpen = () => {
    setIsSettingModalOpen(true);
  };

  const handleSettingModalClose = (updatedValue) => {
    if (updatedValue && updatedValue > 0) {
      setMaxAppointmentsPerHour(updatedValue);
      setStatusMessage("✅ Configuración actualizada exitosamente");
      setTimeout(() => setStatusMessage(""), 3000);
    }
    setIsSettingModalOpen(false);
  };

  // Función para cargar notificaciones
  const loadNotifications = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const response = await fetch(`${apiUrl}/notifications`, {
        headers: {
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        }
      });

      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
        const unread = data.filter(n => !n.read).length;
        setUnreadCount(unread);
      } else {
        console.error("Error loading notifications:", response.status);
      }
    } catch (error) {
      console.error("Error loading notifications:", error);
    } finally {
      setIsLoadingNotifications(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    const roleId = localStorage.getItem("role_id");
    const userId = localStorage.getItem("user_id");

    setHasAccess(!!token && roleId === "1");

    if (token && roleId === "1" && userId) {
      // Cargar perfil del admin
      const loadProfile = async () => {
        try {
          const response = await fetch(`${apiUrl}/users/${userId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled
            },
          });

          if (!response.ok) {
            console.error("Failed to fetch profile");
          } else {
            const data = await response.json();
            setProfile({
              name: data.result.name,
              email: data.result.email,
              password: "********",
            });
          }
        } catch (error) {
          console.error("Error loading profile:", error);
        }
      };

      // Cargar contadores
      const totalCount = async () => {
        try {
          const response = await fetch(`${apiUrl}/totalcount`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled
            },
          });
          if (!response.ok) {
            return false;
          } else {
            const data = await response.json();
            setClientCount(data.total_clients);
            setAppointmentsCount(data.total_appointments);
            setServicesCount(data.total_services);
            setCarsCount(data.total_cars);
          }
        } catch (error) {
          console.error("Error loading counters:", error);
        }
      };

      // Cargar configuración
      const loadSetting = async () => {
        try {
          const response = await fetch(`${apiUrl}/settings`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled
            },
          });
          if (response.ok) {
            const data = await response.json();
            setMaxAppointmentsPerHour(data.max_appointments_per_hour);
          }
        } catch (error) {
          console.error("Error loading setting:", error);
        }
      };

      // Ejecutar todas las cargas
      loadProfile();
      totalCount();
      loadSetting();
      loadNotifications();

      // Polling para notificaciones cada 10 segundos
      const intervalId = setInterval(() => {
        loadNotifications();
      }, 10000);

      return () => clearInterval(intervalId);
    }
  }, []);

  const handleProfileModalOpen = () => {
    setIsProfileModalOpen(true);
  };

  const handleProfileModalClose = (updatedProfile) => {
    if (updatedProfile) {
      setProfile((prevProfile) => ({
        ...prevProfile,
        email: updatedProfile.email,
      }));
      setStatusMessage("✅ Perfil actualizado exitosamente");
      setTimeout(() => setStatusMessage(""), 3000);
    }
    setIsProfileModalOpen(false);
  };

  const saveProfile = async (updatedProfile) => {
    try {
      const result = await actions.saveProfile(updatedProfile);
      if (result.success) {
        setProfile((prevProfile) => ({
          ...prevProfile,
          email: updatedProfile.email,
        }));
        setStatusMessage("✅ Perfil actualizado exitosamente");
        setTimeout(() => setStatusMessage(""), 3000);
        setIsProfileModalOpen(false);
      } else {
        alert("Error updating profile: " + result.error.message);
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    }
  };

  // Función para enviar email desde una notificación
  const sendEmailFromNotification = async (notificationId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      throw new Error("No hay token de autenticación");
    }

    try {
      const response = await fetch(`${apiUrl}/notifications/${notificationId}/send_email`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
          ...store.corsEnabled
        }
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error al enviar el correo');
      }

      // Recargar notificaciones después de enviar el email
      await loadNotifications();

      setStatusMessage(`✅ Email enviado exitosamente a ${data.client_name}`);
      setTimeout(() => setStatusMessage(""), 5000);

      return data;
    } catch (error) {
      console.error("Error sending email:", error);
      setStatusMessage("❌ " + (error.message || "Error al enviar correo al cliente"));
      setTimeout(() => setStatusMessage(""), 5000);
      throw error;
    }
  };

  return (
    <div className="container py-5">
      <div className="d-flex flex-column dashboard">
        <div className="dashboard-header-section">
          <h1>🔧 Panel de Administrador</h1>
          
          {/* Icono de notificaciones mejorado */}
          {hasAccess && (
            <div className="notification-bell-container">
              <button 
                className="btn-notification-bell" 
                type="button"
                onClick={() => {
                  const notifSection = document.getElementById('notifications-section');
                  if (notifSection) {
                    notifSection.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
              >
                🔔
                {unreadCount > 0 && (
                  <span className="notification-count-badge">
                    {unreadCount}
                  </span>
                )}
              </button>
              {unreadCount > 0 && (
                <span className="notification-text">
                  {unreadCount} {unreadCount === 1 ? 'notificación nueva' : 'notificaciones nuevas'}
                </span>
              )}
            </div>
          )}
        </div>

        {!hasAccess ? (
          <div className="card p-5">
            <div className="card-body mx-auto">
              <h2 className="card-title">
                ⚠️ Tu cuenta no tiene acceso a esta página
              </h2>
              <p className="card-text mt-3">
                Por favor, contacta al administrador del sistema.           
              </p>
            </div>
          </div>
        ) : (
          <>
            {/* Mensaje de estado */}
            {statusMessage && (
              <div className={`alert ${statusMessage.includes('❌') ? 'alert-danger' : 'alert-success'} alert-dismissible fade show`} role="alert">
                {statusMessage}
                <button type="button" className="btn-close" onClick={() => setStatusMessage("")}></button>
              </div>
            )}

            {/* Estadísticas */}
            <div className="stats row">
              <div className="stat1 col mx-2">
                <img src={iconUser} alt="Total Clients" />
                <h3>Total clientes</h3>
                <p>{clientCount}</p>
              </div>
              <div className="stat2 col mx-2">
                <img src={iconComments} alt="Total Appointments" />
                <h3>Total turnos</h3>
                <p>{appointmentsCount}</p>
              </div>
              <div className="stat3 col mx-2">
                <img src={iconBriefcase} alt="Total Services" />
                <h3>Total Servicios</h3>
                <p>{servicesCount}</p>
              </div>
              <div className="stat4 col mx-2">
                <img src={iconFavorites} alt="Total Cars" />
                <h3>Total vehículos</h3>
                <p>{carsCount}</p>
              </div>
              <div className="stat5 col mx-2">
                <img src={iconConnect} alt="Settings" />
                <h3>Ajustes</h3>
                <p>Máximo de turnos por hora: {maxAppointmentsPerHour}</p>
                <button
                  className="btn btn-secondary btnSetting"
                  onClick={handleSettingModalOpen}
                >
                  Editar
                </button>
              </div>
              <div className="stat5 col mx-2">
                <img src={iconConnect} alt="Profile" />
                <h3>Perfil</h3>
                <div>
                  <p>Email: {profile.email}</p>
                </div>
                <button
                  className="btn btn-secondary btnSetting"
                  onClick={handleProfileModalOpen}
                >
                  Editar
                </button>
              </div>
              <div className="stat6 col mx-2">
                <img src={iconBriefcase} alt="Economic" />
                <h3>Gestión Económica</h3>
                <p>Ingresos, egresos y metas</p>
                <button
                  className="btn btn-primary btnSetting"
                  onClick={() => navigate('/economic-dashboard')}
                >
                  Acceder
                </button>
              </div>
            </div>

            {/* Lista de usuarios */}
            <UserList />

            {/* Sección de notificaciones */}
            <div id="notifications-section">
              <NotificationList 
                notifications={notifications} 
                onSendEmail={sendEmailFromNotification}
                isLoading={isLoadingNotifications}
              />
            </div>
          </>
        )}

        {/* Modales */}
        {isSettingModalOpen && (
          <SettingModal
            onClose={handleSettingModalClose}
            onSave={(value) => {
              setMaxAppointmentsPerHour(value);
              setStatusMessage("✅ Configuración actualizada exitosamente");
              setTimeout(() => setStatusMessage(""), 3000);
            }}
            currentValue={maxAppointmentsPerHour}
          />
        )}
        {isProfileModalOpen && (
          <UserProfileModal
            user={profile}
            onSave={saveProfile}
            onClose={() => setIsProfileModalOpen(false)}
            error={statusMessage}
            isAdmin={true}
          />
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;