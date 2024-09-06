import sys
import os

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.search_functions import search_similar_publications
from app.utils.query_processing import explain_search_results, create_search_query, create_search_query_from_independent_study
from app.db.operations import get_by_id, add_pdf_text
from app.db.schema import IndependentStudy
from app.utils.web_scraping import scrape_pdf_with_session

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/search")
async def search_endpoint(query: str):
    try:
        print("Received query:", query)
        title = await create_search_query(query)
        similar_publications = search_similar_publications(title)
        explanation = await explain_search_results(query, similar_publications)
        print("similar_publications:", similar_publications, "explanation:", explanation, "title:", title)
        return {"similar_publications": similar_publications, "explanation": explanation, "search_title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask")
async def ask_endpoint(query: str, id: int):
    try:
        print("Received query:", query)
        print("Received id:", id)
        independent_study = get_by_id(IndependentStudy, id)
        print("downloadLink:", independent_study.downloadLink)
        if independent_study.pdf_text is None:
            pdf_text = await scrape_pdf_with_session(independent_study.downloadLink)
            if pdf_text is not None:
                add_pdf_text(independent_study, pdf_text)
        else:
            pdf_text = independent_study.pdf_text
        print("pdf_text:", pdf_text[:10])
        result = await create_search_query_from_independent_study(independent_study, query, pdf_text)
        print("Result:", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))