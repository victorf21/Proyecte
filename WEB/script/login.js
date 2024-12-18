document.addEventListener('DOMContentLoaded', function () {
    // Obtener referencias al formulario y sus campos
    const loginForm = document.querySelector('.login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Evento para manejar el envío del formulario
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario
        
        // Obtener los valores de los campos del formulario
        const email = emailInput.value;
        const password = passwordInput.value;
        
        // Crear el objeto de credenciales
        const credentials = {
            email: email,
            contraseña: password
        };
        
        try {
            // Realizar la solicitud POST a la API de inicio de sesión
            const response = await fetch('http://127.0.0.1:8000/usuarios/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });
            
            // Manejo de la respuesta
            if (response.ok) {
                // Si la respuesta es exitosa, procesar la respuesta JSON
                const data = await response.json();
                console.log('Login exitoso:', data);
                
                // Guardar los datos en localStorage
                localStorage.setItem('user', JSON.stringify({
                    role: data.role,
                    id: data.id,
                    name: data.name
                }));

                // Redirigir al usuario a user.html
                window.location.href = 'user.html'; // Reemplaza esto con la ruta correcta si es necesario
            } else {
                // Si la respuesta no es exitosa, obtener y mostrar el mensaje de error
                const errorData = await response.text(); // Leer el error como texto
                alert('Error en el inicio de sesión: ' + errorData);
            }
        } catch (error) {
            // Manejo de errores en caso de problemas con la conexión o la solicitud
            console.error('Error de conexión:', error);
            alert('Hubo un problema al intentar iniciar sesión. Inténtalo de nuevo.');
        }
    });
});
