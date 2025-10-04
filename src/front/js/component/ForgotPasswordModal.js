import React from "react";

const ForgotPasswordModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="modal fade show d-block" tabIndex="-1" role="dialog">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Olvidaste tu contraseña?</h5>
                        <button type="button" className="close" onClick={onClose}>
                            <span>&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <p>Ponte en contacto con l administrador del sitio web 
                            para restaurar tu contraseña.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPasswordModal;
