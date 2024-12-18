document.addEventListener("DOMContentLoaded", async () => {
    const ufsContainer = document.querySelector("#ufs-container");

    // Obtener el rol del usuario desde el localStorage
    const user = JSON.parse(localStorage.getItem('user'));

    // Crear el menú de navegación basado en el rol del usuario
    const navMenu = document.querySelector('.menu');
    const role = user.role;

    // Mostrar el nombre del usuario según su rol
    if (role === "alumno") {
        document.getElementById('header-usuario').textContent = "Alumne: " + user.name;
    } else if (role === "profesor") {
        document.getElementById('header-usuario').textContent = "Professor: " + user.name;
    } else {
        alert("Rol no reconocido. Redirigiendo al inicio de sesión...");
        window.location.href = "index.html";
    }

    // Configurar el menú de navegación
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
    }
    try {
        const response = await fetch("http://127.0.0.1:8000/uf/list");
        if (!response.ok) {
            throw new Error("Error al obtener las ufs");
        }
        const ufs = await response.json();
        console.log(ufs)
        // Crear un botón por cada uf
        ufs.forEach(uf => {
            const button = document.createElement("button");
            button.classList.add("uf-button");
            button.textContent = uf.nombre_uf; // Texto del botón con el nombre del uf
            ufsContainer.appendChild(button);

            // Evento para cada botón
            button.addEventListener("click", () => {
                localStorage.setItem('nombre_uf', uf.nombre_uf);
                window.location.href = "grafiquesalumne.html";
            });
        });
    } catch (error) {
        console.error("Error al cargar las ufs:", error);
    }

    // Botón de logout
    document.getElementById("logout-button").addEventListener("click", () => {
        localStorage.clear();
        window.location.href = "index.html";
    });
});
