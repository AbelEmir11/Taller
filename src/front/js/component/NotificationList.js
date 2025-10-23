import React, { useState } from 'react';

const NotificationList = ({ notifications, onSendEmail }) => {
  const [loading, setLoading] = useState({});
  const [error, setError] = useState({});
  const [success, setSuccess] = useState({});

  const handleSendEmail = async (notificationId) => {
    setLoading(prev => ({ ...prev, [notificationId]: true }));
    setError(prev => ({ ...prev, [notificationId]: null }));
    setSuccess(prev => ({ ...prev, [notificationId]: false }));

    try {
      await onSendEmail(notificationId);
      setSuccess(prev => ({ ...prev, [notificationId]: true }));
    } catch (err) {
      setError(prev => ({ ...prev, [notificationId]: err.message || 'Error al enviar email' }));
    } finally {
      setLoading(prev => ({ ...prev, [notificationId]: false }));
    }
  };

  return (
    <div className="notifications-container mt-4">
      <h3>Notificaciones</h3>
      <div className="list-group">
        {notifications.length === 0 ? (
          <div className="list-group-item">
            <p className="mb-1">No hay notificaciones.</p>
          </div>
        ) : (
          notifications.map((notification) => (
            <div 
              key={notification.id} 
              className={`list-group-item ${!notification.read ? 'list-group-item-info' : ''}`}
            >
              <div className="d-flex w-100 justify-content-between">
                <h5 className="mb-1">{notification.title}</h5>
                <small>{new Date(notification.created_at).toLocaleDateString()}</small>
              </div>
              <p className="mb-1">{notification.message}</p>

              {/* Si es notificación interna con appointment_id, permitir avisar al cliente */}
              {notification.type === 'internal' && notification.appointment_id && onSendEmail && (
                <div className="mt-2">
                  {error[notification.id] && (
                    <div className="alert alert-danger py-1">{error[notification.id]}</div>
                  )}
                  {success[notification.id] && (
                    <div className="alert alert-success py-1">Email enviado correctamente</div>
                  )}
                  <button
                    className={`btn btn-sm ${success[notification.id] ? 'btn-success' : 'btn-primary'}`}
                    onClick={() => handleSendEmail(notification.id)}
                    disabled={loading[notification.id]}
                  >
                    {loading[notification.id] ? 'Enviando...' : 
                     success[notification.id] ? 'Email enviado ✓' : 'Avisar al cliente'}
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default NotificationList;
