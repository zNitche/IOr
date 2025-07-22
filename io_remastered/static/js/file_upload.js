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

async function sendFile(file_upload_preflight_url, upload_url, csrf_token) {
    const file = getInputFile();

    if (!file) {
        showMessage("can't access selected file", "error");
        return;
    }

    handleSendFileLoadStart();

    try {
        const uploader = new FileChunksUploader(file);
        const response = await uploader.uploadChunkedFile(upload_url, file_upload_preflight_url,
             csrf_token, handleSendFileLoadProgress);

        if (!response) {
            showMessage("no response from server", "error");
            return;
        }

        const resJson = await response.json()
        handleSendFileLoadEnd(resJson.message, response.status !== 200);
    } catch {
        handleSendFileLoadEnd("an error has occured", true);
    }
}

function handleSendFileLoadEnd(message, isError) {
    toggleElementVisibility("file-upload-progress-bar", false);
    showMessage(message, isError ? "error" : "success");

    clearFileInput();
}

function handleSendFileLoadStart() {
    toggleElementVisibility("file-upload-message", false);
    toggleElementVisibility("file-upload-progress-bar", true);
    toggleElementVisibility("file-upload-button", false);

    setUploadProgressDetials(0);
}

function handleSendFileLoadProgress(current, total) {
    const currentProgress = (current * 100 / total).toFixed(2);

    setUploadProgressDetials(currentProgress);
}

function setUploadProgressDetials(progress) {
    const progressBar = document.getElementById("file-upload-progress");
    const progressText = document.getElementById("file-upload-progress-text");

    progressBar.style.width = `${progress}%`;
    progressText.innerHTML = `${progress}%`;
}
