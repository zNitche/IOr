const i18n = new I18n();


function setupFileUploadPage() {
    toggleElementVisibility("file-upload-message", false);
    toggleElementVisibility("file-upload-button", false);
    toggleElementVisibility("file-upload-progress-bar", false);
    toggleElementVisibility("file-upload-name", false);
    toggleElementVisibility("file-upload-target-directory", false);
}

function setupI18n(translationsStr) {
    const rawData = translationsStr.replaceAll("\'", '"');
    i18n.setTranslations(JSON.parse(rawData));
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
    toggleElementVisibility("file-upload-target-directory", false);
}

function handleUploadFileSelected() {
    toggleElementVisibility("file-upload-message", false);

    const file = getInputFile();

    if (file) {
        showUploadFileElements(file.name);
        toggleElementVisibility("file-upload-button", true);
        toggleElementVisibility("file-upload-target-directory", true);
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

    const messagePrefix = type === "success" ? "" : i18n.t("upload_has_failed");

    messageElement.innerHTML = `${messagePrefix}${message}!`;
}

async function sendFile(file_upload_preflight_url, upload_url, csrf_token) {
    const file = getInputFile();

    if (!file) {
        showMessage(i18n.t("cant_access_file"), "error");
        return;
    }

    handleSendFileLoadStart();

    const directorySelectElement = document.getElementById("target-directory-select");
    const targetDirectoryUUID = directorySelectElement?.value;

    try {
        const uploader = new FileChunksUploader(file, targetDirectoryUUID);
        const response = await uploader.uploadChunkedFile(upload_url, file_upload_preflight_url,
            csrf_token, handleSendFileLoadProgress);

        if (!response) {
            showMessage(i18n.t('no_response_from_server'), "error");
            return;
        }

        const resJson = await response.json()
        handleSendFileLoadEnd(resJson.message, response.status !== 200);
    } catch {
        handleSendFileLoadEnd(i18n.t('error_occured'), true);
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
    toggleElementVisibility("file-upload-target-directory", false);

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
