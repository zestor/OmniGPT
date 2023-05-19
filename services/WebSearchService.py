from typing import List,Optional
from services.ServiceBase import ServiceBase
from models.api import WebSearchRequest
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
import re
from datetime import datetime
import pytz
from urllib.parse import unquote

class WebSearchRequest(BaseModel):
    query: str

class WebSearchResult(BaseModel):
    title: Optional[str]=None
    date: Optional[str]=None
    url: Optional[str]=None
    description: Optional[str]=None

class WebSearchResponse(BaseModel):
    results: List[WebSearchResult]

def strip_html_tags(html_string: str) -> str:
    #print(f"Stripping HTML tags from {html_string}...")
    html_tag_pattern = re.compile(r'<[^>]+>')
    text = html_tag_pattern.sub(' ', html_string)
    #print(f"text: {text}")
    return text

def is_valid_date(date_string: str) -> bool:
    # Define the expected date format
    date_format = "%b %d, %Y"
    
    try:
        datetime.strptime(date_string, date_format)
        # If parsing succeeds, the date_string matches the format
        return True
    except Exception:
        # If parsing fails, the date_string does not match the format
        return False
    
def search_google(query: str) -> WebSearchResponse:
    print(f"Searching Google for {query}...")
    base_url = "https://www.google.com/search"
    params = {
        "q": query,
        "hl": "en" 
    }
    response = requests.get(base_url, params=params)
    print(f"Response status code: {response.status_code}")
    print(f"Response length: {len(response.text)} characters")
    decoded_text = bytes(response.text, "utf-8").decode("unicode_escape")
    #print(f"Response text: {decoded_text}")
    soup = BeautifulSoup(decoded_text, "html.parser")
    results = []

    quick_answers = soup.find_all("div", class_="pkphOe")
    quick_answer = ""
    if len(quick_answers) >= 2:
        # Return the second div element (index 1)
        quick_answer += " " + strip_html_tags(quick_answers[1].decode_contents()) + " "
    while "  " in quick_answer:
        quick_answer = quick_answer.replace("  ", " ")
    #print(f"Quick Answer: {quick_answer}")
    utc_timezone = pytz.UTC
    current_utc_datetime = datetime.now(utc_timezone)
    quick_answer = f"{quick_answer} (Last updated: {current_utc_datetime})"
    webResult = WebSearchResult(title="Quick Answer", link=None, description=quick_answer)

    results.append(webResult)
    search_results = soup.find_all("div", class_="Gx5Zad")
    print(f"Found {len(search_results)} div search results.")
    for result in search_results:
        title = result.find("h3").text if result.find("h3") else None
        url = result.find("a")["href"] if result.find("a") else None
        if title and url:
            possibledate = result.find("span").text if result.find("span") else None
            date=None
            if is_valid_date(possibledate):
                date = possibledate
            url = url.replace("/url?q=", "")
            description = result.find("div", class_="DnJfK").text if result.find("div", class_="DnJfK") else ""
            description = strip_html_tags(description)
            #print(f"Title: {title} Link: {url} Description: {description}") 
            webResult = WebSearchResult(title=title, date=date, url=     unquote(url), description=description)
            results.append(webResult)
    return WebSearchResponse(results=results)

class WebSearchService(ServiceBase):
    def handle_request(self, request: WebSearchRequest) -> WebSearchResponse:
        results = search_google(request.query)
        return results
