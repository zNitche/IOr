function closeFlashMessage(event) {
    const container = event.target.parentElement;

    if (container) {
        container.remove();
    } else {
        console.error("flash message container not found")
    }
}

function autoCloseFlashMessage(uuid) {
    const container = document.getElementById(`flash-message-${uuid}`);

    if (container) {
        setTimeout(() => {
            container.remove();
        }, 3000);
    }
}

function disableButtonById(buttonId) {
    const button = document.getElementById(buttonId);


    if (button) {
        button.disabled = true;
    }
}

function toggleElementVisibility(id, visible) {
    const element = document.getElementById(id);

    if (element) {
        if (visible) {
            element.classList.remove("d-none");
        } else {
            element.classList.add("d-none")
        }
    } else {
        console.warn("can't find element with id " + id);
    }
}

function toggleCollapsible(caller, id) {
    const element = document.getElementById(id);

    if (!element) {
        console.warn(`can't find element with id ${id}`);
        return;
    }

    if (element.classList.contains("collapsed")) {
        element.classList.remove("collapsed");
        caller.classList.add("expanded");
    }
    else {
        element.classList.add("collapsed")
        caller.classList.remove("expanded");
    }
}
