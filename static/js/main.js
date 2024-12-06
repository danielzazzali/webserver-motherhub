async function shutdownAsync() {
    showConfirmation('Are you sure you want to shut down the system?', async () => {
        closeModal(document.getElementById('confirmation-modal'));
        showLoadingModal();
        shutdownSystem().then(response => {
            if (response.error) {
                console.error('Error:', response.error);
            } else {
                console.log(response.message);
            }
        });
    });
}

async function rebootAsync() {
    showConfirmation('Are you sure you want to reboot the system?', async () => {
        closeModal(document.getElementById('confirmation-modal'));
        showLoadingModal();
        rebootSystem().then(response => {
            if (response.error) {
                console.error('Error:', response.error);
            } else {
                console.log(response.message);
            }
        });
    });
}