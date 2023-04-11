from services.ServiceBase import ServiceBase
import requests
import re
from pydantic import BaseModel
from bs4 import BeautifulSoup

class WebScrapingRequest(BaseModel):
    url: str

class WebScrapingResponse(BaseModel):
    text: str

class WebScrapingService(ServiceBase):
    def handle_request(self, request: WebScrapingRequest) -> WebScrapingResponse:
        print(f"Downloading for {request.url}...")
        response = requests.get(request.url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        for script_tag in soup.find_all("script"):
            script_tag.decompose()
        for style_tag in soup.find_all("style"):
            style_tag.decompose()
        text = soup.get_text()
        while "\n" in text:
            text = text.replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        return WebScrapingResponse(text=text)

