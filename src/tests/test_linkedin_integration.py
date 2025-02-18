"""
Testes para a integração com LinkedIn Sales Navigator
"""
import os
import pytest
from dotenv import load_dotenv
from ..data_enrichment.contact_finder import ContactFinder
from ..config.linkedin_config import LinkedInConfig

@pytest.fixture
def linkedin_config():
    load_dotenv()
    return LinkedInConfig()

@pytest.fixture
def contact_finder():
    load_dotenv()
    return ContactFinder({})

def test_linkedin_auth(linkedin_config):
    """
    Testa se conseguimos obter um token de acesso válido
    """
    headers = linkedin_config.get_auth_headers()
    assert headers.get('Authorization') is not None
    assert headers.get('Authorization').startswith('Bearer ')

def test_find_contacts(contact_finder):
    """
    Testa a busca de contatos em uma empresa
    """
    company_name = "Empresa Teste"  # Substitua por uma empresa real para teste
    contacts = contact_finder.find_key_contacts(company_name)
    
    assert isinstance(contacts, list)
    if contacts:
        contact = contacts[0]
        assert 'nome' in contact
        assert 'cargo' in contact
        assert 'empresa' in contact
        assert 'perfil_linkedin' in contact

def test_enrich_contact(contact_finder):
    """
    Testa o enriquecimento de dados de um contato
    """
    test_contact = {
        'nome': 'Teste',
        'cargo': 'CFO',
        'empresa': 'Empresa Teste',
        'perfil_linkedin': 'https://www.linkedin.com/in/teste-perfil'
    }
    
    enriched = contact_finder.enrich_contact_data(test_contact)
    assert enriched.get('email') is not None or enriched.get('telefone') is not None

def test_send_inmail(contact_finder):
    """
    Testa o envio de InMail para um contato
    """
    test_contact = {
        'nome': 'Teste',
        'perfil_linkedin': 'https://www.linkedin.com/in/teste-perfil'
    }
    
    subject = "Teste de Integração"
    message = "Esta é uma mensagem de teste automatizado."
    
    result = contact_finder.send_inmail(test_contact, subject, message)
    assert isinstance(result, bool)
