document.addEventListener('DOMContentLoaded', () => {
    const panels = {
        mode: document.getElementById('mode-panel'),
        devices: document.getElementById('devices-panel'),
        wifi: document.getElementById('wifi-panel'),
    };

    const buttons = {
        mode: document.getElementById('btn-mode'),
        devices: document.getElementById('btn-devices'),
        wifi: document.getElementById('btn-wifi'),
    };

    const togglePanel = (panel) => {
        Object.values(panels).forEach(p => p.classList.add('hidden'));
        panels[panel].classList.remove('hidden');
    };

    buttons.mode.addEventListener('click', () => togglePanel('mode'));
    buttons.devices.addEventListener('click', () => togglePanel('devices'));
    buttons.wifi.addEventListener('click', () => togglePanel('wifi'));

    // Fetch mode
    fetch('/mode')
        .then(res => res.json())
        .then(data => document.getElementById('current-mode').textContent = data.mode)
        .catch(err => console.error('Error fetching mode:', err));

    document.getElementById('set-mode-btn').addEventListener('click', () => {
        const newMode = document.getElementById('new-mode').value;
        fetch('/mode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: newMode })
        })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(err => console.error('Error setting mode:', err));
    });

    // Fetch connected devices
    buttons.devices.addEventListener('click', () => {
        fetch('/devices')
            .then(res => res.json())
            .then(devices => {
                const deviceList = document.getElementById('device-list');
                deviceList.innerHTML = devices.map(d => `<p>${d}</p>`).join('');
            })
            .catch(err => console.error('Error fetching devices:', err));
    });

    // Fetch WiFi info
    fetch('/ap_info')
        .then(res => res.json())
        .then(data => {
            document.getElementById('wifi-ssid').textContent = data.ssid;
            document.getElementById('wifi-password').value = data.password;
        })
        .catch(err => console.error('Error fetching WiFi info:', err));

    // Toggle password visibility
    document.getElementById('toggle-password').addEventListener('click', () => {
        const passwordInput = document.getElementById('wifi-password');
        passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    });

    // Change SSID
    document.getElementById('change-ssid-btn').addEventListener('click', () => {
        const newSSID = document.getElementById('new-ssid').value;
        fetch(`/change_ssid/${newSSID}`, { method: 'POST' })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(err => console.error('Error changing SSID:', err));
    });

    // Change Password
    document.getElementById('change-password-btn').addEventListener('click', () => {
        const newPassword = document.getElementById('new-password').value;
        fetch(`/change_password/${newPassword}`, { method: 'POST' })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(err => console.error('Error changing password:', err));
    });
});
