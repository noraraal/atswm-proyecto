// Funciones comunes de autenticación para las páginas

// Actualiza la navbar según si el usuario está logueado o no
async function updateNav() {
    const navLinks = document.getElementById('nav-links');
    const res = await getMe();

    if (res.ok) {
        navLinks.innerHTML = `
            <span id="nav-user">Hola, ${res.data.nombre}</span>
            <a href="/alojamientos.html">Alojamientos</a>
            <a href="/mis-reservas.html">Mis reservas</a>
            ${res.data.rol === 'admin' ? '<a href="/admin.html">Admin</a>' : ''}
            <a href="#" onclick="doLogout()" class="btn-nav">Cerrar sesión</a>
        `;
    } else {
        navLinks.innerHTML = `
            <a href="/alojamientos.html">Alojamientos</a>
            <a href="/login.html" class="btn-nav">Iniciar sesión</a>
            <a href="/registro.html">Registrarse</a>
        `;
    }
}

async function doLogout() {
    await logout();
    window.location.href = '/';
}

// Mostrar alerta en formularios
function showAlert(id, message, type) {
    const el = document.getElementById(id);
    el.textContent = message;
    el.className = 'alert alert-' + type;
    el.style.display = 'block';
}

function hideAlert(id) {
    document.getElementById(id).style.display = 'none';
}
