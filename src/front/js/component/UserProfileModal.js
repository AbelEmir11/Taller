import React, { useState } from 'react';

function UserProfileModal({ user, onSave, onClose, isAdmin }) {
  const [updatedUser, setUpdatedUser] = useState(user);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setError(null);
    setUpdatedUser(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSave = () => {
    if (!updatedUser.email || (isAdmin && !currentPassword)) {
      setError("All required fields must be filled");
      return;
    }

    if (newPassword && newPassword !== confirmPassword) {
      setError("New passwords do not match");
      return;
    }

    onSave({ ...updatedUser, currentPassword, newPassword })
      .then(() => {
        setError(null); 
      })
      .catch((err) => {
        setError("Ocurrio un error, vuelve a intentarlo luego.");
      });
  };

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Editar Perfil</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <div className="modal-body">
            {error && <div className="alert alert-danger">{error}</div>}
            {!isAdmin && (
              <>
                <div className="mb-3">
                  <label className="form-label">Nombre</label>
                  <input type="text" className="form-control" name="name" value={updatedUser.name} onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label className="form-label">Numero de telefono</label>
                  <input type="text" className="form-control" name="phoneNumber" value={updatedUser.phoneNumber} onChange={handleChange} />
                </div>
              </>
            )}
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input type="email" className="form-control" name="email" value={updatedUser.email} onChange={handleChange} />
            </div>
            <div className="mb-3">
              <label className="form-label">Contraseña actual</label>
              <input type="password" className="form-control" name="currentPassword" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Nueva contraseña</label>
              <input type="password" className="form-control" name="newPassword" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Confirmar nueva contraseña</label>
              <input type="password" className="form-control" name="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
            <button type="button" className="btn btn-primary" onClick={handleSave}>Guardar</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserProfileModal;
