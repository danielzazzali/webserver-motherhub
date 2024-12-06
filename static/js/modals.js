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
        closeConfirmation(modal);
    };

    const noButton = document.createElement('button');
    noButton.textContent = 'No';
    noButton.onclick = function () {
        closeConfirmation(modal);
    };

    buttonsDiv.appendChild(yesButton);
    buttonsDiv.appendChild(noButton);
    card.appendChild(messageParagraph);
    card.appendChild(buttonsDiv);
    modal.appendChild(card);
    document.body.appendChild(modal);
}

function closeConfirmation(modal) {
    document.body.removeChild(modal);
}