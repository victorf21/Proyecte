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

    document.getElementById("logout-button").addEventListener("click", () => {
        // Eliminar los datos de localStorage
        localStorage.clear();
    
        // Redirigir al inicio de sesión
        window.location.href = "index.html";
    });
});
