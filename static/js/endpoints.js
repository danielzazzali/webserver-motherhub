async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(`Request failed: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

async function getConnectedDevices() {
    return fetchWithErrorHandling(`/connected_devices`);
}

async function getApSsidAndPassword() {
    return fetchWithErrorHandling(`/ap_ssid_and_password`);
}

async function changeApSsid(newSsid) {
    return fetchWithErrorHandling(`/change_ap_ssid/${newSsid}`, {
        method: 'POST',
    });
}

async function changeApPassword(newPassword) {
    return fetchWithErrorHandling(`/change_ap_password/${newPassword}`, {
        method: 'POST',
    });
}


async function rebootSystem() {
    return fetchWithErrorHandling(`/reboot`, {
        method: 'POST'
    });
}

async function shutdownSystem() {
    return fetchWithErrorHandling(`/shutdown`, {
        method: 'POST'
    });
}

