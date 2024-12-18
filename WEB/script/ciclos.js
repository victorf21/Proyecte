document.addEventListener("DOMContentLoaded", async () => {
    const ciclosContainer = document.querySelector(".ciclos");
    const navMenu = document.querySelector('.menu'); // Asegúrate de que el selector sea correcto
    const user = JSON.parse(localStorage.getItem('user'));
    const role = user.role; // Recuperamos el rol del usuario desde localStorage

    // Mostrar el nombre del usuario en el header
    if (role === "alumno") {
        document.getElementById('header-usuario').textContent = "Alumne: " + user.name;
    } else if (role === "profesor") {
        document.getElementById('header-usuario').textContent = "Professor: " + user.name;
    }

    // Crear el menú de navegación basado en el rol del usuario
    if (role === "alumno") {
        navMenu.innerHTML = `
            <ul>
                <li><a href="assistencia.html">Assistencia</a></li>
            </ul>
        `;
    } else if (role === "profesor") {
        navMenu.innerHTML = `
            <ul>
                <li><a href="llista.html">Llista</a></li>
                <li><a href="horari.html">Horari</a></li>
                <li><a href="modificar.html">Modificar</a></li>
                <li><a href="grafiques.html">Gràfiques</a></li>
            </ul>
        `;
    } else {
        // Si el rol no es reconocido, redirigir al login
        alert("Rol no reconocido. Redirigiendo al inicio de sesión...");
        window.location.href = "index.html";
    }

    // Obtener los ciclos
    const getCiclos = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/ciclos/list"); 
            if (!response.ok) {
                throw new Error("Error al obtener los ciclos");
            }
            return await response.json();
        } catch (error) {
            console.error("Error al cargar los ciclos:", error);
            return [];
        }
    };

    // Obtener los módulos
    const getModulos = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/modulos/list"); 
            if (!response.ok) {
                throw new Error("Error al obtener los módulos");
            }
            return await response.json();
        } catch (error) {
            console.error("Error al cargar los módulos:", error);
            return [];
        }
    };

    // Obtener los registros de pertenecer
    const getPertenecer = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/pertenecer/list"); 
            if (!response.ok) {
                throw new Error("Error al obtener los registros de pertenecer");
            }
            return await response.json();
        } catch (error) {
            console.error("Error al cargar los registros de pertenecer:", error);
            return [];
        }
    };

    // Crear los desplegables para ciclos y módulos
    const createDropdowns = async () => {
        const ciclos = await getCiclos();
        const modulos = await getModulos();
        const pertenecer = await getPertenecer();

        // Crear el dropdown de ciclos
        const cicloSelect = document.createElement("select");
        cicloSelect.setAttribute("id", "ciclo-select");
        const cicloDefaultOption = document.createElement("option");
        cicloDefaultOption.textContent = "Selecciona un cicle";
        cicloSelect.appendChild(cicloDefaultOption);

        // Mostrar solo el nombre_ciclo en el dropdown
        ciclos.forEach(ciclo => {
            const cicloOption = document.createElement("option");
            cicloOption.value = ciclo.codigo_ciclo; // Usamos el ID del ciclo (codigo_ciclo)
            cicloOption.textContent = ciclo.nombre_ciclo; // Solo mostramos el nombre_ciclo
            cicloSelect.appendChild(cicloOption);
        });

        // Crear el dropdown de módulos
        const moduloSelect = document.createElement("select");
        moduloSelect.setAttribute("id", "modulo-select");
        const moduloDefaultOption = document.createElement("option");
        moduloDefaultOption.textContent = "Selecciona un módulo";
        moduloSelect.appendChild(moduloDefaultOption);

        // Agregar los desplegables al contenedor
        ciclosContainer.appendChild(cicloSelect);
        ciclosContainer.appendChild(moduloSelect);

        // Función para actualizar los módulos según el ciclo seleccionado
        cicloSelect.addEventListener("change", (event) => {
            const selectedCiclo = event.target.value;

            // Limpiar los módulos
            moduloSelect.innerHTML = '<option value="">Selecciona un mòdul</option>';

            if (selectedCiclo) {
                // Filtrar los módulos que corresponden al ciclo seleccionado
                const modulosFiltrados = pertenecer
                    .filter(item => item.codigo_ciclo == selectedCiclo)
                    .map(item => item.nombre_modulo);

                // Agregar las opciones de módulos al dropdown
                modulosFiltrados.forEach(modulo => {
                    const moduloOption = document.createElement("option");
                    moduloOption.value = modulo;
                    moduloOption.textContent = modulo;
                    moduloSelect.appendChild(moduloOption);
                });
            }
        });

        // Crear el botón debajo de los desplegables
        const goButton = document.createElement("button");
        goButton.textContent = "Ir a la página alumnes";
        goButton.setAttribute("id", "go-button");
        goButton.classList.add("btn"); // Puedes agregar clases para el estilo

        // Añadir el botón al contenedor
        ciclosContainer.appendChild(goButton);

        // Agregar evento al botón para redirigir a alumnes.html
        goButton.addEventListener("click", () => {
            const selectedCiclo = cicloSelect.options[cicloSelect.selectedIndex];
            const selectedModulo = moduloSelect.options[moduloSelect.selectedIndex];

            // Guardar los nombres seleccionados en localStorage
            if (selectedCiclo && selectedModulo && selectedCiclo.value && selectedModulo.value) {
                localStorage.setItem("selectedCiclo", selectedCiclo.textContent);
                localStorage.setItem("selectedModulo", selectedModulo.textContent);
            }

            // Redirigir a la página alumnes
            window.location.href = "alumnes.html";
        });
    };

    // Ejecutar la función para crear los desplegables y el botón
    await createDropdowns();

    // Agregar el evento para el botón de cerrar sesión
    document.getElementById("logout-button").addEventListener("click", () => {
        // Eliminar los datos de localStorage
        localStorage.clear();
    
        // Redirigir al inicio de sesión
        window.location.href = "index.html";
    });
});