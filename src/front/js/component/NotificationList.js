import React from 'react';

const NotificationList = ({ notifications, onSendEmail }) => {
  return (
    <div className="notifications-container mt-4">
      <h3>Notificaciones</h3>
      <div className="list-group">
        {notifications.map((notification) => (
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
                <button
                  className="btn btn-sm btn-primary"
                  onClick={() => onSendEmail(notification.id)}
                >
                  Avisar al cliente
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default NotificationList;
