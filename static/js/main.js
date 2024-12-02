async function changeContentToCameras() {

    const data = await getConnectedDevices();

    const contentPanel = document.getElementById('content-panel');

    contentPanel.innerHTML = '';

    const deviceCardsContainer = document.createElement('div');
    deviceCardsContainer.classList.add('device-cards-container');

    data.forEach(device => {

        const card1 = document.createElement('div');
        card1.classList.add('card');
        card1.innerHTML = `
            <div class="card-header">
                <span class="emoji">🎥</span>
                <h3>Camera: ${device.ip}</h3>
            </div>
            <button onclick="window.open('http://${device.ip}', '_blank')">Camera</button>
        `;
        deviceCardsContainer.appendChild(card1);

        const card2 = document.createElement('div');
        card2.classList.add('card');
        card2.innerHTML = `
            <div class="card-header">
                <span class="emoji">💻</span>
                <h3>DaughterBox: ${device.ip}</h3>
            </div>
            <button onclick="window.open('http://${device.ip_with_port}', '_blank')">DaughterBox</button>
        `;
        deviceCardsContainer.appendChild(card2);
    });

    contentPanel.appendChild(deviceCardsContainer);
}

function changeContentToWifi() {
    document.getElementById('content-panel').textContent = "Wi-fi";
}

function refreshPage() {
    alert('Refreshing page...');
}


