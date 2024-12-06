async function changeContentToCameras() {
    const data = await getConnectedDevices();

    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = '';

    const deviceCardsContainer = document.createElement('div');
    deviceCardsContainer.classList.add('device-cards-container');

    if(data.length === 0) {
        const noDevices = document.createElement('div');
        noDevices.classList.add('no-devices');
        noDevices.textContent = 'No devices found';
        deviceCardsContainer.appendChild(noDevices);
        contentPanel.appendChild(deviceCardsContainer);
        return;
    }

    data.forEach(device => {

        const card1 = document.createElement('div');
        card1.classList.add('card');
        card1.innerHTML = `
            <div class="card-header">
                <span class="emoji">🎥</span>
                <h3>${device.ip}</h3>
            </div>
            <div class="card-buttons">
                <button onclick="window.open('http://${device.ip}', '_blank')">Camera</button>
                <button onclick="window.open('http://${device.ip_with_port}', '_blank')">DAUGHTER BOX</button>
            </div>
        `;
        deviceCardsContainer.appendChild(card1);
    });

    contentPanel.appendChild(deviceCardsContainer);
}
