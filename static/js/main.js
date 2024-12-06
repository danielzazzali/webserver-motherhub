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

async function changeContentToWifi() {
    const data = await getApSsidAndPassword();

    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = '';

    const wifiSettingsContainer = document.createElement('div');
    wifiSettingsContainer.classList.add('wifi-settings-container');

    const title = document.createElement('h2');
    title.textContent = 'Wi-Fi Settings';
    wifiSettingsContainer.appendChild(title);

    const ssidInput = document.createElement('input');
    ssidInput.type = 'text';
    ssidInput.placeholder = 'SSID';
    ssidInput.value = data.ssid;
    wifiSettingsContainer.appendChild(ssidInput);

    const inputContainer = document.createElement('div');
    inputContainer.classList.add('input-container');

    const passwordInput = document.createElement('input');
    passwordInput.type = 'password';
    passwordInput.id = 'password-input';
    passwordInput.placeholder = 'Password';
    passwordInput.value = data.password;
    inputContainer.appendChild(passwordInput);

    const togglePassword = document.createElement('span');
    togglePassword.classList.add('toggle-password');
    togglePassword.textContent = '👁️';
    togglePassword.onclick = togglePasswordVisibility;
    inputContainer.appendChild(togglePassword);

    wifiSettingsContainer.appendChild(inputContainer);
    contentPanel.appendChild(wifiSettingsContainer);



    contentPanel.appendChild(wifiSettingsContainer);

}

function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password-input');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
}


async function shutdownAsync() {
    showConfirmation('Are you sure you want to shut down the system?', async () => {
        const response = await shutdownSystem();
        if (response.error) {
            console.error('Error:', response.error);
        } else {
            console.log(response.message);
        }
    });
}

async function rebootAsync() {
    showConfirmation('Are you sure you want to reboot the system?', async () => {
        const response = await rebootSystem();
        if (response.error) {
            console.error('Error:', response.error);
        } else {
            console.log(response.message);
        }
    });
}
