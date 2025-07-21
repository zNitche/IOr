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
    filesInputElement.value = '';

    fileNameElement.innerHTML = "";

    toggleElementVisibility("file-upload-name", false);
    toggleElementVisibility("file-upload-button", false);
}

function handleUploadFileSelected() {
    toggleElementVisibility("file-upload-message", false);

    const file = getInputFile();

    if (file) {
        showUploadFileElements(file.name);
        toggleElementVisibility("file-upload-button", true);
    } else {
        clearFileInput();
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

async function sendFile(upload_preflight_url, upload_url, csrf_token) {
    const file = getInputFile();

    if (!file) {
        showMessage("can't access selected file", "error");
        return;
    }

    // it seems xhr can't be aborted midflight via backend response, so let's do a preflight request]
    await fileUploadPreflight(upload_preflight_url, file, csrf_token);

    // setup XHR
    const xhr = new XMLHttpRequest();

    xhr.addEventListener("abort", handleSendFileError);
    xhr.addEventListener("error", handleSendFileError);
    xhr.addEventListener("timeout", handleSendFileError);

    xhr.addEventListener("loadend", handleSendFileLoadEnd);
    xhr.addEventListener("loadstart", handleSendFileLoadStart);

    xhr.upload.addEventListener("progress", (event) => handleSendFileLoadProgress(event));

    xhr.open("POST", upload_url, true);

    xhr.setRequestHeader("X-Is-JS-Request", true);
    xhr.setRequestHeader("X-CSRF-TOKEN", csrf_token);
    xhr.setRequestHeader("X-File-Name", file.name);
    xhr.setRequestHeader("X-File-Size", file.size);
    xhr.setRequestHeader("Content-Type", file.type);

    xhr.send(file);
}

async function fileUploadPreflight(preflight_url, file, csrf_token) {
    const preflightResponse = await fetch(preflight_url, {
        method: "POST",
        headers: {
            "X-Is-JS-Request": true,
            "X-CSRF-TOKEN": csrf_token,
            "X-File-Size": file.size,
        }
    });

    if (!preflightResponse.ok) {
        const responseJson = await preflightResponse.json();

        showMessage(responseJson.message, "error");
        clearFileInput();

        throw new Error(responseJson.message)
    }
}

function handleSendFileError(event) {
    showMessage(event.type, "error")
}

function handleSendFileLoadEnd(event) {
    toggleElementVisibility("file-upload-progress-bar", false);

    const response = getXHRResponse(event.currentTarget);

    showMessage(response.message, response.status !== 200 ? "error" : "success");

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
