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

  const handleSettingModalOpen = () => {
    setIsSettingModalOpen(true);
  };

  const handleSettingModalClose = (updatedValue) => {
    if (updatedValue && updatedValue > 0) {
      setMaxAppointmentsPerHour(updatedValue);
      setStatusMessage("Settings updated successfully");
    }
    setIsSettingModalOpen(false);
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    const roleId = localStorage.getItem("role_id");
    const userId = localStorage.getItem("user_id");

    setHasAccess(!!token && roleId === "1");

    if (token && roleId === "1" && userId) {
      const loadProfile = async () => {
        try {
          const response = await fetch(`${apiUrl}/users/${userId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled // Deshabilitar una vez en producción
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
      loadProfile();

      const totalCount = async () => {
        try {
          const response = await fetch(`${apiUrl}/totalcount`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled // Deshabilitar una vez en producción
            },
          });
          if (!response.ok) {
            return false;
          } else {
            const data = await response.json();
            const clientCount = data.total_clients;
            const appointmentsCount = data.total_appointments;
            const servicesCount = data.total_services;
            const carsCount = data.total_cars;
            return { clientCount, appointmentsCount, servicesCount, carsCount };
          }
        } catch (error) {
          console.error("Error loading counters:", error);
        }
      };
      totalCount();

      const totalCounters = async () => {
        const counts = await totalCount();
        if (counts) {
          setClientCount(counts.clientCount);
          setAppointmentsCount(counts.appointmentsCount);
          setServicesCount(counts.servicesCount);
          setCarsCount(counts.carsCount);
        } else {
          return false
        }
      };
      totalCounters();

      const loadSetting = async () => {
        try {
          const response = await fetch(`${apiUrl}/settings`, {
            headers: {
              Authorization: `Bearer ${token}`,
              ...store.corsEnabled // Deshabilitar una vez en producción
            },
          });
          if (!response.ok) {
            return false;
          } else {
            const data = await response.json();
            setMaxAppointmentsPerHour(data.max_appointments_per_hour);
          }
        } catch (error) {
          console.error("Error loading setting:", error);
        }
      };
      loadSetting();

      const loadNotifications = async () => {
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
          } else {
            const text = await response.text();
            console.error("Error loading notifications:", response.status, text);
          }
        } catch (error) {
          console.error("Error loading notifications:", error);
        }
      };

      // Llamar directamente dentro del bloque con token y roleId (no usar hasAccess que aún no se actualiza)
      loadNotifications();
    }
  }, [store.token, store.setting]);

  const handleProfileModalOpen = () => {
    setIsProfileModalOpen(true);
  };

  const handleProfileModalClose = (updatedProfile) => {
    if (updatedProfile) {
      setProfile((prevProfile) => ({
        ...prevProfile,
        email: updatedProfile.email,
        // name: updatedProfile.name,
      }));
      setStatusMessage("Profile updated successfully");
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
          // name: updatedProfile.name,
        }));
        setStatusMessage("Profile updated successfully");
        setIsProfileModalOpen(false);
      } else {
        alert("Error updating profile: " + result.error.message);
      }
    } catch (error) {
      alert("An error occurred: " + error.message);
    }
  };

  // Nueva función para enviar email desde una notificación
  const sendEmailFromNotification = async (notificationId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(`${apiUrl}/notifications/${notificationId}/send_email`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
          ...store.corsEnabled
        }
      });

      if (response.ok) {
        // recargar notificaciones
        const resp = await fetch(`${apiUrl}/notifications`, {
          headers: {
            Authorization: `Bearer ${token}`,
            ...store.corsEnabled
          }
        });
        if (resp.ok) {
          const data = await resp.json();
          setNotifications(data);
          setStatusMessage("Correo enviado al cliente");
        }
      } else {
        const err = await response.json();
        setStatusMessage("Error: " + (err.error || 'No se pudo enviar el correo'));
      }
    } catch (error) {
      console.error("Error sending email from notification:", error);
      setStatusMessage("Error al enviar correo al cliente");
    }
  };

  return (
    <div className="container py-5">
      <div className="d-flex flex-column dashboard">
        <h1>Panel de administrador</h1>
        {!hasAccess ? (
          <div className="card p-5">
            <div className="card-body mx-auto">
              <h2 className="card-title">
                Tu cuenta no tiene acceso a esta página
              </h2>
              <p className="card-text mt-3">
                Por favor, contacta al administrador del sistema.           
              </p>
            </div>
          </div>
        ) : (
          <>
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
                <h3>Total vehiculos</h3>
                <p>{carsCount}</p>
              </div>
              <div className="stat5 col mx-2">
                <img src={iconConnect} alt="Settings" />
                <h3>Ajustes</h3>
                <p>Maximo de turnos por hora: {maxAppointmentsPerHour}</p>
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
            <UserList />
          </>
        )}
        {isSettingModalOpen && (
          <SettingModal
            onClose={handleSettingModalClose}
            onSave={(value) => {
              setMaxAppointmentsPerHour(value);
              setStatusMessage("Settings updated successfully");
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
        {statusMessage && (
          <div className="alert alert-success mt-3">{statusMessage}</div>
        )}
        {hasAccess && (
          <NotificationList notifications={notifications} onSendEmail={sendEmailFromNotification} />
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
