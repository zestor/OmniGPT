# This is a version of the main.py file found in ../../../server/main.py for testing the plugin locally.
# Use the command `poetry run dev` to run this.
from typing import Type, Optional
import json 
from enum import Enum
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from UnicornAPI import UnicornAPI

from services.ServiceBase import ServiceBase
from services.DateTimeService import DateTimeService, DateTimeResponse
from services.WebSearchService import WebSearchService, WebSearchRequest, WebSearchResponse
from services.WebScrapingService import WebScrapingService, WebScrapingRequest, WebScrapingResponse
from services.WebPageLinksService import WebPageLinksService, WebPageLinksRequest, WebPageLinksResponse
from services.FileService import FileReadService, FileWriteService, FileAppendService, FileDeleteService, FileSearchService, FileBasicRequest, FileBasicResponse, FileSearchRequest, FileSearchResponse

def print_exception_details(exc: Exception):
    # Print the type of the exception
    print(f"Exception type: {type(exc).__name__}")

    # Print the exception message (also known as the exception's "args")
    print(f"Exception message: {exc}")

    # Print the full traceback, including the call stack and exception details
    print("Exception traceback:")
    traceback.print_tb(exc.__traceback__)

class Services(Enum):
    DateTime = "datetime"
    WebSearch = "websearch"

app = FastAPI(title="OmniGPT", description="OmniGPT is a comprehensive toolkit that enhances ChatGPT's capabilities by providing a wide range of tools and utilities for tasks that go beyond language understanding. With OmniGPT, ChatGPT can perform tasks such as web search, web scraping, gpt agent, file operations, database operations, python code execution, news retrieval, stock market information, cryptocurrency information, event calendar, and much more. OmniGPT transforms ChatGPT into a multi-talented digital assistant, ready to tackle creative challenges and automate complex tasks.", version="v1", servers=[{"url": "http://localhost:3000"}])

PORT = 3000

origins = [
    f"http://localhost:{PORT}",
    "https://chat.openai.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.route("/.well-known/ai-plugin.json")
async def get_manifest(request):
    file_path = "./ai-plugin.json"
    return FileResponse(file_path, media_type="text/json")

@app.route("/logo.png")
async def get_logo(request):
    file_path = "./logo.png"
    return FileResponse(file_path, media_type="image/png")

@app.route("/openapi.yaml")
async def get_openapi(request):
    file_path = "./openapi.yaml"
    return FileResponse(file_path, media_type="text/plain")

@app.get("/datetime", summary="Get the current date and time")
async def datetime_main(fastrequest: Request) -> DateTimeResponse:
    try:
        return DateTimeService().handle_request()
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/websearch", summary="Search Google and Return the Top Short Web Result and Top 10 Web Links (Title, Date, Url, Description)")
async def websearch_main(request: WebSearchRequest, fastRequest: Request) -> WebSearchResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return WebSearchService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/webscraping", summary="Retrieve a web page, remove all HTML tags, and retrieve only the text")
async def websearch_main(request: WebScrapingRequest, fastRequest: Request) -> WebScrapingResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return WebScrapingService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/webpagelinks", summary="Get all hyperlink anchor tags (Title, url) from a web page")
async def websearch_main(request: WebPageLinksRequest, fastRequest: Request) -> WebPageLinksResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return WebPageLinksService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

@app.post("/fileread", summary="Read the contents of a file")
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

@app.post("/filesearch", summary="Search for text in all files")
async def filesearch_main(request: FileSearchRequest, fastRequest: Request) -> FileSearchResponse:
    try:
        if fastRequest.headers:
            print(f"request headers: {fastRequest.headers}")
        return FileSearchService().handle_request(request)
    except Exception as e:
        print_exception_details(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")
    
"""
@app.on_event("startup")
async def startup():
    return None
"""

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=PORT, reload=True)
