function setupFileUploadPage() {
    toggleElementVisibility("file-upload-message", false);
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

function clearFileInput() {
    const filesInputElement = document.getElementById("file-upload-input");
    const fileNameElement = document.getElementById("file-upload-name");

    filesInputElement.file = null;
    fileNameElement.innerHTML = "";

    toggleElementVisibility("file-upload-name", false);
}

function handleUploadFileSelected() {
    toggleElementVisibility("file-upload-message", false);

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

function showMessage(message, type) {
    toggleElementVisibility("file-upload-message", true);

    const messageElement = document.getElementById("file-upload-message");

    messageElement.classList.remove("error");
    messageElement.classList.remove("success");

    messageElement.classList.add(type);

    const messagePrefix = type === "success" ? "" : "upload has failed: ";

    messageElement.innerHTML = `${messagePrefix}${message}!`;
}

function sendFile(upload_url, csrf_token) {
    const file = getInputFile();

    if (!file) {
        showMessage("can't access selected file", "error")
        return;
    }

    const xhr = new XMLHttpRequest();

    xhr.addEventListener("abort", handleSendFileError)
    xhr.addEventListener("error", handleSendFileError)
    xhr.addEventListener("timeout", handleSendFileError)

    xhr.addEventListener("loadend", handleSendFileLoadEnd)
    xhr.addEventListener("loadstart", handleSendFileLoadStart)

    xhr.addEventListener("progress", handleSendFileLoadProgress)

    xhr.open("POST", upload_url, true);

    xhr.setRequestHeader("X-Is-JS-Request", true);
    xhr.setRequestHeader("X-File-Name", file.name);
    xhr.setRequestHeader("X-File-Size", file.size);
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.setRequestHeader("X-CSRF-TOKEN", csrf_token);

    xhr.send();
}

function handleSendFileError(event) {
    showMessage(event.type, "error")
}

function handleSendFileLoadEnd(event) {
    toggleElementVisibility("file-upload-progress-bar", false);

    const response = getXHRResponse(event.currentTarget);

    if (response.status !== 200) {
        showMessage(response.message, "error");
    } else {
        showMessage("file has been uploaded successfully", "success");
    }

    clearFileInput();
}

function handleSendFileLoadStart(event) {
    toggleElementVisibility("file-upload-message", false);
    toggleElementVisibility("file-upload-progress-bar", true);
    toggleElementVisibility("file-upload-button", false);

    setUploadProgressDetials(0);
}

function handleSendFileLoadProgress(event) {
    const currentProgress = ((event.loaded / event.total) * 100).toFixed(2);

    setUploadProgressDetials(currentProgress);
}

function setUploadProgressDetials(progress) {
    const progressBar = document.getElementById("file-upload-progress");
    const progressText = document.getElementById("file-upload-progress-text");

    progressBar.style.width = `${progress}%`;
    progressText.innerHTML = `${progress}%`;
}

function getXHRResponse(request) {
    const response = JSON.parse(request.responseText);
    const status = request.status;

    return {
        message: response.message,
        status,
    };
}
