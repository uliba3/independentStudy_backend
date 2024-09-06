import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.operations import add_independent_study, add_vector_embedding, is_exists, get_all, get_one_by_field, contains_none, get_batch
from app.db.schema import IndependentStudy, VectorEmbedding
from scripts.webscrape import scrape_openworks_page
from app.utils.googleGenai import embed

def add_all_publications():
    for i in range(1, 11248): # 11247 is the total number of independent studies 8644
        url = f"https://openworks.wooster.edu/independentstudy/{i}/"
        record = get_one_by_field(IndependentStudy, {'url': url})
        if record is None:
            print(f"Independent study does not exist: {url}")
            data = scrape_openworks_page(url)
            print(data)
            if data['status'] == '404':
                continue
            add_independent_study(data)
            print(f"Added or updated independent study: {url}")
        else:
            print(f"Independent study already exists: {url}")

def add_vector_embeddings(embedding_type='all', batch_size=100):
    """
    Add vector embeddings for independent studies.
    :param embedding_type: str - 'all', 'title', 'abstract', or 'keywords'
    """
    offset = 0
    while True:
        independent_studies = get_batch(IndependentStudy, offset, batch_size)
        if not independent_studies:
            break
        for independent_study in independent_studies:
            # Process title embeddings
            if (embedding_type in ['all', 'title'] and 
                independent_study.title is not None):
                print(independent_study.id, independent_study.title)
                if not is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': independent_study.title}):
                    print(f"Adding title embedding for: {independent_study.id}")
                    try:
                        embedding = embed(independent_study.title)
                        add_vector_embedding(independent_study.id, 'title', embedding, independent_study.title)
                    except Exception as e:
                        print(f"Error adding title embedding for {independent_study.id}: {e}")

            # Process abstract embeddings
            if (embedding_type in ['all', 'abstract'] and 
                independent_study.abstract is not None):
                print(independent_study.id, independent_study.title)
                if not is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': independent_study.abstract}):
                    print(f"Adding abstract embedding for: {independent_study.id}")
                    try:
                        embedding = embed(independent_study.abstract)
                        add_vector_embedding(independent_study.id, 'abstract', embedding, independent_study.abstract)
                    except Exception as e:
                        print(f"Error adding abstract embedding for {independent_study.id}: {e}")

            # Process keyword embeddings
            if (embedding_type in ['all', 'keywords'] and 
                independent_study.keywords):
                keywords = ' '.join(independent_study.keywords)
                print(independent_study.id, keywords)
                if not is_exists(VectorEmbedding, {'independent_study_id': independent_study.id, 'original_text': keywords}):
                    print(f"Adding keywords embedding for: {independent_study.id}")
                    try:
                        embedding = embed(keywords)
                        add_vector_embedding(independent_study.id, 'keywords', embedding, keywords)
                    except Exception as e:
                        print(f"Error adding keywords embedding for {independent_study.id}: {e}")
        offset += batch_size

if __name__ == "__main__":
    add_all_publications()
    add_vector_embeddings(embedding_type='all', batch_size=100)  # This will process all types of embeddings
