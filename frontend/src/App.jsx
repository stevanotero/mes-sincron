import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import RutaProtegida from "./components/RutaProtegida";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <RutaProtegida>
            <Dashboard />
          </RutaProtegida>
        }
      />
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

export default App;