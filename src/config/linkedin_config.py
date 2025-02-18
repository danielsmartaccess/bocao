"""
Configurações para integração com LinkedIn Sales Navigator
"""
from typing import Dict
import os
from dotenv import load_dotenv

class LinkedInConfig:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.access_token = None

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Retorna os headers de autenticação para as requisições à API
        """
        if not self.access_token:
            self.access_token = self._get_access_token()
            
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _get_access_token(self) -> str:
        """
        Obtém um novo access token usando as credenciais OAuth2
        """
        # TODO: Implementar lógica de OAuth2 para obter access token
        # Por enquanto, retornamos o token estático do .env
        return os.getenv('LINKEDIN_ACCESS_TOKEN')
