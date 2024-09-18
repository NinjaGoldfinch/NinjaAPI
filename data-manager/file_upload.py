# From https://github.com/NinjaGoldfinch/api-file-manager/blob/main/file_upload_manager.py

import requests
import json

class FileUploadManager:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filesToUpload = []
        
    def addFile(self, filename: str, content) -> None:
        self.filesToUpload.append((filename, content))
        
    def uploadFiles(self) -> None:
        files = {}
        
        for filename, content in self.filesToUpload:
            if isinstance(content, str):
                files[filename] = (filename, content)
            elif isinstance(content, dict):
                files[filename] = (filename, json.dumps(content))
        
        response = requests.post(self.url, files=files)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to upload files")
    
    def uploadFile(self, filename: str, content) -> None:
        files = {}
        
        if isinstance(content, str):
            files[filename] = (filename, content)
        elif isinstance(content, dict):
            files[filename] = (filename, json.dumps(content))
        
        response = requests.post(self.url, files=files)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to upload file")
            
    def deleteFiles(self, filenames: list) -> None:
        response = requests.delete(self.url, params={'filenames': filenames})
        
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)