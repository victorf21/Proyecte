const loginForm = document.querySelector("form");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Obtén los valores de email y contraseña
    const email = document.querySelector("#email").value;
    const contraseña = document.querySelector("#password").value;

    try {
        // Enviamos la solicitud POST al backend
        const response = await fetch("http://localhost:8000/usuarios/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, contraseña }), // Enviamos los valores como JSON
        });

        // Si la respuesta no es OK, mostrar el error
        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.detail);  // Muestra el mensaje de error
            return;
        }

        // Si la respuesta es exitosa, obtenemos los datos del usuario
        const data = await response.json();
        console.log(data);

        // Guardamos el ID y el rol en el localStorage
        localStorage.setItem("Uid_usuarios", data.id);  // Guarda el ID del usuario
        localStorage.setItem("rol", data.role);  // Guarda el rol del usuario
        localStorage.setItem("nombre", data.name);  // Guarda el nombre del usuario
        // Redirige a la página de usuario
        window.location.href = "user.html"; // Puedes cambiar la URL según tu aplicación
    } catch (error) {
        console.error("Error al iniciar sesión:", error);
        alert("Error en el servidor, por favor intenta nuevamente.");
    }
});