// Function to get connected devices
async function getConnectedDevices() {
    try {
        const response = await fetch(`/connected_devices`);
        if (response.ok) {
            const data = await response.json();
            return data; // Return the connected devices
        } else {
            throw new Error('Error getting connected devices');
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

// Function to get the SSID and password of the AP
async function getApSsidAndPassword() {
    try {
        const response = await fetch(`/ap_ssid_and_password`);
        if (response.ok) {
            const data = await response.json();
            return data; // Return the AP SSID and password
        } else {
            throw new Error('Error getting SSID and password');
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

// Function to change the SSID of the AP
async function changeApSsid(newSsid) {
    try {
        const response = await fetch(`/change_ap_ssid/${newSsid}`, {
            method: 'POST',
        });
        if (response.ok) {
            const data = await response.json();
            return data; // Return success message
        } else {
            throw new Error('Error changing SSID');
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

// Function to change the password of the AP
async function changeApPassword(newPassword) {
    try {
        const response = await fetch(`/change_ap_password/${newPassword}`, {
            method: 'POST',
        });
        if (response.ok) {
            const data = await response.json();
            return data; // Return success message
        } else {
            throw new Error('Error changing password');
        }
    } catch (error) {
        console.error("Error:", error);
        return { error: error.message };
    }
}

export { getConnectedDevices, getApSsidAndPassword, changeApSsid, changeApPassword };
