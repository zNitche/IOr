def formatted_file_size(size: str):
    sizes = ["KB", "MB", "GB"]
    size_bytes = int(size)
    
    current_size = size_bytes

    for size in sizes:
        current_size = round(current_size / 1_000, 2)

        if current_size < 1000:
            return f"{current_size}{size}"

    return f"{size_bytes} B"
