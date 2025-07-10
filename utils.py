import os
import zipfile
import shutil

SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.heic', '.heif')
MAX_SIZE_MB = 3072
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def filter_large_files(uploaded_files, st=None):
    filtered = []
    for f in uploaded_files:
        f.seek(0, 2)
        size = f.tell()
        f.seek(0)
        if size > MAX_SIZE_BYTES:
            if st:
                st.error(f"Файл {f.name} превышает {MAX_SIZE_MB} МБ и не будет обработан.")
        else:
            filtered.append(f)
    return filtered

def safe_extract(zip_ref, path):
    """Извлекает файлы из архива zip_ref в path, предотвращая path traversal."""
    for member in zip_ref.namelist():
        member_path = os.path.abspath(os.path.join(path, member))
        if not member_path.startswith(os.path.abspath(path)):
            raise Exception(f"Path traversal attempt: {member}")
        zip_ref.extract(member, path)

def cleanup_temp_files(temp_dir):
    """Удаляет временную директорию после обработки."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)