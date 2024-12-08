document.addEventListener("DOMContentLoaded", () => {
    // Recuperar el nombre y el ID del usuario desde localStorage
    const username = localStorage.getItem("name");
    const userId = localStorage.getItem("userId");

    console.log(username, userId);  // Verifica si los valores existen en el localStorage

    // Verificar si los datos existen
    if (!username || !userId) {
        window.location.href = "login.html"; // Redirige si no hay datos del usuario
        return;
    }

    // Mostrar el nombre del usuario en la sección de bienvenida
    const welcomeSection = document.querySelector(".welcome-section h1");

    welcomeSection.textContent += ` ${username}`;
});
