from app.db.schema import IndependentStudy, VectorEmbedding
from app.db.session import session
from sqlalchemy import func
from app.utils.googleGenai import embed

def add_pdf_text(independent_study, pdf_text):
    independent_study.pdf_text = pdf_text
    session.commit()

def add_independent_study(data):
    record = get_one_by_field(IndependentStudy, {'url': data['url']})
    if record is None:
        new_publication = IndependentStudy(
            title=data.pop('title', None),
            url=data.pop('url', None),
            downloads=data.pop('downloads', None),
            abstract=data.pop('abstract', None),
            advisor=data.pop('advisor1', None),
            department=data.pop('subject_area', []),
            disciplines=data.pop('bp_categories', []),
            keywords=data.pop('keywords', []),
            year=data.pop('publication_date', None),
            downloadLink=data.pop('downloadLink', None),
            citations=data.pop('recommended_citation', None)
        )
        session.add(new_publication)
        session.commit()
    elif contains_none(record):
        existing_study = session.query(IndependentStudy).filter(IndependentStudy.url == data['url']).first()
        existing_study.title = data.pop('title', None)
        existing_study.downloads = data.pop('downloads', None)
        existing_study.abstract = data.pop('abstract', None)
        existing_study.advisor = data.pop('advisor1', None)
        existing_study.department = data.pop('subject_area', None)
        existing_study.disciplines = data.pop('bp_categories', None)
        existing_study.keywords = data.pop('keywords', None)
        existing_study.year = data.pop('publication_date', None)
        existing_study.downloadLink = data.pop('downloadLink', None)
        existing_study.citations = data.pop('recommended_citation', None)
        session.commit()

def add_vector_embedding(independent_study_id, text_type, embedding, original_text):
    record = get_one_by_field(VectorEmbedding, {'independent_study_id': independent_study_id, 'original_text': original_text})
    if record is None:
        new_embedding = VectorEmbedding(
            independent_study_id=independent_study_id,
            text_type=text_type,
            embedding=embedding,
            original_text=original_text
        )
        session.add(new_embedding)
        session.commit()
    elif contains_none(record):
        existing_embedding = session.query(VectorEmbedding).filter(VectorEmbedding.independent_study_id == independent_study_id, VectorEmbedding.original_text == original_text).first()
        existing_embedding.text_type = text_type
        existing_embedding.embedding = embedding
        existing_embedding.original_text = original_text
        session.commit()

def get_all(name):
    return session.query(name).all()

def get_batch(name, offset, batch_size):
    return session.query(name).order_by(name.id).offset(offset).limit(batch_size).all()

def get_by_id(name, id):
    return session.query(name).get(id)

def contains_none(record, columns=None):
    if record is None:
        return True
    
    if columns is None:
        # Check all columns if no specific columns are provided
        columns = record.__table__.columns
    else:
        # Convert column names to actual column objects
        columns = [getattr(record.__table__.c, col) for col in columns]
    
    for column in columns:
        if getattr(record, column.name) is None:
            return True
    return False

def get_one_by_field(name, field_value_map):
    query = session.query(name)
    for field, value in field_value_map.items():
        query = query.filter(getattr(name, field) == value)
    return query.first()

def is_exists(name, field_value_map):
    query = session.query(name)
    for field, value in field_value_map.items():
        query = query.filter(getattr(name, field) == value)
    return session.query(query.exists()).scalar()

def get_nearest_neighbors(embedding, k, publication_type_id=None):
    subquery = (
        session.query(
            VectorEmbedding.independent_study_id,
            func.min(VectorEmbedding.embedding.cosine_distance(embedding)).label('min_distance')
        )
        .group_by(VectorEmbedding.independent_study_id)
        .subquery()
    )

    query = (
        session.query(VectorEmbedding, IndependentStudy)
        .join(IndependentStudy)
        .join(subquery, VectorEmbedding.independent_study_id == subquery.c.independent_study_id)
        .filter(VectorEmbedding.embedding.cosine_distance(embedding) == subquery.c.min_distance)
        .order_by(subquery.c.min_distance)
    )

    if publication_type_id is not None:
        query = query.filter(IndependentStudy.publication_type_id == publication_type_id)

    return query.limit(k).all()

if __name__ == "__main__":
    print(get_nearest_neighbors(embed("African Art"), 3)[0][1].title)
    session.commit()
    session.close()
