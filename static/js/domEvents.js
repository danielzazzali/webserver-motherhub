document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cameras-tab').addEventListener('click', () => changeContent('cameras-tab'));
    document.getElementById('wifi-tab').addEventListener('click', () => changeContent('wifi-tab'));
});

async function changeContent(activeButtonId) {

    const buttons = document.querySelectorAll('.sidebar button');
    buttons.forEach(button => button.classList.remove('active'));
    document.getElementById(activeButtonId).classList.add('active');

    showLoading();

    if (activeButtonId === 'cameras-tab') {
        await changeContentToCameras()
    } else if (activeButtonId === 'wifi-tab') {
        await changeContentToWifi()
    }
}

function showLoading() {
    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = `
        <div class="loading-container">
            <div class="spinner"></div>
            <p>Loading, please wait...</p>
        </div>
    `;
}