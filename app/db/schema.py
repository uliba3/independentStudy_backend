from sqlalchemy import Integer, String, ForeignKey, ARRAY, Text
from sqlalchemy.orm import relationship, mapped_column
from pgvector.sqlalchemy import Vector
from app.db.session import Base

class IndependentStudy(Base):
    __tablename__ = 'independent_study'
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    url = mapped_column(String)
    downloads = mapped_column(Integer)
    abstract = mapped_column(String)
    advisor = mapped_column(String)
    department = mapped_column(ARRAY(String))
    disciplines = mapped_column(ARRAY(String))
    keywords = mapped_column(ARRAY(String))
    year = mapped_column(Integer)
    citations = mapped_column(String)
    downloadLink = mapped_column(String)
    pdf_text = mapped_column(Text)
    vector_embeddings = relationship("VectorEmbedding", back_populates="independent_study")

class VectorEmbedding(Base):
    __tablename__ = 'vector_embedding'
    id = mapped_column(Integer, primary_key=True)
    independent_study_id = mapped_column(Integer, ForeignKey('independent_study.id'), nullable=False)
    text_type = mapped_column(String, nullable=False)
    embedding = mapped_column(Vector(768), nullable=False)
    original_text = mapped_column(String, nullable=False)
    independent_study = relationship("IndependentStudy", back_populates="vector_embeddings")