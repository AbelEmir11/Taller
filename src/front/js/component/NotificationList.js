import React from 'react';

const NotificationList = ({ notifications }) => {
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
          </div>
        ))}
      </div>
    </div>
  );
};

export default NotificationList;
