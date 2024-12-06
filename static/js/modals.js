function showConfirmation(message, onConfirm) {
    const modal = document.createElement('div');
    modal.id = 'confirmation-modal';
    modal.className = 'confirmation-modal';

    const card = document.createElement('div');
    card.classList.add('confirmation-card');

    const messageParagraph = document.createElement('p');
    messageParagraph.textContent = message;

    const buttonsDiv = document.createElement('div');
    buttonsDiv.classList.add('confirmation-buttons');

    const yesButton = document.createElement('button');
    yesButton.textContent = 'Yes';
    yesButton.onclick = function () {
        onConfirm();
        closeModal(modal);
    };

    const noButton = document.createElement('button');
    noButton.textContent = 'No';
    noButton.onclick = function () {
        closeModal(modal);
    };

    buttonsDiv.appendChild(yesButton);
    buttonsDiv.appendChild(noButton);
    card.appendChild(messageParagraph);
    card.appendChild(buttonsDiv);
    modal.appendChild(card);
    document.body.appendChild(modal);
}

function showSuccess(message) {
    const modal = document.createElement('div');
    modal.id = 'success-modal';
    modal.className = 'success-modal';

    const card = document.createElement('div');
    card.classList.add('success-card');

    const messageParagraph = document.createElement('p');
    messageParagraph.textContent = message;

    const buttonsDiv = document.createElement('div');
    buttonsDiv.classList.add('success-buttons');

    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.onclick = function () {
        closeModal(modal);
    };

    buttonsDiv.appendChild(closeButton);
    card.appendChild(messageParagraph);
    card.appendChild(buttonsDiv);
    modal.appendChild(card);
    document.body.appendChild(modal);
}

function showLoadingModal() {
    const modal = document.createElement('div');
    modal.id = 'loading-modal';
    modal.className = 'loading-modal';

    const container = document.createElement('div');
    container.classList.add('loading-container');

    const spinner = document.createElement('div');
    spinner.classList.add('spinner');

    const loadingText = document.createElement('p');
    loadingText.textContent = 'Loading...';

    container.appendChild(spinner);
    container.appendChild(loadingText);
    modal.appendChild(container);
    document.body.appendChild(modal);
}

function closeLoadingModal() {
    const modal = document.getElementById('loading-modal');
    if (modal && modal.parentNode) {
        modal.parentNode.removeChild(modal);
    }
}

function closeModal(modal) {
    if (modal && modal.parentNode) {
        modal.parentNode.removeChild(modal);
    }
}
