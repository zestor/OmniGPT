from services.ServiceBase import ServiceBase
import requests
import re
from pydantic import BaseModel
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import threading
import concurrent.futures
#import undetected_chromedriver as uc
import time
from urllib.parse import unquote, urlparse, parse_qs, urlencode, urlunparse


class WebScrapingRequest(BaseModel):
    url: str

class WebScrapingResponse(BaseModel):
    text: str

class WebScrapingService(ServiceBase):

    #driver = None

    def __init__(self):
        print(f"Starting Chrome Driver")
        options = ChromeOptions()
        options.add_argument("no-sandbox")
        #options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

        #service = ChromeService(executable_path='./chromedriver')
        #self.driver = webdriver.Chrome(service=service)

    def set_language_parameter(self, url, language='en'):
        url_components = urlparse(url)
        query_params = parse_qs(url_components.query)
        if 'language' in query_params:
            query_params['language'] = [language]
            updated_query = urlencode(query_params, doseq=True)
            updated_url = urlunparse(
                (url_components.scheme, url_components.netloc, url_components.path,
                url_components.params, updated_query, url_components.fragment)
            )
            return updated_url
        return url
    
    def download_web_page(self,url)->str:
        url = self.set_language_parameter(url, language='en')
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "article-title")]')))
        except Exception as e:
            print(f"Timeout waiting for h1 article-title: {e}")
            pass
        # Get the HTML content of the web page, likely nothing useful here
        main_page_html = self.driver.page_source
        # Set a variable to store the frames HTML content
        retval = ''
        print(f'HTML Main Page Content Length: {len(retval)}')
        frames = self.driver.find_elements(By.XPATH,'//iframe')
        print(f'Total number of iframes: {len(frames)}')
        for index, frame in enumerate(frames):
            print(f"Processing frame {index}")
            try:
                if not EC.staleness_of(frame):
                    self.driver.switch_to.frame(frame)
                else:
                    print('Frame is stale. Aborting loop for this frame.')
                    continue
                frame_name = frame.get_attribute('name')
                if frame_name:
                    print(f'Frame Name: {frame_name}')
                else:
                    print(f'Frame Index: {index}')
                retval += self.driver.page_source
                print(f'HTML Content Length: {len(retval)}')
                self.driver.switch_to.default_content()
            except NoSuchFrameException:
                self.driver.switch_to.default_content()
                print('Unable to switch to frame.')
        # If there is no content in the frames, return the main page content
        if len(retval) == 0:
            retval = main_page_html
        return retval
    
    def handle_request(self, request: WebScrapingRequest) -> WebScrapingResponse:
        html_content=None
        request.url = unquote(request.url)
        print(f"Downloading for {request.url}...")
        if(request.url.startswith('https://help.salesforce.com') or request.url.startswith('https://developer.salesforce.com')):
            request.url
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                start_time = time.perf_counter()
                future = executor.submit(self.download_web_page, request.url)
                html_content = future.result()
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time:.6f} seconds")
        else:
            response = requests.get(request.url)
            html_content = response.text
        print(f"Response length: {len(html_content)} characters")
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup.find_all("script"):
            tag.decompose()
        for tag in soup.find_all("style"):
            tag.decompose()
        for tag in soup.find_all("a"):
            tag.decompose()
        for tag in soup.find_all("svg"):
            tag.decompose()
        for tag in soup.find_all("symbol"):
            tag.decompose()
        for tag in soup.find_all("g"):
            tag.decompose()
        for tag in soup.find_all("path"):
            tag.decompose()
        tag = soup.find('//c-hc-community-main-nav-bar')
        if tag:
            tag.decompose()
        tag = soup.find('//c-hc-article-top-bar')
        if tag:
            tag.decompose()
        tag = soup.find('//c-hc-article-feedback')
        if tag:
            tag.decompose()
        tag = soup.find('//c-hc-community-footer')
        if tag:
            tag.decompose()
        tag = soup.find('//div[@id="onetrust-consent-sdk"]')
        if tag:
            tag.decompose()
        tag = soup.find('//div[@class="auraErrorMask"]')
        if tag:
            tag.decompose()
             
        text = soup.get_text()
        print(f"Cleansed Response length: {len(text)} characters")
        while "\n" in text:
            text = text.replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        return WebScrapingResponse(text=text)

