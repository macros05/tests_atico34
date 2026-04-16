const API_URL = 'http://127.0.0.1:8000';

async function cargarDatos() {
    const res = await fetch(`${API_URL}/historial_clientes`);
    const datos = await res.json();

    document.getElementById('total').textContent = datos.length;
    document.getElementById('pendientes').textContent = datos.filter(d => !d.revisado_por_humano).length;
    document.getElementById('revisados').textContent = datos.filter(d => d.revisado_por_humano).length;

    const tbody = document.getElementById('tabla');
    tbody.innerHTML = datos.map(d => `
        <tr>
            <td>${d.cliente_id}</td>
            <td>${d.cliente_nombre}</td>
            <td>${d.comercial_asignado}</td>
            <td>${d.timestamp.replace('T', ' ').substring(0, 19)}</td>
            <td class="${d.revisado_por_humano ? 'revisado' : 'pendiente'}">
                ${d.revisado_por_humano
                    ? 'Revisado'
                    : `<button class="btn-aprobar" onclick="revisarCliente('${d.cliente_id}')">✅ Aprobar</button>`
                }
            </td>
        </tr>
    `).join('');
}

async function revisarCliente(clienteId) {
    await fetch(`${API_URL}/revisar_cliente/${clienteId}`, {
        method: 'POST'
    });
    cargarDatos();
}

cargarDatos();
setInterval(cargarDatos, 5000);