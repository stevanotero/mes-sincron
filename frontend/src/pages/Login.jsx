import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const respuesta = await api.post("/api/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", respuesta.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div style={{ maxWidth: "350px", margin: "100px auto", fontFamily: "sans-serif" }}>
      <h2>Micro MES - Iniciar sesión</h2>

      <form onSubmit={manejarSubmit}>
        <div style={{ marginBottom: "10px" }}>
          <label>Usuario</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>

        <div style={{ marginBottom: "10px" }}>
          <label>Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" style={{ width: "100%", padding: "10px" }}>
          Entrar
        </button>
      </form>
    </div>
  );
}

export default Login;