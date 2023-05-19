from services.ServiceBase import ServiceBase
import requests
import re
from pydantic import BaseModel
from bs4 import BeautifulSoup
from typing import Type, Optional, List
import os
from main import app
from main import print_exception_details
from fastapi import Request, HTTPException
import traceback
import json

class SettingRequest(BaseModel):
    setting_name: str
    text: Optional[str]=None

class SettingResponse(BaseModel):
    text: Optional[str]=None
    status: str

class UserSettingsService(ServiceBase):
    def handle_request(self, request: SettingRequest) -> SettingResponse:
        status = "failes"
        return SettingResponse(text="Hello World", status="success")

class UserSettings:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        # Load settings from the JSON file into memory on startup
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                try:
                    self.settings = json.load(file)
                except json.JSONDecodeError:
                    print("Error: Could not decode JSON file.")

    def read_all(self):
        # Read all settings
        return self.settings

    def write(self, name, value):
        # Write a setting (name-value pair)
        self.settings[name] = value
        self.save_settings()

    def delete(self, name):
        # Delete a setting by name
        if name in self.settings:
            del self.settings[name]
            self.save_settings()

    def save_settings(self):
        # Save the current settings to the JSON file
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)

@app.post("/usersettings", summary="Retrieve a list of name value pairs of settings specific to the user.")
async def usersetting_main(request: SettingRequest, fastRequest: Request) -> SettingResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return UserSettingsService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")
    
@app.post("/user_setting_read", summary="Read the contents of a file")
async def fileread_main(request: FileBasicRequest, fastRequest: Request) -> FileBasicResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return FileReadService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/filewrite", summary="Write to a file")
async def filewrite_main(request: FileBasicRequest, fastRequest: Request) -> FileBasicResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return FileWriteService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/fileappend", summary="Append to a file")
async def fileappend_main(request: FileBasicRequest, fastRequest: Request) -> FileBasicResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return FileAppendService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/filedelete", summary="Delete a file")
async def filedelete_main(request: FileBasicRequest, fastRequest: Request) -> FileBasicResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return FileDeleteService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

