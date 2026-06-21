# Cuestionario de Conocimientos Teóricos

## A. Ecosistema Front-end (React)

### 1. ¿Qué es React y qué diferencias tiene respecto a frameworks estructurados como Angular o Vue.js?

React es una biblioteca de JavaScript desarrollada por Meta para construir interfaces de usuario basadas en componentes reutilizables. A diferencia de Angular, que es un framework completo con herramientas integradas, React se enfoca únicamente en la capa de vista y permite elegir librerías externas para enrutamiento, manejo de estado y otras funcionalidades. Vue.js se encuentra en un punto intermedio, ofreciendo una estructura más completa que React pero más flexible que Angular.

### 2. Explica en qué consiste el proceso de Reconciliación (Reconciliation) y el funcionamiento del Virtual DOM en React.

El Virtual DOM es una representación ligera del DOM real almacenada en memoria. Cuando ocurre un cambio de estado, React crea una nueva versión del Virtual DOM y la compara con la anterior mediante un proceso llamado Reconciliation. Luego actualiza únicamente los elementos modificados en el DOM real, mejorando el rendimiento de la aplicación.

### 3. ¿Cuál es la diferencia entre los hooks useMemo y useCallback?

useMemo memoriza el resultado de una operación costosa para evitar recalcularla en cada renderizado. useCallback memoriza una función para evitar que se cree nuevamente en cada render.

Ejemplo:

* useMemo: cálculos complejos sobre listas grandes.
* useCallback: pasar funciones a componentes hijos optimizados con React.memo.

### 4. Explica detalladamente las fases de ciclo de vida representadas por el hook useEffect.

Montaje: se ejecuta cuando el componente se crea por primera vez.

Actualización: se ejecuta cuando cambian las dependencias especificadas.

Desmontaje: se ejecuta cuando el componente se elimina de la interfaz mediante la función de limpieza (cleanup function).

Ejemplo:

```javascript
useEffect(() => {
  const interval = setInterval(() => {}, 1000);

  return () => {
    clearInterval(interval);
  };
}, []);
```

### 5. ¿Cómo se puede gestionar el estado global en una aplicación React sin recurrir a librerías externas?

Utilizando Context API junto con useContext y useReducer. Esto permite compartir datos entre múltiples componentes sin necesidad de instalar librerías externas como Redux.

### 6. ¿Cuál es la diferencia entre componentes controlados y no controlados en React al trabajar con formularios?

Los componentes controlados almacenan el valor del formulario en el estado de React y cada cambio se maneja mediante eventos. Los no controlados permiten que el DOM gestione directamente los valores utilizando referencias (refs).

### 7. ¿Para qué sirven las Keys al renderizar listas en React y por qué se desaconseja utilizar el índice del arreglo como key?

Las Keys permiten a React identificar elementos únicos dentro de una lista para optimizar las actualizaciones. Utilizar índices puede generar comportamientos incorrectos cuando se agregan, eliminan o reordenan elementos.

### 8. ¿Qué es un Custom Hook y en qué escenarios resulta útil crearlo?

Un Custom Hook es una función personalizada que reutiliza lógica basada en hooks. Es útil cuando varios componentes necesitan compartir la misma lógica, como autenticación, peticiones HTTP o manejo de formularios.

### 9. ¿Cómo funciona React.Suspense y la carga perezosa (lazy) para la división de código?

React.lazy permite cargar componentes únicamente cuando son necesarios. React.Suspense muestra un contenido temporal mientras el componente se descarga. Esto reduce el tamaño inicial de la aplicación y mejora el rendimiento.

### 10. ¿Cómo manejas las condiciones de carrera (race conditions) que ocurren cuando se realizan múltiples peticiones asíncronas consecutivas dentro de un useEffect?

Se pueden utilizar AbortController para cancelar solicitudes anteriores, controlar dependencias correctamente y verificar que la respuesta recibida corresponda a la solicitud más reciente antes de actualizar el estado.

# B. Python, FastAPI y Bases de Datos (PostgreSQL sin ORM)

### 1. ¿Qué es FastAPI y en qué se diferencia de frameworks tradicionales de Python como Django o Flask (mencione ASGI y WSGI)?

FastAPI es un framework moderno para desarrollar APIs en Python. Está basado en ASGI (Asynchronous Server Gateway Interface), lo que le permite manejar operaciones asíncronas de manera eficiente. Flask y Django tradicionalmente utilizan WSGI (Web Server Gateway Interface), orientado principalmente a operaciones síncronas. Gracias a ASGI, FastAPI ofrece un mejor rendimiento en aplicaciones con muchas conexiones concurrentes.

