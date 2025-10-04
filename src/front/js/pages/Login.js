import React, { useContext, useState } from "react";
import "../../styles/login.css";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import ForgotPasswordModal from "../component/ForgotPasswordModal";

const Login = () => {
  const { actions } = useContext(Context);
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [isForgotPasswordModalOpen, setIsForgotPasswordModalOpen] = useState(false);

  const handleForgotPasswordModalOpen = () => {
    setIsForgotPasswordModalOpen(false);
    setTimeout(() => {
      setIsForgotPasswordModalOpen(true);
    }, 0);
  };

  const handleForgotPasswordModalClose = () => {
    setIsForgotPasswordModalOpen(false);
  };

  async function submitForm(event) {
    event.preventDefault();
    let formData = new FormData(event.target);
    let email = formData.get("inputEmail");
    let password = formData.get("inputPassword");

    if (!email || !password) {
      setError("All fields are required");
      return;
    }

    setError(null);

    try {
      let response = await actions.login(email, password);
      
      if (response.success) {
        const roleId = localStorage.getItem("role_id");
        if (roleId == 1) {
          navigate("/admindashboard");
        } else if (roleId == 2) {
          navigate("/mechanicdashboard");
        } else if (roleId == 3) {
          navigate("/userdashboard");
        }
      } else {
        setError(response.message || "Invalid email or password. Please try again.");
      }
    } catch (error) {
      console.error("Error al hacer login:", error);
      setError("An error occurred while trying to log in. Please try again later.");
    }
  }

  return (
    <div
      id="content"
      className="d-flex justify-content-center align-items-center min-vh-100"
    >
      <div className="col-md-5">
        <div className="card">
          <div className="card-header">
            <strong>
              Inicia sesión en tu cuenta
            </strong>
          </div>
          <div className="card-body">
            <form onSubmit={submitForm}>
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}
              <div className="form-group">
                <label className="text-muted" htmlFor="inputEmail">
                  Correo electrónico
                </label>
                <input
                  name="inputEmail"
                  type="email"
                  className="form-control"
                  id="InputEmail1"
                  aria-describedby="emailHelp"
                  placeholder="Ingresa tu email"
                />
                <small id="emailHelp" className="form-text text-muted">
                no compartiremos tu email con nadie más.
                </small>
              </div>
              <div className="form-group">
                <label className="text-muted" htmlFor="inputPassword">
                  Contraseña
                </label>
                <input
                  name="inputPassword"
                  type="password"
                  className="form-control"
                  id="inputPassword"
                  placeholder="Contraseña"
                />
                <small id="passwordHelp" className="form-text text-muted">
                  
                 Tu contraseña debe tener al menos 8 caracteres.
                </small>
              </div>
              <div className="form-group mt-2">
                <span
                  className="text-primary"
                  role="button"
                  onClick={handleForgotPasswordModalOpen}
                >
                  Olvidaste tu contraseña?
                </span>
              </div>
              <button type="submit" className="btn btn-primary mt-3">
                Enviar
              </button>
            </form>
          </div>
        </div>
      </div>
      <ForgotPasswordModal
        isOpen={isForgotPasswordModalOpen}
        onClose={handleForgotPasswordModalClose}
      />
    </div>
  );
};

export default Login;
