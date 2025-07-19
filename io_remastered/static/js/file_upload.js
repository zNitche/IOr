function handleUploadFileSelected(event) {
    const filesInput = event.currentTarget;

    if (filesInput.files.length === 1) {
        const file = filesInput.files[0];
        const fileName = file.name;
        const fileSize = file.size;

        showUploadFileElements(fileName);
    }
}

function showUploadFileElements(filename) {
    const filenameElement = document.getElementById("file-upload-name");
    filenameElement.style.display = "block";
    filenameElement.innerHTML = filename;

    const uploadButton = document.getElementById("file-upload-button");
    uploadButton.style.display = "block";
}
