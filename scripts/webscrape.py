from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import sys
import subprocess
from bs4 import BeautifulSoup
import time
import requests
import io
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from dotenv import load_dotenv
import os
import tempfile
import atexit
import shutil

load_dotenv()

'''
# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# Try to find Chrome binary location
try:
    chrome_path = subprocess.check_output(["which", "google-chrome"]).decode().strip()
    chrome_options.binary_location = chrome_path
except subprocess.CalledProcessError:
    print("Could not find Chrome binary. Make sure Chrome is installed.", file=sys.stderr)
    sys.exit(1)

try:
    # Initialize the WebDriver with improved error handling
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}", file=sys.stderr)
    print(f"Chrome options: {chrome_options.arguments}", file=sys.stderr)
    print(f"Chrome binary location: {chrome_options.binary_location}", file=sys.stderr)
    sys.exit(1)
'''

# Define all possible element IDs, split characters, and element names
all_elements = {
    'title': None,
    'authors': None,
    'abstract': None,
    'advisor1': None,
    'city': None,
    'coverage': None,
    'format': None,
    'subject_area': ';',
    'recommended_citation': None,
    'bp_categories': '|',
    'keywords': ',',
    'publication_date': None,
    'degree_granted': None,
    'document_type': None,
    'article-downloads': None,
    'subject': ';',
    'source': None,
    'rights': None,
    'publisher': None,
    'relation': None,
    'identifier': None,
    'dc_subject': ';',
    'length': None
}

def extract_page_elements(soup):
    page_elements = {}
    # Get text content for all elements
    for element_id, split_char in all_elements.items():
        element = soup.find(attrs={'id': element_id})
        if element:
            text = element.find('p').text if element.find('p') else element.text
            if split_char:
                page_elements[element_id] = [item.strip() for item in text.split(split_char) if item.strip()]
            else:
                page_elements[element_id] = text.strip()
    return page_elements

def extract_download_link(soup):
    element = soup.find('div', class_='aside download-button')
    if element:
        link = element.find('a', id='pdf')
        if link:
            return link['href']
    return None

# Define a function to create and get driver
def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")  # Use incognito mode to avoid profile issues
    
    try:
        # Use ChromeDriverManager with chromium
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}", file=sys.stderr)
        raise

# Replace the global driver initialization with the function call
try:
    driver = get_chrome_driver()
except Exception as e:
    print(f"Failed to initialize Chrome driver: {e}")
    sys.exit(1)

def scrape_openworks_page(url):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    result = {'url': url, 'article-downloads': '0', 'status': '200'}
    if soup.find('div', id='404-error'):
        result['status'] = '404'
        return result

    result.update(extract_page_elements(soup))
    result['article-downloads'] = int(result['article-downloads'].replace(',', '') or '0')
    result['downloads'] = result['article-downloads']
    del result['article-downloads']
    result['downloadLink'] = extract_download_link(soup)
    result = {
        k: v.replace('\x00', '') if isinstance(v, str) else v
        for k, v in result.items()
    }
    return result

def scrape_pdf_with_session(url):
    # Create a session object
    session = requests.Session()

    # Add the cookies you found in Chrome
    cookies = {
        'BPAuth201311': os.getenv('BPAuth201311'),
        'BPUserData': os.getenv('BPUserData'),
        'bp_visitor_id': os.getenv('bp_visitor_id'),
        'bp_plack_session': os.getenv('bp_plack_session'),
        'bpsc': os.getenv('bpsc')
    }

    # Update the session's cookies
    session.cookies.update(cookies)

    # Make the request
    response = session.get(url)

    # Check if the response is a PDF
    if response.headers.get('Content-Type') == 'application/pdf':
        try:
            # Read the PDF content
            pdf_content = io.BytesIO(response.content)
            
            # Use pdfminer to extract text
            text = extract_text_with_pdfminer(pdf_content)
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return None
    else:
        return None

def extract_text_with_pdfminer(pdf_content):
    output = StringIO()
    laparams = LAParams()
    extract_text_to_fp(pdf_content, output, laparams=laparams)
    return output.getvalue()

# Modify the main block to properly handle driver cleanup
if __name__ == "__main__":
    try:
        url = 'https://openworks.wooster.edu/cgi/viewcontent.cgi?article=5098&context=independentstudy'
        print(scrape_pdf_with_session(url))
    finally:
        driver.quit()  # Ensure driver is always closed