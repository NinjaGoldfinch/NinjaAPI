import os

def list_files(directory):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return None

    files = []
    for root, dirs, filenames in os.walk(directory):
        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            file_count = sum([len(files) for r, d, files in os.walk(dir_path)])
            files.append({'name': dirname, 'type': 'directory', 'file_count': file_count})
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append({'name': filename, 'type': 'file'})
        break  # Only process the top-level directory

    return {'success': 'true', 'files': files}

def download_file(file_path):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            return {'error': 'Requested path is a directory'}
        
        return file_path
    
    return {'error': 'File not found'}

async def upload_file(file_content, directory):
    print(f"Received {len(file_content)} files")
    files_written = []
    
    for filename, file_contents in file_content.items():
        file_path = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:      
            f_cont = await file_contents.read()
            f.write(f_cont)
            files_written.append(filename)
            
    return files_written

def remove_file(directory, filenames):
    if not filenames:
        return {'error': 'No filenames provided'}
    
    deleted_files = []
    errors = []
    
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        
        if not os.path.exists(file_path):
            errors.append({'filename': filename, 'error': 'File not found'})
            continue
        
        try:
            if os.path.isdir(file_path):
                os.rmdir(file_path)
            else:
                os.remove(file_path)
            deleted_files.append(filename)
        except Exception as e:
            errors.append({'filename': filename, 'error': str(e)})
    
    return {'success': True, 'deleted': deleted_files, 'errors': errors}