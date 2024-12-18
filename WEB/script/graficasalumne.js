document.addEventListener('DOMContentLoaded', function () {
    // Recuperar la información del usuario desde localStorage
    const user = JSON.parse(localStorage.getItem('user'));

    // Si no se encuentra la información del usuario, redirigir al login
    if (!user || !user.id) {
        alert('No se ha encontrado información del usuario.');
        window.location.href = 'index.html';
        return;
    }

    // Crear el menú de navegación basado en el rol del usuario
    const navMenu = document.querySelector('.menu'); // Asegúrate de que el selector sea correcto

    const role = user.role; // Recuperamos el rol del usuario desde localStorage

    if (role === "alumno") {
        document.getElementById('header-usuario').textContent = "Alumne: " + user.name;
    } else if (role === "profesor") {
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

    // Mostrar el módulo seleccionado en el encabezado uf-modulo
    const ufModuloContainer = document.querySelector("#uf-modulo");
    const nombre_modulo = localStorage.getItem('nombre_modulo');
    const nombre_uf = localStorage.getItem('nombre_uf');

    if (nombre_modulo && nombre_uf) {
        ufModuloContainer.textContent = `${nombre_modulo} - ${nombre_uf}`;
    } else {
        ufModuloContainer.textContent = "No se ha seleccionado un módulo.";
    }

    // Botón de logout
    document.getElementById("logout-button").addEventListener("click", () => {
        localStorage.clear(); // Eliminar los datos del localStorage
        window.location.href = "index.html"; // Redirigir al inicio de sesión
    });
});
