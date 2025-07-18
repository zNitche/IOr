function closeFlashMessage(event) {
    const container = event.target.parentElement;

    if (container) {
        container.remove();
    } else {
        console.error("flash message container not found")
    }
}

function disableButtonById(buttonId) {
    const button = document.getElementById(buttonId);


    if (button) {
        button.disabled = true;
    }
}

