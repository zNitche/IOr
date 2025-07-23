class FileChunksUploader {
    constructor(file, chunkSize = 10_000_000) {
        this.file = file;
        this.chunkSize = chunkSize;

        this.fileSize = file.size;
        this.fileName = file.name.substring(0, 64) // limit filename to 64 characters

        this.fileChunksCount = Math.ceil(this.fileSize / chunkSize);
    }

    getChunksRange() {
        return [...Array(this.fileChunksCount).keys()];
    }

    getFileChunk(chunkId) {
        const offset = chunkId * this.chunkSize;
        return this.file.slice(offset, offset + this.chunkSize);
    }

    async preflightRequest(url, csrf_token) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-Is-JS-Request": true,
                "X-File-Size": this.fileSize,
                "X-File-Name": this.fileName,
                "X-CSRF-TOKEN": csrf_token,
            },
        });

        return response;
    }

    async uploadChunkedFile(url, preflight_url, csrf_token, progressCallback) {
        const preflightResponse = await this.preflightRequest(preflight_url, csrf_token);

        if (!preflightResponse.ok) {
            return preflightResponse;
        }

        const preflightResponseJson = await preflightResponse.json();
        const fileUUID = preflightResponseJson.file_uuid;

        let response = null;

        const chunksRange = this.getChunksRange();

        for (const chunkId of chunksRange) {
            const chunkData = this.getFileChunk(chunkId);

            response = await this.uploadFileChunk(url, chunkData, fileUUID);

            progressCallback(chunkId + 1, chunksRange.length);

            if (!response.ok) {
                break;
            }
        }

        return response;
    }

    async uploadFileChunk(url, chunkData, fileUUID) {
        const response = await fetch(url, {
            method: "PUT",
            headers: {
                "X-Is-JS-Request": true,
                "X-File-UUID": fileUUID,
                "X-File-Name": this.fileName,
                "X-Is-Last-Chunk": chunkData.size < this.chunkSize ? 1 : 0,
            },
            body: chunkData
        });

        return response;
    }
}
