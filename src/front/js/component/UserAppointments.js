import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

function UserAppointments() {
  const [appointments, setAppointments] = useState([]);
  const { store } = useContext(Context);
  const navigate = useNavigate();

  const [newComments, setNewComments] = useState({});
  const [errors, setErrors] = useState({});
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [appointmentToCancel, setAppointmentToCancel] = useState(null);

  const apiUrl = process.env.BACKEND_URL + "/api";

  const compareDates = (a, b) => {
    const today = new Date().setHours(0, 0, 0, 0);
    const dateA = new Date(a.date).setHours(0, 0, 0, 0);
    const dateB = new Date(b.date).setHours(0, 0, 0, 0);

    if (dateA >= today && dateB >= today) {
      return dateA - dateB;
    }

    if (dateA < today && dateB < today) {
      return dateA - dateB;
    }

    return dateA < today ? 1 : -1;
  };

  useEffect(() => {
    const userId = localStorage.getItem("user_id");

    const loadAppointments = async () => {
      try {
        const response = await fetch(`${apiUrl}/appointmentsuser/${userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            ...store.corsEnabled // Deshabilitar una vez en producción
          },
        });

        if (response.ok) {
          const appointmentsData = await response.json();
          const sortedAppointments = appointmentsData.sort(compareDates);
          setAppointments(sortedAppointments);
        } else {
          const text = await response.text();
          if (response.status === 404) {
            console.warn("No appointments found (404)");
            setAppointments([]);
          } else {
            console.error("Failed to fetch appointments:", response.status, text);
            setAppointments([]);
          }
        }
      } catch (error) {
        console.error("Error loading appointments:", error);
      }
    };

    loadAppointments();
  }, []);

  const handleAddComment = async (appointmentId) => {
    const token = localStorage.getItem("token");

    if (newComments[appointmentId]?.trim()) {
      try {
        const response = await fetch(`${apiUrl}/comments`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            ...store.corsEnabled // Deshabilitar una vez en producción
          },
          body: JSON.stringify({
            comment: newComments[appointmentId],
            user_id: localStorage.getItem("user_id"),
            appointment_id: appointmentId,
            is_mechanic: false,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to add comment");
        }

        const commentData = await response.json();

        const updatedAppointments = appointments.map((app) => {
          if (app.id === appointmentId) {
            return {
              ...app,
              comments: [...app.comments, commentData],
            };
          }
          return app;
        });

        setAppointments(updatedAppointments);
        setNewComments((prevState) => ({ ...prevState, [appointmentId]: "" }));
        setErrors((prevState) => ({ ...prevState, [appointmentId]: "" }));
      } catch (error) {
        console.error("Error adding comment:", error);
        setErrors((prevState) => ({
          ...prevState,
          [appointmentId]: "Failed to add comment",
        }));
      }
    } else {
      setErrors((prevState) => ({
        ...prevState,
        [appointmentId]: "Comment cannot be blank",
      }));
    }
  };

  const handleCommentChange = (appointmentId, value) => {
    setNewComments((prevState) => ({ ...prevState, [appointmentId]: value }));
    setErrors((prevState) => ({ ...prevState, [appointmentId]: "" }));
  };

  const handleKeyDown = (e, appointmentId) => {
    if (e.key === "Enter") {
      handleAddComment(appointmentId); 
    }
  };

  const handleCancelClick = (appointmentId) => {
    setAppointmentToCancel(appointmentId);
    setShowConfirmModal(true);
  };

  const confirmCancel = async () => {
    try {
      const appoinmentToDelete = appointmentToCancel;
      const response = await fetch(
        `${apiUrl}/appointments/${appoinmentToDelete}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            ...store.corsEnabled // Deshabilitar una vez en producción
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Failed to delete user:", errorData.error);
        return false;
      }

      const updatedAppointments = appointments.filter(
        (app) => app.id !== appoinmentToDelete
      );

      setAppointments(updatedAppointments);
      setShowConfirmModal(false);
      return true;
    } catch (error) {
      return `Error deleting user: ${error.message}`;
    }
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
    <div className="user-appointments">
      <h2 className="fw-bolder text-dark py-3">Mis turnos</h2>
      <button
        onClick={() => navigate("/createappointmentregistereduser")}
        className="btn btn-primary mb-3"
      >
        Solicitar nuevo turno
      </button>
      <div className="table-responsive">
        <table className="table table-striped table-bordered">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Hora</th>
              <th>Servicio</th>
              <th>Vehiculo</th>
              <th>Estado</th>
              <th>Comentarios</th>
              <th>Agregar comentario</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {appointments.length === 0 ? (
              <tr>
                <td colSpan="8" className="text-center">
                  No tienes turnos programados.
                </td>
              </tr>
            ) : (
              appointments.map((app) => (
                <tr key={app.id}>
                  <td>{convertUTCToLocalDate(app.date)}</td>
                  <td>{convertUTCToLocalTime(app.date)}</td>
                  <td>{app.service?.name || "Unknown"}</td>
                  <td>{app.car?.car_model || "Unknown"}</td>
                  <td>{app.status || "Unknown"}</td>
                  <td>
                    {app.comments.map((comment, index) => (
                      <p key={index}>
                        <strong>
                          {comment.is_mechanic ? "Mechanic" : "Client"}:
                        </strong>{" "}
                        {comment.content}
                        <br />
                        <small>
                          ({convertUTCToLocalDate(comment.timestamp)}{" "}
                          {convertUTCToLocalTime(comment.timestamp)})
                        </small>
                      </p>
                    ))}
                  </td>
                  <td>
                    {errors[app.id] && (
                      <div className="alert alert-danger">{errors[app.id]}</div>
                    )}
                    <input
                      type="text"
                      className="form-control"
                      value={newComments[app.id] || ""}
                      onChange={(e) =>
                        handleCommentChange(app.id, e.target.value)
                      }
                      onKeyDown={(e) => handleKeyDown(e, app.id)}
                    />
                    <button
                      className="btn btn-secondary mt-2"
                      onClick={() => handleAddComment(app.id)}
                    >
                      Agregar comentarios
                    </button>
                  </td>
                  <td>
                    {new Date(app.date).setHours(0, 0, 0, 0) >=
                      new Date().setHours(0, 0, 0, 0) && (
                      <button
                        className="btn btn-danger ms-2"
                        onClick={() => handleCancelClick(app.id)}
                      >
                        Cancelar
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showConfirmModal && (
        <div
          className="modal show d-block"
          tabIndex="-1"
          style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirmar cancelacion</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowConfirmModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                <p>Estas seguro de cancelar el turno?</p>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowConfirmModal(false)}
                >
                  No
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={confirmCancel}
                >
                  Si, cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserAppointments;
