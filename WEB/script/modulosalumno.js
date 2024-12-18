document.addEventListener("DOMContentLoaded", async () => {
    const moduloContainer = document.querySelector("#modulo-container");

    // Obtener el rol del usuario desde el localStorage
    const user = JSON.parse(localStorage.getItem('user'));

    // Crear el menú de navegación basado en el rol del usuario
    const navMenu = document.querySelector('.menu'); // Asegúrate de que el selector sea correcto

    const role = user.role; // Recuperamos el rol del usuario desde localStorage
    
    if(role === "alumno"){
        document.getElementById('header-usuario').textContent = "Alumne: " + user.name;
    }else if (role === "profesor"){
        document.getElementById('header-usuario').textContent = "Professor: " + user.name;
    }

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

    try {
        const response = await fetch("http://127.0.0.1:8000/modulos/list");
        if (!response.ok) {
            throw new Error("Error al obtener las modulos");
        }

        const modulos = await response.json();
        console.log(modulos)

        // Crear un botón por cada modulo
        modulos.forEach(modulo => {
            const button = document.createElement("button");
            button.classList.add("modulo-button");
            button.textContent = modulo.nombre_modulo; // Texto del botón con el nombre del modulo
            moduloContainer.appendChild(button);

            // Evento para cada botón
            button.addEventListener("click", () => {
                localStorage.setItem('nombre_modulo', modulo.nombre_modulo);
                window.location.href = "ufs.html";
            });
        });
    } catch (error) {
        console.error("Error al cargar las modulos:", error);
    }

    document.getElementById("logout-button").addEventListener("click", () => {
        // Eliminar los datos de localStorage
        localStorage.clear();
    
        // Redirigir al inicio de sesión
        window.location.href = "index.html";
    });
});
