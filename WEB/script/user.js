document.addEventListener("DOMContentLoaded", () => {
    // Recuperar el nombre, ID y rol del usuario desde localStorage
    const name = localStorage.getItem("name");
    const id = localStorage.getItem("id");
    const role = localStorage.getItem("role");


    console.log(name, id, role);  // Verifica si los valores existen en el localStorage

    // Verificar si los datos existen
    if (!name || !id || !role) {
        window.location.href = "login.html"; // Redirige si no hay datos del usuario
        return;
    }

    // Mostrar el nombre del usuario en la sección de bienvenida
    const welcomeSection = document.querySelector(".welcome-section h1");
    welcomeSection.textContent += ` ${name}`;

    // Seleccionar el contenedor del header
    const navMenu = document.querySelector(".menu");

    // Limpiar el contenido existente del menú, si lo hubiera
    navMenu.innerHTML = "";

    // Generar contenido del menú según el rol
    if (role === "alumne") {
        navMenu.innerHTML = `
            <li><a href="assistenciaalumne.html">Assistencia</a></li>
        `;
    } else if (role === "professor") {
        navMenu.innerHTML = `
            <ul>
                <li><a href="assistencia.html">Assistencia</a></li>
                <li><a href="llista.html">Llista</a></li>
                <li><a href="horari.html">Horari</a></li>
                <li><a href="modificar.html">Modificar</a></li>
                <li><a href="grafiques.html">Gràfiques</a></li>
            </ul>
        `;
    } else {
        // Si el rol no es reconocido, mostramos un mensaje y redirigimos al inicio de sesión
        alert("Rol no reconocido. Redirigiendo al inicio de sesión...");
        window.location.href = "login.html";
    }
});