### 2. ¿Qué rol desempeñan los Type Hints de Python y la librería Pydantic dentro del ecosistema de FastAPI?

Los Type Hints permiten definir explícitamente los tipos de datos esperados en variables, funciones y parámetros. FastAPI utiliza esta información junto con Pydantic para validar automáticamente los datos recibidos y generar documentación interactiva mediante OpenAPI y Swagger.

### 3. Explica cómo funciona la concurrencia basada en async y await en Python. ¿Cuándo se debe definir una ruta de FastAPI como async def frente a un def clásico?

Las palabras clave async y await permiten ejecutar tareas concurrentes sin bloquear el hilo principal mientras se esperan operaciones de entrada/salida como consultas a bases de datos o llamadas a APIs externas. Se utiliza async def cuando se realizan operaciones asíncronas. Se utiliza def cuando la lógica es completamente síncrona o realiza cálculos rápidos.

### 4. ¿Qué es y cómo funciona el sistema de Inyección de Dependencias (Depends) en FastAPI?

Depends permite reutilizar lógica común en diferentes rutas sin duplicar código. FastAPI ejecuta automáticamente las dependencias antes de ejecutar la ruta principal. Es útil para autenticación, validación de usuarios y manejo de conexiones a bases de datos.

Ejemplo:

```python
from fastapi import Depends

def obtener_usuario():
    return {"usuario": "admin"}

@app.get("/perfil")
def perfil(usuario=Depends(obtener_usuario)):
    return usuario
```

### 5. ¿Qué es el Global Interpreter Lock (GIL) en Python y cómo influye en el rendimiento de un servicio backend cuando se procesan tareas intensivas de CPU?

El GIL es un mecanismo interno de Python que permite que solo un hilo ejecute código Python a la vez dentro de un proceso. Esto limita el rendimiento en tareas intensivas de CPU, aunque no suele afectar significativamente aplicaciones web orientadas a operaciones de entrada/salida.

### 6. Explica la diferencia entre las estructuras de datos list y tuple en Python en términos de mutabilidad y rendimiento de memoria.

Las listas (list) son mutables, por lo que sus elementos pueden modificarse después de su creación. Las tuplas (tuple) son inmutables y generalmente consumen menos memoria. Las tuplas son apropiadas cuando los datos no deben cambiar durante la ejecución.

### 7. ¿Qué es un generador (yield) en Python y cómo se utiliza de manera eficiente para manejar la apertura y cierre de conexiones a bases de datos en FastAPI?

Un generador utiliza la palabra clave yield para producir valores bajo demanda sin almacenarlos todos en memoria. En FastAPI puede utilizarse para abrir una conexión a la base de datos antes de la petición y cerrarla automáticamente al finalizar, garantizando una correcta liberación de recursos.

### 8. En un entorno donde no se utiliza un ORM, ¿cómo se previenen los ataques de Inyección SQL (SQLi) al ejecutar sentencias dinámicas en PostgreSQL desde Python?

Se deben utilizar consultas parametrizadas en lugar de concatenar cadenas de texto. Las librerías como psycopg envían los parámetros por separado de la consulta SQL, evitando que datos maliciosos sean interpretados como instrucciones SQL.

Ejemplo:

```python
cursor.execute(
    "SELECT * FROM usuarios WHERE id = %s",
    (usuario_id,)
)
```

### 9. ¿Qué es el Connection Pooling (Pool de conexiones), por qué es fundamental implementarlo al interactuar directamente con PostgreSQL y qué herramientas lo facilitan?

El Connection Pooling mantiene un conjunto de conexiones abiertas y reutilizables. Esto evita crear y destruir conexiones constantemente, mejorando el rendimiento y reduciendo el consumo de recursos. Librerías como psycopg_pool y asyncpg ofrecen soporte para pools de conexiones.

### 10. ¿Cómo recomiendas gestionar variables de entorno delicadas (como credenciales de base de datos o secretos JWT) en una aplicación backend con FastAPI?

Las credenciales sensibles deben almacenarse en variables de entorno y cargarse mediante archivos .env o configuraciones del sistema operativo. Nunca deben incluirse directamente en el código fuente ni subirse a repositorios públicos. También es recomendable incluir el archivo .env en .gitignore.
