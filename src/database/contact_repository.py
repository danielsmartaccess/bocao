"""
Módulo responsável pelo armazenamento e gestão dos dados dos contatos.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import ContatoLinkedIn, init_db

class ContactRepository:
    def __init__(self, database_url: str):
        """
        Inicializa o repositório com a conexão ao banco de dados
        """
        Session = init_db(database_url)
        self.session = Session()

    def save_contact(self, contact_data: Dict) -> ContatoLinkedIn:
        """
        Salva ou atualiza um contato no banco de dados
        """
        existing_contact = self.get_contact_by_linkedin(contact_data.get('perfil_linkedin'))
        
        if existing_contact:
            # Atualiza o contato existente
            for key, value in contact_data.items():
                setattr(existing_contact, key, value)
            contact = existing_contact
        else:
            # Cria um novo contato
            contact = ContatoLinkedIn(**contact_data)
            self.session.add(contact)
        
        self.session.commit()
        return contact

    def get_contact_by_linkedin(self, linkedin_profile: str) -> Optional[ContatoLinkedIn]:
        """
        Busca um contato pelo perfil do LinkedIn
        """
        return self.session.query(ContatoLinkedIn).filter_by(perfil_linkedin=linkedin_profile).first()

    def get_contact_by_email(self, email: str) -> Optional[ContatoLinkedIn]:
        """
        Busca um contato pelo email
        """
        return self.session.query(ContatoLinkedIn).filter_by(email=email).first()

    def update_contact_status(self, contact_id: int, new_status: str, interaction_note: str = None):
        """
        Atualiza o status de um contato e adiciona nota de interação
        """
        contact = self.session.query(ContatoLinkedIn).get(contact_id)
        if contact:
            contact.status = new_status
            contact.ultima_atualizacao = datetime.now()
            
            if interaction_note:
                historico = contact.historico_interacoes or []
                historico.append({
                    'data': datetime.now().isoformat(),
                    'status': new_status,
                    'nota': interaction_note
                })
                contact.historico_interacoes = historico
            
            self.session.commit()

    def get_contacts_by_status(self, status: str) -> List[ContatoLinkedIn]:
        """
        Retorna todos os contatos com um determinado status
        """
        return self.session.query(ContatoLinkedIn).filter_by(status=status).all()

    def get_contacts_by_company(self, company_name: str) -> List[ContatoLinkedIn]:
        """
        Retorna todos os contatos de uma determinada empresa
        """
        return self.session.query(ContatoLinkedIn).filter_by(empresa=company_name).all()

    def get_contacts_needing_followup(self, days_since_last_update: int = 7) -> List[ContatoLinkedIn]:
        """
        Retorna contatos que precisam de follow-up baseado na última atualização
        """
        cutoff_date = datetime.now() - timedelta(days=days_since_last_update)
        return (self.session.query(ContatoLinkedIn)
                .filter(ContatoLinkedIn.ultima_atualizacao <= cutoff_date)
                .filter(ContatoLinkedIn.status.in_(['identified', 'contacted']))
                .all())
