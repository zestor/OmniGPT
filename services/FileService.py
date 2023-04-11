from services.ServiceBase import ServiceBase
import requests
import re
from pydantic import BaseModel
from bs4 import BeautifulSoup
from typing import Optional, List
import os

FILES_ROOT = "./files"

class FileBasicRequest(BaseModel):
    filename: str
    text: Optional[str]=None

class FileBasicResponse(BaseModel):
    text: Optional[str]=None
    status: str

class FileSearchRequest(BaseModel):
    search_text: str

class FileSearchResponse(BaseModel):
    filenames: Optional[List[str]]=None

def create_path_to_file(file_path):
    file_path=join_and_create_absolute_path(FILES_ROOT, file_path)
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def join_and_create_absolute_path(path1, path2):
    joined_path = os.path.join(path1, path2)
    absolute_path = os.path.abspath(joined_path)
    return absolute_path    

def read_file(file_path):
    file_path=join_and_create_absolute_path(FILES_ROOT, file_path)
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(file_path, content) -> bool:
    try:
        file_path=join_and_create_absolute_path(FILES_ROOT, file_path)
        create_path_to_file(file_path)
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        return False

def append_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content)

def delete_file(file_path):
    file_path=join_and_create_absolute_path(FILES_ROOT, file_path)
    print(f"Deleting file: {file_path}")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

def search_text_in_files(directory, search_text) -> List[str]:
    print(f"Searching for {search_text} in {directory}")
    filenames = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            print(f"Searching in file: {file_name}")
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    if search_text in file_content:
                        filenames.append(file_path)
                        print(f"Text found in file: {file_path}")
                    else:
                        print(f"Text not found in file: {file_path}")
            except Exception as e:
                print(f"Error reading file: {file_path}. Error: {e}")
    return filenames

class FileReadService(ServiceBase):
    def handle_request(self, request: FileBasicRequest) -> FileBasicResponse:
        status = "failed"
        text = None
        file_path=join_and_create_absolute_path(FILES_ROOT, request.filename)
        if os.path.exists(file_path):
            text = read_file(file_path)
            status = "success"
        return FileBasicResponse(text=text, status=status)
    
class FileWriteService(ServiceBase):
    def handle_request(self, request: FileBasicRequest) -> FileBasicResponse:
        status = "failed"
        if write_file(request.filename, request.text):
            status = "success"
        return FileBasicResponse(status=status)
    
class FileAppendService(ServiceBase):
    def handle_request(self, request: FileBasicRequest) -> FileBasicResponse:
        status = "failed"
        file_path=join_and_create_absolute_path(FILES_ROOT, request.filename)
        if os.path.exists(file_path):
            text = append_file(file_path, request.text)
            status = "success"
        return FileBasicResponse(status=status)

class FileDeleteService(ServiceBase):
    def handle_request(self, request: FileBasicRequest) -> FileBasicResponse:
        status = "failed"
        file_path=join_and_create_absolute_path(FILES_ROOT, request.filename)
        if os.path.exists(file_path):
            delete_file(file_path)
            status = "success"
        return FileBasicResponse(status=status)
    
class FileSearchService(ServiceBase):
    def handle_request(self, request: FileSearchRequest) -> FileSearchResponse:
        status = "failed"
        files = search_text_in_files(FILES_ROOT, request.search_text)
        if len(files) > 0:
            status = "success"
        return FileSearchResponse(filenames=files, status=status)