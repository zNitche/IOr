IMAGE_FILE = "image_file"
MEDIA_FILE = "media_file"
CODE_FILE = "code_file"
DOCUMENT_FILE = "document_file"


COMMON_FILES_EXTENSIONS = {
    ".jpg": IMAGE_FILE,
    ".jpeg": IMAGE_FILE,
    ".png": IMAGE_FILE,
    ".gif": IMAGE_FILE,
    ".tiff": IMAGE_FILE,
    ".tif": IMAGE_FILE,
    ".bmp": IMAGE_FILE,
    ".svg": IMAGE_FILE,
    ".webp": IMAGE_FILE,

    ".mp3": MEDIA_FILE,
    ".wav": MEDIA_FILE,
    ".mp4": MEDIA_FILE,
    ".avi": MEDIA_FILE,
    ".mov": MEDIA_FILE,
    ".webm": MEDIA_FILE,
    ".mkv": MEDIA_FILE,
    ".ogg": MEDIA_FILE,

    ".txt": DOCUMENT_FILE,
    ".doc": DOCUMENT_FILE,
    ".docx": DOCUMENT_FILE,
    ".pdf": DOCUMENT_FILE,
    ".odt": DOCUMENT_FILE,
    ".xls": DOCUMENT_FILE,
    ".xlsx": DOCUMENT_FILE,
    ".ods": DOCUMENT_FILE,
    ".rtf": DOCUMENT_FILE,

    ".html": CODE_FILE,
    ".css": CODE_FILE,
    ".js": CODE_FILE,
    ".ts": CODE_FILE,
    ".tsx": CODE_FILE,
    ".jsx": CODE_FILE,
    ".py": CODE_FILE,
    ".c": CODE_FILE,
    ".cpp": CODE_FILE,
    ".cs": CODE_FILE,
    ".rs": CODE_FILE,
    ".xml": CODE_FILE,
    ".toml": CODE_FILE,
    ".json": CODE_FILE,
    ".yaml": CODE_FILE,
    ".yml": CODE_FILE,
}


WEB_PREVIEW_MIMETYPE_FOR_FILE_EXTENSION = {
    ".jpg": "image/jpg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".tiff": "image/tiff",
    ".tif": "image/tif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",

    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
    ".flac": "audio/flac",
    ".mov": "video/quicktime"
}
