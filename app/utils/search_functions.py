from app.utils.googleGenai import embed
from app.db.operations import get_nearest_neighbors


def search_similar_publications(query):
    embedding = embed(query)
    nearest_neighbors = get_nearest_neighbors(embedding, 10)
    return [
        {
            'id': nn[1].id,
            'title': nn[1].title,
            'url': nn[1].url,
            'downloads': nn[1].downloads,
            'abstract': nn[1].abstract,
            'advisor': nn[1].advisor,
            'department': nn[1].department,
            'disciplines': nn[1].disciplines,
            'keywords': nn[1].keywords,
            'year': nn[1].year,
            'citations': nn[1].citations,
            'downloadLink': nn[1].downloadLink
        }
        for nn in nearest_neighbors
    ]
