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


