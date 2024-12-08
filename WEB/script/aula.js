document.addEventListener("DOMContentLoaded", async () => {
    const aulaContainer = document.querySelector("#aula-container");

    try {
        const response = await fetch("http://localhost:8000/aulas/aulas");
        
        
        if (!response.ok) {
            throw new Error("Error al obtener las aulas");
        }

        const aulas = await response.json();

        // Crear un botón por cada aula
        aulas.forEach(aula => {
            const button = document.createElement("button");
            button.classList.add("aula-button");
            button.textContent = aula.nombre; // Texto del botón
            button.dataset.id = aula.id;     // ID del aula como atributo de datos
            aulaContainer.appendChild(button);

            // Agregar un evento al botón (opcional)
            button.addEventListener("click", () => {
            });
        });
    } catch (error) {
        console.error("Error al cargar las aulas:", error);
    }
});