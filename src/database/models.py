"""
Modelos de dados para o banco PostgreSQL
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ContatoLinkedIn(Base):
    __tablename__ = 'contatos_linkedin'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    cargo = Column(String(100))
    empresa = Column(String(255))
    perfil_linkedin = Column(String)
    email = Column(String(255))
    telefone = Column(String(50))
    localizacao = Column(String(255))
    experiencia = Column(JSON)
    educacao = Column(JSON)
    status = Column(String(50))  # identified, contacted, interested, converted
    data_captura = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    historico_interacoes = Column(JSON)

def init_db(database_url: str):
    """
    Inicializa o banco de dados e cria as tabelas se não existirem
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
