import { useState, useEffect } from "react";

const valoresIniciales = {
    nombre_linea: "",
    capacidad_teorica: "",
    tiempo_planificado: "",
    tiempo_paradas: "",
    unidades_producidas: "",
    unidades_defectuosas: "",
    estado: "Activa",
};

function LineaForm({ lineaEditar, onGuardar, onCancelar }) {
    const [datos, setDatos] = useState(valoresIniciales);
    const [error, setError] = useState("");

    // Si nos pasan una línea para editar, llenamos el formulario con sus datos
    useEffect(() => {
        if (lineaEditar) {
            setDatos({
                nombre_linea: lineaEditar.nombre_linea,
                capacidad_teorica: lineaEditar.capacidad_teorica,
                tiempo_planificado: lineaEditar.tiempo_planificado,
                tiempo_paradas: lineaEditar.tiempo_paradas,
                unidades_producidas: lineaEditar.unidades_producidas,
                unidades_defectuosas: lineaEditar.unidades_defectuosas,
                estado: lineaEditar.estado,
            });
        } else {
            setDatos(valoresIniciales);
        }
    }, [lineaEditar]);

    const manejarCambio = (e) => {
        setDatos({ ...datos, [e.target.name]: e.target.value });
    };

    const manejarSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            // Convertimos los campos numéricos de texto a número antes de enviar
            const datosFormateados = {
                ...datos,
                capacidad_teorica: Number(datos.capacidad_teorica),
                tiempo_planificado: Number(datos.tiempo_planificado),
                tiempo_paradas: Number(datos.tiempo_paradas),
                unidades_producidas: Number(datos.unidades_producidas),
                unidades_defectuosas: Number(datos.unidades_defectuosas),
            };

            await onGuardar(datosFormateados);
        } catch (err) {
            if (err.response?.data?.errores) {
                const mensajes = err.response.data.errores
                    .map((er) => er.mensaje)
                    .join(" / ");
                setError(mensajes);
            } else {
                setError("Ocurrió un error al guardar la línea");
            }
        }
    };

    return (
        <form
            onSubmit={manejarSubmit}
            style={{
                border: "1px solid #ccc",
                padding: "20px",
                borderRadius: "8px",
                marginBottom: "20px",
                maxWidth: "500px",
            }}
        >
            <h3>{lineaEditar ? "Editar línea" : "Nueva línea"}</h3>

            <div style={{ marginBottom: "10px" }}>
                <label>Nombre de la línea</label>
                <input
                    name="nombre_linea"
                    value={datos.nombre_linea}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Capacidad teórica (unid/hora)</label>
                <input
                    type="number"
                    name="capacidad_teorica"
                    value={datos.capacidad_teorica}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Tiempo planificado (min)</label>
                <input
                    type="number"
                    name="tiempo_planificado"
                    value={datos.tiempo_planificado}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Tiempo de paradas (min)</label>
                <input
                    type="number"
                    name="tiempo_paradas"
                    value={datos.tiempo_paradas}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Unidades producidas</label>
                <input
                    type="number"
                    name="unidades_producidas"
                    value={datos.unidades_producidas}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Unidades defectuosas</label>
                <input
                    type="number"
                    name="unidades_defectuosas"
                    value={datos.unidades_defectuosas}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                    required
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>Estado</label>
                <select
                    name="estado"
                    value={datos.estado}
                    onChange={manejarCambio}
                    style={{ width: "100%", padding: "6px" }}
                >
                    <option value="Activa">Activa</option>
                    <option value="Inactiva">Inactiva</option>
                    <option value="Mantenimiento">Mantenimiento</option>
                </select>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <div style={{ display: "flex", gap: "10px" }}>
                <button type="submit" style={{ padding: "8px 16px" }}>
                    Guardar
                </button>
                <button type="button" onClick={onCancelar} style={{ padding: "8px 16px" }}>
                    Cancelar
                </button>
            </div>
        </form>
    );
}

export default LineaForm;