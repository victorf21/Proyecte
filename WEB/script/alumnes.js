document.addEventListener("DOMContentLoaded", () => {
    const alumnosListContainer = document.querySelector("#alumnos-list");
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

    const cicloModuloContainer = document.querySelector("#ciclo-modulo");

    // Recuperar los valores del ciclo y módulo seleccionados
    const selectedCiclo = localStorage.getItem("selectedCiclo");
    const selectedModulo = localStorage.getItem("selectedModulo");

    // Verificar si los valores están en el localStorage
    if (selectedCiclo && selectedModulo) {
        cicloModuloContainer.textContent = `Llista - ${selectedCiclo} - ${selectedModulo}`;
    } else {
        cicloModuloContainer.textContent = "No se ha seleccionado ciclo o módulo.";
    }

    // Simulamos una lista de alumnos (puedes cargarla desde una API o base de datos)
    const alumnos = [
        {nombre: "Juan Pérez" },
        {nombre: "María López" },
        { nombre: "Carlos García" },
        {nombre: "Ana Martínez" },
        {nombre: "Victor Fernández" },
        {nombre: "Albert Penades" },
        {nombre: "Pau Insa" },
        {nombre: "Anna Perez" }
    ];

    // Crear una lista de alumnos con sus respectivos checkboxes
    alumnos.forEach(alumno => {
        const alumnoDiv = document.createElement("div");
        alumnoDiv.classList.add("alumno-item");

        // Crear el nombre del alumno
        const alumnoName = document.createElement("span");
        alumnoName.textContent = alumno.nombre;
        alumnoDiv.appendChild(alumnoName);

        // Crear un contenedor para los checkboxes
        const checkboxesContainer = document.createElement("div");
        checkboxesContainer.classList.add("checkboxes-container");

        // Crear el checkbox para "Present"
        const presentCheckbox = document.createElement("input");
        presentCheckbox.type = "checkbox";
        presentCheckbox.classList.add("present");

        // Crear el checkbox para "Retard"
        const retardCheckbox = document.createElement("input");
        retardCheckbox.type = "checkbox";
        retardCheckbox.classList.add("retard");

        // Crear el checkbox para "Absent"
        const absentCheckbox = document.createElement("input");
        absentCheckbox.type = "checkbox";
        absentCheckbox.classList.add("absent");


        // Añadir los checkboxes al contenedor
        checkboxesContainer.appendChild(presentCheckbox);
        checkboxesContainer.appendChild(retardCheckbox);
        checkboxesContainer.appendChild(absentCheckbox);

        // Añadir el contenedor de los checkboxes al div del alumno
        alumnoDiv.appendChild(checkboxesContainer);

        // Añadir el div del alumno a la lista
        alumnosListContainer.appendChild(alumnoDiv);
    });

    document.getElementById("logout-button").addEventListener("click", () => {
        // Eliminar los datos de localStorage
        localStorage.clear();
    
        // Redirigir al inicio de sesión
        window.location.href = "index.html";
    });

});
