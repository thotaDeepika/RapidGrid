import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import SharedShell from './components/SharedShell';
import LandingPage from './views/LandingPage';
import Login from './views/Login';
import CitizenDashboard from './views/CitizenDashboard';
import DispatcherDashboard from './views/DispatcherDashboard';
import DriverDashboard from './views/DriverDashboard';
import HospitalDashboard from './views/HospitalDashboard';
import GuidedDemo from './views/GuidedDemo';
import ControlRoom from './views/ControlRoom';
import Seats, { SeatBanner } from './views/Seats';

/**
 * Demo role gate.
 *
 * Remembers which portal this tab is showing. It is not the staff PIN check.
 */
function DemoRole({ role, children }) {
  const { role: current, login } = useAuth();
  React.useEffect(() => {
    if (current !== role) login(role);
  }, [current, role, login]);
  return children;
}

const UNIT_LABEL = {
  Ambulance: 'Ambulance',
  'Fire Engine': 'Fire engine',
  'Police Cruiser': 'Police unit',
  'Disaster Rescue': 'Rescue unit',
};

/**
 * When staff PINs are on, opening a portal URL is not a sign-in. The API
 * then answers 401, which the consoles used to paint as a dead backend.
 */
function StaffGate({ staffRole, home, children }) {
  const { login } = useAuth();
  const [state, setState] = useState('loading');

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [dirRes, sesRes] = await Promise.all([
          fetch('/api/staff/directory'),
          fetch('/api/staff/session'),
        ]);
        if (!dirRes.ok || !sesRes.ok) throw new Error();
        const dir = await dirRes.json();
        const ses = await sesRes.json();
        if (cancelled) return;
        if (!dir.enabled) {
          setState('open');
          return;
        }
        if (ses.role !== staffRole) {
          setState('closed');
          return;
        }
        if (staffRole === 'unit') {
          const unit = (dir.units || []).find((u) => u.unit_id === ses.subject);
          if (!unit) {
            setState('closed');
            return;
          }
          login('driver', {
            unitId: unit.unit_id,
            vehicleType: unit.type,
            driverName: UNIT_LABEL[unit.type] ?? unit.type,
            hubName: unit.station,
          });
        } else if (staffRole === 'hospital') {
          const hospital = (dir.hospitals || []).find((h) => h.hospital_id === ses.subject);
          if (!hospital) {
            setState('closed');
            return;
          }
          login('hospital', { id: hospital.hospital_id, name: hospital.name });
        } else {
          login('dispatcher');
        }
        setState('open');
      } catch {
        if (!cancelled) setState('error');
      }
    })();
    return () => { cancelled = true; };
    // login is a new function every render; the check runs once per portal.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [staffRole]);

  if (state === 'loading') {
    return (
      <div className="grid min-h-screen place-items-center bg-field px-4">
        <p role="status" className="text-[14px] text-text-muted">Checking sign-in…</p>
      </div>
    );
  }
  if (state === 'error') {
    return (
      <div className="grid min-h-screen place-items-center bg-field px-4">
        <p role="alert" className="max-w-[42ch] text-center text-[14px] text-critical">
          Could not check staff sign-in. Reload the page to try again.
        </p>
      </div>
    );
  }
  if (state === 'closed') {
    const pick = staffRole === 'unit' ? 'driver' : staffRole === 'hospital' ? 'hospital' : 'dispatcher';
    const params = new URLSearchParams({ pick, next: home });
    return <Navigate to={`/login?${params.toString()}`} replace />;
  }
  return children;
}

const portal = (role, View) => {
  const inner = (
    <DemoRole role={role}>
      <SharedShell>
        <View />
      </SharedShell>
    </DemoRole>
  );
  if (role === 'citizen') return inner;
  const staffRole = role === 'driver' ? 'unit' : role;
  return (
    <StaffGate staffRole={staffRole} home={`/${role}`}>
      {inner}
    </StaffGate>
  );
};

// Showcase access token removed: every page opens without one.
function SessionGate({ children }) {
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <SessionGate>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/citizen" element={portal('citizen', CitizenDashboard)} />
            <Route path="/dispatcher" element={portal('dispatcher', DispatcherDashboard)} />
            <Route path="/driver" element={portal('driver', DriverDashboard)} />
            <Route path="/hospital" element={portal('hospital', HospitalDashboard)} />
            <Route path="/demo" element={<GuidedDemo />} />
            <Route path="/seats" element={<Seats />} />
            <Route path="/control" element={
              <StaffGate staffRole="dispatcher" home="/control">
                <DemoRole role="dispatcher"><SeatBanner /><ControlRoom /></DemoRole>
              </StaffGate>
            } />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </SessionGate>
    </AuthProvider>
  );
}
