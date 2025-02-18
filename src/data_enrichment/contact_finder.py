"""
Módulo responsável por identificar e enriquecer dados de contatos-chave usando LinkedIn Sales Navigator.
"""
from typing import Dict, List
import requests
from datetime import datetime
from ..config.linkedin_config import LinkedInConfig

class ContactFinder:
    def __init__(self, linkedin_credentials: Dict[str, str]):
        self.linkedin_config = LinkedInConfig()
        self.base_url = "https://api.linkedin.com/v2/salesNavigator"
        
    def find_key_contacts(self, company_name: str) -> List[Dict]:
        """
        Busca contatos-chave (CFO, Gerente Financeiro, Tesoureiro) em uma empresa usando Sales Navigator.
        """
        target_positions = [
            "CFO", "Chief Financial Officer",
            "Gerente Financeiro", "Financial Manager",
            "Tesoureiro", "Treasurer",
            "Gerente de Tesouraria", "Treasury Manager"
        ]
        
        contacts = []
        headers = self.linkedin_config.get_auth_headers()
        
        for position in target_positions:
            params = {
                "query": position,
                "company": company_name,
                "location": "Brasil"
            }
            
            try:
                response = requests.get(
                    f"{self.base_url}/search",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if 'elements' in data:
                    for element in data['elements']:
                        contact = {
                            'nome': f"{element.get('firstName', '')} {element.get('lastName', '')}",
                            'cargo': element.get('title', ''),
                            'empresa': element.get('company', ''),
                            'perfil_linkedin': element.get('linkedinProfile', ''),
                            'data_captura': datetime.now().isoformat()
                        }
                        contacts.append(contact)
            
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar contatos para cargo {position}: {str(e)}")
                continue
        
        return contacts

    def enrich_contact_data(self, contact: Dict) -> Dict:
        """
        Enriquece os dados do contato com informações adicionais do LinkedIn.
        """
        if not contact.get('perfil_linkedin'):
            return contact
            
        try:
            headers = self.linkedin_config.get_auth_headers()
            profile_id = contact['perfil_linkedin'].split('/')[-1]
            
            response = requests.get(
                f"{self.base_url}/people/{profile_id}",
                headers=headers
            )
            response.raise_for_status()
            profile_data = response.json()
            
            # Enriquece o contato com dados adicionais
            contact.update({
                'email': profile_data.get('email', ''),
                'telefone': profile_data.get('phone', ''),
                'localizacao': profile_data.get('location', ''),
                'experiencia': profile_data.get('experience', []),
                'educacao': profile_data.get('education', []),
                'ultima_atualizacao': datetime.now().isoformat()
            })
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enriquecer dados do contato {contact['nome']}: {str(e)}")
            
        return contact

    def send_inmail(self, contact: Dict, subject: str, message: str) -> bool:
        """
        Envia uma mensagem InMail para o contato via LinkedIn Sales Navigator.
        """
        if not contact.get('perfil_linkedin'):
            return False
            
        try:
            headers = self.linkedin_config.get_auth_headers()
            profile_id = contact['perfil_linkedin'].split('/')[-1]
            
            payload = {
                "recipients": [f"urn:li:person:{profile_id}"],
                "subject": subject,
                "body": message
            }
            
            response = requests.post(
                f"{self.base_url}/messaging/conversations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar InMail para {contact['nome']}: {str(e)}")
            return False
