import React, { useContext, useEffect, useState } from "react";
import UserProfile from "../component/UserProfile";
import UserAppointments from "../component/UserAppointments";
import UserCars from "../component/UserCars";
import { Context } from '../store/appContext';
import "../../styles/userdashboard.css";

const UserDashboard = () => {
  const { store, actions } = useContext(Context);
  const [hasAccess, setHasAccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const roleId = localStorage.getItem("role_id");
    setHasAccess(!!token && roleId === "3");
  }, [store.token, localStorage.token]);

  return (
    <div className="container py-4">
      <div className="d-flex flex-column user-dashboard">
        <h1>Panel de Usuario</h1>
        {!hasAccess ? (
        <div className="card p-5">
          <div className="card-body mx-auto">
            <h2 className="card-title">no tienes acceso a esta seccion</h2>
            <p className="card-text mt-3">
             Debes logearte para acceder a tu panel de usuario.
            </p>
          </div>
        </div>
      ) : (
        <>
        <UserProfile />
        <UserAppointments />
        <UserCars />
        </>
      )}
      </div>
    </div>
  );
};

export default UserDashboard;
