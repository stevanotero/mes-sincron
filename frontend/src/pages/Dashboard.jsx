import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import LineaForm from "../components/LineaForm";

function Dashboard() {
    const [lineas, setLineas] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [mostrarForm, setMostrarForm] = useState(false);
    const [lineaEditar, setLineaEditar] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const cargarLineas = async () => {
        setCargando(true);
        setError("");
        try {
            const respuesta = await api.get("/api/lineas/");
            setLineas(respuesta.data);
        } catch (err) {
            setError("No se pudieron cargar las líneas");
        } finally {
            setCargando(false);
        }
    };

    useEffect(() => {
        cargarLineas();
    }, []);

    const manejarLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const manejarNuevaLinea = () => {
        setLineaEditar(null);
        setMostrarForm(true);
    };

    const manejarEditar = (linea) => {
        setLineaEditar(linea);
        setMostrarForm(true);
    };

    const manejarGuardar = async (datos) => {
        if (lineaEditar) {
            await api.put(`/api/lineas/${lineaEditar.id}`, datos);
        } else {
            await api.post("/api/lineas/", datos);
        }
        setMostrarForm(false);
        setLineaEditar(null);
        cargarLineas();
    };

    const manejarCancelar = () => {
        setMostrarForm(false);
        setLineaEditar(null);
    };

    const manejarEliminar = async (id) => {
        const confirmar = window.confirm("¿Seguro que quieres eliminar esta línea?");
        if (!confirmar) return;

        try {
            await api.delete(`/api/lineas/${id}`);
            cargarLineas();
        } catch (err) {
            setError("No se pudo eliminar la línea");
        }
    };

    return (
        <div style={{ maxWidth: "900px", margin: "40px auto", fontFamily: "sans-serif" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2>Micro MES - Líneas de producción</h2>
                <button onClick={manejarLogout} style={{ padding: "8px 16px" }}>
                    Cerrar sesión
                </button>
            </div>

            {!mostrarForm && (
                <button onClick={manejarNuevaLinea} style={{ padding: "8px 16px", margin: "10px 0" }}>
                    + Nueva línea
                </button>
            )}

            {mostrarForm && (
                <LineaForm
                    lineaEditar={lineaEditar}
                    onGuardar={manejarGuardar}
                    onCancelar={manejarCancelar}
                />
            )}

            {error && <p style={{ color: "red" }}>{error}</p>}

            {cargando ? (
                <p>Cargando líneas...</p>
            ) : (
                <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Estado</th>
                            <th>Disponibilidad</th>
                            <th>Rendimiento</th>
                            <th>Calidad</th>
                            <th>OEE</th>
                            <th>Clasificación</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lineas.map((linea) => (
                            <tr key={linea.id}>
                                <td>{linea.id}</td>
                                <td>{linea.nombre_linea}</td>
                                <td>{linea.estado}</td>
                                <td>{linea.disponibilidad}%</td>
                                <td>{linea.rendimiento}%</td>
                                <td>{linea.calidad}%</td>
                                <td>{linea.oee}%</td>
                                <td>{linea.clasificacion}</td>
                                <td>
                                    <button onClick={() => manejarEditar(linea)} style={{ marginRight: "5px" }}>
                                        Editar
                                    </button>
                                    <button onClick={() => manejarEliminar(linea.id)}>
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Dashboard;