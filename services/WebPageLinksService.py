from typing import List, Optional
from services.ServiceBase import ServiceBase
import requests
import re
from pydantic import BaseModel
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebPageLinksRequest(BaseModel):
    url: str

class WebPageLink(BaseModel):
    title: Optional[str]=None
    url: str

class WebPageLinksResponse(BaseModel):
    results: List[WebPageLink]

def get_absolute_url(host, path):
    # Use urljoin to combine the host and path to create an absolute URL
    absolute_url = urljoin(host, path)
    return absolute_url

class WebPageLinksService(ServiceBase):
    def handle_request(self, request: WebPageLinksRequest) -> WebPageLinksResponse:
        print(f"Downloading for {request.url}...")
        response = requests.get(request.url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        for link in soup.find_all("a"):
            link_text = link.text
            while "\n" in link_text:
                link_text = link_text.replace("\n", " ")
            while "  " in link_text:
                link_text = link_text.replace("  ", " ")
            link_text = link_text.strip()
            links.append(WebPageLink(url=get_absolute_url(request.url,link.get("href","")), title=link_text))
        return WebPageLinksResponse(results=links[:30])

