
function changeContent(content) {
    document.getElementById('content-panel').textContent = content;
}

function refreshPage() {
    alert('Refreshing page...');
}

function reboot() {
    alert('Rebooting system...');
}

function shutdown() {
    alert('Shutting down...');
}

function initializePage() {
    changeContent('Contenido de Cámaras');
}

async function loadExternalContent(url) {
    try {
        // Hacer una solicitud fetch para cargar el contenido HTML del template
        const response = await fetch(url);
        const html = await response.text();

        // Insertar el contenido cargado en el panel
        const contentPanel = document.getElementById('content-panel');
        contentPanel.innerHTML = ''; // Limpiar contenido actual
        contentPanel.innerHTML = html; // Insertar nuevo contenido
    } catch (error) {
        console.error('Error al cargar el contenido:', error);
    }
}
