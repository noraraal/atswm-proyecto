// Base URL de la API (detecta si estamos bajo /reservas/ en producción)
const BASE = window.location.pathname.startsWith('/reservas') ? '/reservas' : '';
const API = BASE + '/api/v1';

// --- Utilidades ---

async function request(method, path, body = null) {
    const opts = {
        method: method,
        credentials: 'same-origin',
        headers: {}
    };
    if (body) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(body);
    }
    const res = await fetch(API + path, opts);
    const data = res.status !== 204 ? await res.json() : null;
    return { ok: res.ok, status: res.status, data: data };
}

// --- Auth ---

async function registro(nombre, email, password) {
    return request('POST', '/auth/registro', { nombre, email, password });
}

async function login(email, password) {
    return request('POST', '/auth/login', { email, password });
}

async function logout() {
    return request('POST', '/auth/logout');
}

async function getMe() {
    return request('GET', '/usuarios/me');
}

// --- Alojamientos ---

async function getAlojamientos(filtros = {}) {
    const params = new URLSearchParams();
    if (filtros.ciudad) params.set('ciudad', filtros.ciudad);
    if (filtros.tipo) params.set('tipo', filtros.tipo);
    if (filtros.huespedes) params.set('huespedes', filtros.huespedes);
    const query = params.toString() ? '?' + params.toString() : '';
    return request('GET', '/alojamientos' + query);
}

async function getAlojamiento(id) {
    return request('GET', '/alojamientos/' + id);
}

// --- Reservas ---

async function crearReserva(alojamientoId, fechaEntrada, fechaSalida, numHuespedes) {
    return request('POST', '/reservas', {
        alojamiento_id: alojamientoId,
        fecha_entrada: fechaEntrada,
        fecha_salida: fechaSalida,
        num_huespedes: numHuespedes
    });
}

async function getMisReservas() {
    return request('GET', '/reservas');
}

async function cancelarReserva(id) {
    return request('PATCH', '/reservas/' + id, { estado: 'cancelada' });
}
