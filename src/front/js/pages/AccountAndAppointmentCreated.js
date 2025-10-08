import React from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "../../styles/accountandappointmentcreated.css";
import logoAutoAgenda from "../../img/autoagendalogo1080.png";

const AccountAndAppointmentCreated = () => {
  const navigate = useNavigate();

  const userDashboard = () => {
    navigate("/userdashboard");
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 page-background">
      <div className="card padding text-center">
        <div className="card-body">
          <h1 className="card-header">tu cuenta y turno se crearon exitosamente!</h1>
          <br />
          <p className="appointment-description">
            Gracias por crear una cuenta y programar una cita con nosotros.
            <br />
            <br />
           Un email de confirmación sera enviado a tu correo.
            <br />
            <br />
            ¡Esperamos verte pronto!
          </p>
          <div className="mt-4">
            <button onClick={userDashboard} className="btn btn-secondary">
              Panel de usuario
            </button>
            <br />
            <img
              src={logoAutoAgenda}
              className="autoAgendaLogo mt-3"
              alt="AutoAgenda Logo"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountAndAppointmentCreated;
