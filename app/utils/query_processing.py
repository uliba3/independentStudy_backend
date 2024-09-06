from app.utils.googleGenai import runModel

async def explain_search_results(query, publications):
    # Format the publications list into a string
    formatted_publications = str(publications)
    
    result = await runModel("flash", 
             f"""You are AI search engine for past independent research projects at Wooster. 
             You are given a search query and the relevant publications found in response to that query.
             Summarize and analyze the key findings or themes from the search results in Markdown format.
             ###
             Search Query: {query}
             Publications:
            {formatted_publications}
             """)
    return result
    
async def create_search_query(query):
    result = await runModel("flash", 
             f"""You are AI search engine for past independent research projects at Wooster. 
             You are given a search query. You need to find relevant publications.
             I will do the semantic search so please provide the title for the search query.
             Try to make the title as abstract as possible.
             ###
             Input: I want to find the publications on pesticides in the atmosphere.
             Title: Pesticides in the Atmosphere
             ###
             Input: Something related to the AI
             Title: Artificial Intelligence
             ###
             Input: {query}
             """)
    return result[6:]

async def create_search_query_from_independent_study(independent_study, query, pdf_text):
    if pdf_text is None:
        return f"Could not find the paper. Try visiting {independent_study.url}"
    print("Independent study:", pdf_text[:10])
    result = await runModel("flash", 
             f"""
             {pdf_text}
             ###
             {query}
             Answer in Markdown format.
             """)
    return result