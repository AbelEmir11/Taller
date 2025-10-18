import React, { useState, useContext, useEffect } from "react";
import "../../styles/economicdashboard.css";
import { Context } from "../store/appContext";

const EconomicDashboard = () => {
  const { store, actions } = useContext(Context);
  const [hasAccess, setHasAccess] = useState(false);
  const [loading, setLoading] = useState(true);
  const [financialSummary, setFinancialSummary] = useState(null);
  const [incomes, setIncomes] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [goals, setGoals] = useState([]);
  const [showAddIncome, setShowAddIncome] = useState(false);
  const [showAddExpense, setShowAddExpense] = useState(false);
  const [showAddGoal, setShowAddGoal] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  
  const apiUrl = process.env.BACKEND_URL + "/api";

  useEffect(() => {
    const token = localStorage.getItem("token");
    const roleId = localStorage.getItem("role_id");
    
    setHasAccess(!!token && roleId === "1");
    
    if (token && roleId === "1") {
      loadFinancialData();
    } else {
      setLoading(false);
    }
  }, []);

  const loadFinancialData = async () => {
    try {
      const token = localStorage.getItem("token");
      
      // Cargar resumen financiero
      const summaryResponse = await fetch(`${apiUrl}/financial-summary`, {
        headers: {
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
      });
      
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json();
        setFinancialSummary(summaryData);
      }

      // Cargar ingresos del mes actual
      const now = new Date();
      const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      
      const incomesResponse = await fetch(`${apiUrl}/incomes?start_date=${startOfMonth.toISOString().split('T')[0]}&end_date=${endOfMonth.toISOString().split('T')[0]}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
      });
      
      if (incomesResponse.ok) {
        const incomesData = await incomesResponse.json();
        setIncomes(incomesData);
      }

      // Cargar egresos del mes actual
      const expensesResponse = await fetch(`${apiUrl}/expenses?start_date=${startOfMonth.toISOString().split('T')[0]}&end_date=${endOfMonth.toISOString().split('T')[0]}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
      });
      
      if (expensesResponse.ok) {
        const expensesData = await expensesResponse.json();
        setExpenses(expensesData);
      }

      // Cargar metas financieras
      const goalsResponse = await fetch(`${apiUrl}/financial-goals`, {
        headers: {
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
      });
      
      if (goalsResponse.ok) {
        const goalsData = await goalsResponse.json();
        setGoals(goalsData);
      }

    } catch (error) {
      console.error("Error loading financial data:", error);
      setStatusMessage("Error al cargar los datos financieros");
    } finally {
      setLoading(false);
    }
  };

  const handleAddIncome = async (incomeData) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${apiUrl}/incomes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
        body: JSON.stringify(incomeData),
      });

      if (response.ok) {
        setStatusMessage("Ingreso agregado exitosamente");
        setShowAddIncome(false);
        loadFinancialData(); // Recargar datos
      } else {
        const error = await response.json();
        setStatusMessage("Error: " + error.error);
      }
    } catch (error) {
      setStatusMessage("Error al agregar ingreso");
    }
  };

  const handleAddExpense = async (expenseData) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${apiUrl}/expenses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
        body: JSON.stringify(expenseData),
      });

      if (response.ok) {
        setStatusMessage("Egreso agregado exitosamente");
        setShowAddExpense(false);
        loadFinancialData(); // Recargar datos
      } else {
        const error = await response.json();
        setStatusMessage("Error: " + error.error);
      }
    } catch (error) {
      setStatusMessage("Error al agregar egreso");
    }
  };

  const handleAddGoal = async (goalData) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${apiUrl}/financial-goals`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
          ...store.corsEnabled
        },
        body: JSON.stringify(goalData),
      });

      if (response.ok) {
        setStatusMessage("Meta financiera creada exitosamente");
        setShowAddGoal(false);
        loadFinancialData(); // Recargar datos
      } else {
        const error = await response.json();
        setStatusMessage("Error: " + error.error);
      }
    } catch (error) {
      setStatusMessage("Error al crear meta financiera");
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-AR');
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Cargando...</span>
          </div>
        </div>
      </div>
    );
  }

  if (!hasAccess) {
    return (
      <div className="container py-5">
        <div className="card p-5">
          <div className="card-body mx-auto text-center">
            <h2 className="card-title">Acceso Denegado</h2>
            <p className="card-text mt-3">
              Tu cuenta no tiene acceso a esta sección. Solo los administradores pueden acceder al módulo económico.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="d-flex flex-column economic-dashboard">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1>Dashboard Económico</h1>
          <div>
            <button 
              className="btn btn-success me-2" 
              onClick={() => setShowAddIncome(true)}
            >
              + Ingreso
            </button>
            <button 
              className="btn btn-danger me-2" 
              onClick={() => setShowAddExpense(true)}
            >
              + Egreso
            </button>
            <button 
              className="btn btn-primary" 
              onClick={() => setShowAddGoal(true)}
            >
              + Meta
            </button>
          </div>
        </div>

        {statusMessage && (
          <div className={`alert ${statusMessage.includes('Error') ? 'alert-danger' : 'alert-success'} mt-3`}>
            {statusMessage}
          </div>
        )}

        {/* Resumen Financiero */}
        {financialSummary && (
          <div className="row mb-4">
            <div className="col-md-4">
              <div className="card text-center">
                <div className="card-body">
                  <h5 className="card-title text-success">Ingresos del Mes</h5>
                  <h3 className="text-success">{formatCurrency(financialSummary.monthly_income)}</h3>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center">
                <div className="card-body">
                  <h5 className="card-title text-danger">Egresos del Mes</h5>
                  <h3 className="text-danger">{formatCurrency(financialSummary.monthly_expense)}</h3>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card text-center">
                <div className="card-body">
                  <h5 className="card-title">Balance del Mes</h5>
                  <h3 className={financialSummary.monthly_balance >= 0 ? 'text-success' : 'text-danger'}>
                    {formatCurrency(financialSummary.monthly_balance)}
                  </h3>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Metas Financieras */}
        {goals.length > 0 && (
          <div className="row mb-4">
            <div className="col-12">
              <h3>Metas Financieras</h3>
              <div className="row">
                {goals.map((goal) => (
                  <div key={goal.id} className="col-md-6 mb-3">
                    <div className="card">
                      <div className="card-body">
                        <h5 className="card-title">{goal.title}</h5>
                        <p className="card-text">{goal.description}</p>
                        <div className="progress mb-2">
                          <div 
                            className="progress-bar" 
                            role="progressbar" 
                            style={{width: `${Math.min(goal.progress_percentage, 100)}%`}}
                            aria-valuenow={goal.progress_percentage}
                            aria-valuemin="0" 
                            aria-valuemax="100"
                          >
                            {goal.progress_percentage.toFixed(1)}%
                          </div>
                        </div>
                        <div className="d-flex justify-content-between">
                          <small className="text-muted">
                            {formatCurrency(goal.current_amount)} / {formatCurrency(goal.target_amount)}
                          </small>
                          <small className="text-muted">
                            {goal.target_date ? `Meta: ${formatDate(goal.target_date)}` : 'Sin fecha límite'}
                          </small>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Ingresos Recientes */}
        <div className="row mb-4">
          <div className="col-md-6">
            <h3>Ingresos Recientes</h3>
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Descripción</th>
                    <th>Cliente</th>
                    <th>Monto</th>
                  </tr>
                </thead>
                <tbody>
                  {incomes.slice(0, 5).map((income) => (
                    <tr key={income.id}>
                      <td>{formatDate(income.date)}</td>
                      <td>{income.description}</td>
                      <td>{income.client_name || '-'}</td>
                      <td className="text-success">{formatCurrency(income.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Egresos Recientes */}
          <div className="col-md-6">
            <h3>Egresos Recientes</h3>
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Descripción</th>
                    <th>Categoría</th>
                    <th>Monto</th>
                  </tr>
                </thead>
                <tbody>
                  {expenses.slice(0, 5).map((expense) => (
                    <tr key={expense.id}>
                      <td>{formatDate(expense.date)}</td>
                      <td>{expense.description}</td>
                      <td>{expense.category}</td>
                      <td className="text-danger">{formatCurrency(expense.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Modales para agregar datos */}
        {showAddIncome && (
          <AddIncomeModal 
            onClose={() => setShowAddIncome(false)}
            onSave={handleAddIncome}
          />
        )}

        {showAddExpense && (
          <AddExpenseModal 
            onClose={() => setShowAddExpense(false)}
            onSave={handleAddExpense}
          />
        )}

        {showAddGoal && (
          <AddGoalModal 
            onClose={() => setShowAddGoal(false)}
            onSave={handleAddGoal}
          />
        )}
      </div>
    </div>
  );
};

// Modal para agregar ingresos
const AddIncomeModal = ({ onClose, onSave }) => {
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    client_name: '',
    car_license_plate: '',
    date: new Date().toISOString().slice(0, 16)
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.amount && formData.description) {
      onSave(formData);
    }
  };

  return (
    <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Agregar Ingreso</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Monto *</label>
                <input 
                  type="number" 
                  className="form-control" 
                  value={formData.amount}
                  onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value)})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Descripción *</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Cliente</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={formData.client_name}
                  onChange={(e) => setFormData({...formData, client_name: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Patente del Vehículo</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={formData.car_license_plate}
                  onChange={(e) => setFormData({...formData, car_license_plate: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Fecha</label>
                <input 
                  type="datetime-local" 
                  className="form-control" 
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                />
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-success">Guardar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Modal para agregar egresos
const AddExpenseModal = ({ onClose, onSave }) => {
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    category: '',
    date: new Date().toISOString().slice(0, 16)
  });

  const categories = [
    'Impuestos', 'Alquiler', 'Luz', 'Gas', 'Sueldo', 'Repuestos', 
    'Herramientas', 'Mantenimiento', 'Otros'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.amount && formData.description && formData.category) {
      onSave(formData);
    }
  };

  return (
    <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Agregar Egreso</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Monto *</label>
                <input 
                  type="number" 
                  className="form-control" 
                  value={formData.amount}
                  onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value)})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Descripción *</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Categoría *</label>
                <select 
                  className="form-control" 
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                  required
                >
                  <option value="">Seleccionar categoría</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Fecha</label>
                <input 
                  type="datetime-local" 
                  className="form-control" 
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                />
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-danger">Guardar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Modal para agregar metas
const AddGoalModal = ({ onClose, onSave }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    target_amount: '',
    target_date: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.title && formData.target_amount) {
      onSave(formData);
    }
  };

  return (
    <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Crear Meta Financiera</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Título *</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Descripción</label>
                <textarea 
                  className="form-control" 
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows="3"
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Monto Objetivo *</label>
                <input 
                  type="number" 
                  className="form-control" 
                  value={formData.target_amount}
                  onChange={(e) => setFormData({...formData, target_amount: parseFloat(e.target.value)})}
                  required 
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Fecha Objetivo</label>
                <input 
                  type="date" 
                  className="form-control" 
                  value={formData.target_date}
                  onChange={(e) => setFormData({...formData, target_date: e.target.value})}
                />
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-primary">Crear Meta</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EconomicDashboard;
