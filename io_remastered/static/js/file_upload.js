function setupFileUploadPage() {
    toggleElementVisibility("file-upload-error", false);
    toggleElementVisibility("file-upload-button", false);
    toggleElementVisibility("file-upload-progress-bar", false);
    toggleElementVisibility("file-upload-name", false);
}

function getInputFile() {
    const filesInput = document.getElementById("file-upload-input");

    if (filesInput.files.length > 0) {
        const file = filesInput.files[0];
        return file
    } else {
        return null;
    }
}

function handleUploadFileSelected() {
    toggleElementVisibility("file-upload-error", false);

    const file = getInputFile();

    if (file) {
        showUploadFileElements(file.name);
        toggleElementVisibility("file-upload-button", true);
    }
}

function showUploadFileElements(filename) {
    toggleElementVisibility("file-upload-name", true);

    const filenameElement = document.getElementById("file-upload-name");
    filenameElement.innerHTML = filename;
}

function showErrorMessage(message) {
    toggleElementVisibility("file-upload-error", true);

    const errorWrapper = document.getElementById("file-upload-error");
    errorWrapper.innerHTML = `upload has failed : ${message}!`;
}

function sendFile(upload_url, csrf_token) {
    const file = getInputFile();

    if (!file) {
        showErrorMessage("can't access selected file")
        return;
    }

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener("abort", (event) => handleSendFileError(event))
    xhr.upload.addEventListener("error", (event) => handleSendFileError(event))
    xhr.upload.addEventListener("timeout", (event) => handleSendFileError(event))

    xhr.upload.addEventListener("load", (event) => handleSendFileLoad(event))
    xhr.upload.addEventListener("loadend", (event) => handleSendFileLoadEnd(event))
    xhr.upload.addEventListener("loadstart", (event) => handleSendFileLoadStart(event))

    xhr.upload.addEventListener("progress", (event) => handleSendFileLoadProgress(event))

    xhr.open("POST", upload_url, true);

    xhr.setRequestHeader("X-File-Name", file.name);
    xhr.setRequestHeader("X-File-Size", file.size);
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.setRequestHeader("X-CSRF-TOKEN", csrf_token);

    xhr.send();
}

function handleSendFileError(event) {
    showErrorMessage(event.type)
}

function handleSendFileLoad(event) {

}

function handleSendFileLoadEnd(event) {

}

function handleSendFileLoadStart(event) {

}

function handleSendFileLoadProgress(event) {

}
