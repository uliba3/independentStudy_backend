import requests
import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

async def scrape_pdf_with_session(url):
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

    print("cookies:", cookies)

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
            text = await extract_text_with_pdfminer(pdf_content)
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return None
    else:
        return None

async def extract_text_with_pdfminer(pdf_content):
    output = StringIO()
    laparams = LAParams()
    extract_text_to_fp(pdf_content, output, laparams=laparams)
    return output.getvalue()

if __name__ == "__main__":
    url = "https://openworks.wooster.edu/cgi/viewcontent.cgi?article=5098&context=independentstudy"
    result = asyncio.run(scrape_pdf_with_session(url))
    print(result)