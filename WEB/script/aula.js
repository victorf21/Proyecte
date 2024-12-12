document.addEventListener("DOMContentLoaded", async () => {
    const aulaContainer = document.querySelector("#aula-container");
    const menu = document.querySelector(".menu");

    // Obtener el rol del usuario desde el localStorage
    const userRole = localStorage.getItem("role");

    // Configurar el menú según el rol
    if (userRole === "professor") {
        menu.innerHTML = `
            <ul>
                <li><a href="assistencia.html">Assistencia</a></li>
                <li><a href="llista.html">Llista</a></li>
                <li><a href="horari.html">Horari</a></li>
                <li><a href="modificar.html">Modificar</a></li>
                <li><a href="grafiques.html">Gràfiques</a></li>
            </ul>
        `;
    } else if (userRole === "alumne") {
        menu.innerHTML = `
            <nav class="menu">
                <li><a href="assistenciaalumne.html">Assistencia</a></li>
            </nav>
        `;
    } else {
        alert("Rol desconocido. Redirigiendo al inicio de sesión...");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/aulas/list");
        if (!response.ok) {
            throw new Error("Error al obtener las aulas");
        }

        const aulas = await response.json();

        // Crear un botón por cada aula
        aulas.forEach(aula => {
            const button = document.createElement("button");
            button.classList.add("aula-button");
            button.textContent = aula.nombre; // Texto del botón con el nombre del aula
            button.dataset.codigo = aula.codigo; // Código del aula como atributo de datos
            aulaContainer.appendChild(button);

            // Evento para cada botón
            button.addEventListener("click", () => {
                alert(`Has seleccionado el aula: ${aula.nombre} (Código: ${aula.codigo})`);
            });
        });
    } catch (error) {
        console.error("Error al cargar las aulas:", error);
    }
});
