from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import FastAPI, React
from diagrams.onprem.database import PostgreSQL
from diagrams.custom import Custom
from diagrams.generic.device import Tablet

with Diagram("WooScholar Architecture", show=False, filename="docs/architecture.png"):

    openworks = Custom("openworks.wooster.edu", "resources/internet.jpg")

    with Cluster("Frontend"):
        user = Tablet("User")
        frontend = React("Frontend")

    with Cluster("Backend"):
        main = FastAPI("Program")
        with Cluster("Database"):
            db = PostgreSQL("Database")
            vector_db = PostgreSQL("Vector Database")
    with Cluster("LLM"):
        gemini = Custom("Gemini API", "resources/gemini.png")
    
    openworks >> Edge(label="0. Web Scrape") << db
    frontend >> Edge(label="1. User Query") >> main >> Edge(label="5. Return Results") >> frontend
    gemini >> Edge(label="2. Generate IS title") << main
    main >> Edge(label="3. Vector Search") << vector_db
    gemini >> Edge(label="4. Generate IS description") << main
    db >> Edge(style="dotted") << vector_db