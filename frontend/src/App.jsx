import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import SharedShell from './components/SharedShell';
import Login from './views/Login';
import CitizenDashboard from './views/CitizenDashboard';
import DispatcherDashboard from './views/DispatcherDashboard';
import DriverDashboard from './views/DriverDashboard';
import HospitalDashboard from './views/HospitalDashboard';

function ProtectedRoute({ allowedRoles, children }) {
  const { role, login } = useAuth();
  const location = window.location.pathname.replace('/', '');
  
  useEffect(() => {
    if (allowedRoles && allowedRoles.includes(location) && role !== location) {
      login(location);
    }
  }, [allowedRoles, location, role, login]);

  return children;
}

function RoleRedirect() {
  const { role } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (role) {
      navigate(`/${role}`, { replace: true });
    }
  }, [role, navigate]);

  return <Login />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          
          <Route path="/citizen" element={
            <ProtectedRoute allowedRoles={['citizen']}>
              <CitizenDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/dispatcher" element={
            <ProtectedRoute allowedRoles={['dispatcher']}>
              <SharedShell><DispatcherDashboard /></SharedShell>
            </ProtectedRoute>
          } />
          
          <Route path="/driver" element={
            <ProtectedRoute allowedRoles={['driver']}>
              <SharedShell><DriverDashboard /></SharedShell>
            </ProtectedRoute>
          } />
          
          <Route path="/hospital" element={
            <ProtectedRoute allowedRoles={['hospital']}>
              <SharedShell><HospitalDashboard /></SharedShell>
            </ProtectedRoute>
          } />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
