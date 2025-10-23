import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Context } from '../store/appContext';

const MechanicAppointmentList = () => {
  const [appointments, setAppointments] = useState([]);
  const navigate = useNavigate();
  const { store } = useContext(Context);

  const apiUrl = process.env.BACKEND_URL + "/api";

  useEffect(() => {
    const loadAppointments = async () => {
      try {
        const response = await fetch(`${apiUrl}/appointments`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
            ...store.corsEnabled // Deshabilitar una vez en producción
          },
        });

        if (response.ok) {
          const appointmentsData = await response.json();
          const sortedAppointments = appointmentsData.sort((a, b) => new Date(b.date) - new Date(a.date));
          setAppointments(sortedAppointments);
        } else {
          const errorData = await response.json();
          console.error('Failed to fetch appointments', errorData);
        }
      } catch (error) {
        console.error('Error loading appointments:', error);
      }
    };

    loadAppointments();
  }, []);

  const handleStatusChange = async (appointmentId, status) => {
    try {
      const response = await fetch(`${apiUrl}/appointments/${appointmentId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          ...store.corsEnabled // Deshabilitar una vez en producción
        },
        body: JSON.stringify({ status }),
      });

      if (response.ok) {
        setAppointments(prevAppointments =>
          prevAppointments.map(app =>
            app.id === appointmentId ? { ...app, status } : app
          )
        );

        // Si el estado pasó a "Completed", notificar internamente al admin
        if (status && status.toLowerCase() === "completed") {
          try {
            const notifyResp = await fetch(`${apiUrl}/notifications/notify_appointment_complete/${appointmentId}`, {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
                ...store.corsEnabled
              }
            });
            if (!notifyResp.ok) {
              const txt = await notifyResp.text();
              console.error('Error notifying admin (notify endpoint):', notifyResp.status, txt);
            } else {
              console.log('Admin notificado (notify endpoint) para appointment', appointmentId);
            }
          } catch (err) {
            console.error('Network error notifying admin:', err);
          }
        }

      } else {
        const errorData = await response.json(); 
        console.error('Failed to update appointment status', errorData);
      }
    } catch (error) {
      console.error('Error updating appointment status:', error);
    }
  };

  const handleViewDetails = appointmentId => {
    navigate(`/appointmentdetails/${appointmentId}`);
  };
  const convertUTCToLocal = (date) => {
    const utcDate = new Date(date);
    const localDate = new Date(utcDate.getTime() + utcDate.getTimezoneOffset() * 60000);
    return localDate;
  };
  
  const convertUTCToLocalDate = (date) => {
    return convertUTCToLocal(date).toLocaleDateString();
  };
  
  const convertUTCToLocalTime = (date) => {
    return convertUTCToLocal(date).toLocaleTimeString();
  };

  return (
    <div className="mechanic-appointments">
      <h2 className="fw-bolder text-dark py-3 text-center">Mis turnos asignados </h2>
      <div className="table-responsive">
        <table className="table table-striped table-bordered">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Hora</th>
              <th>Servicio</th>
              <th>Vehiculo</th>
              <th>Cliente</th>
              <th>Estado</th>
              <th>Comentarios</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map(app => (
              <tr key={app.id}>
                <td>{convertUTCToLocalDate(app.date)}</td>  {/* Muestra la fecha correcta */}
                <td>{convertUTCToLocalTime(app.date)}</td>  {/* Muestra la hora correcta */}
                <td>{app.service?.name || 'Unknown'}</td>
                <td>{app.car?.car_model || 'Unknown'}</td>
                <td>{app.user?.name || 'Unknown'}</td>
                <td>
                  <select 
                    value={app.status} 
                    onChange={(e) => handleStatusChange(app.id, e.target.value)}
                  >
                    <option value="Pending">Pendiente</option>
                    <option value="In Progress">En progreso</option>
                    <option value="Completed">Completado</option>
                  </select>
                </td>
                <td>{app.comments?.length || 0}</td>
                <td>
                  <button 
                    className="btn btn-primary" 
                    onClick={() => handleViewDetails(app.id)}
                  >
                    Ver detalles
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MechanicAppointmentList;
