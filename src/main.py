"""
Módulo principal que integra todos os componentes do agente inteligente.
"""
import os
from dotenv import load_dotenv
from data_enrichment.contact_finder import ContactFinder
from communication.message_handler import MessageHandler
from automation.prospect_automation import ProspectAutomation
from database.contact_repository import ContactRepository
from analytics.conversion_analytics import ConversionAnalytics

class ZFPortalAgent:
    def __init__(self):
        load_dotenv()
        
        # Inicialização dos componentes
        self.contact_finder = ContactFinder({
            'username': os.getenv('LINKEDIN_USERNAME'),
            'password': os.getenv('LINKEDIN_PASSWORD')
        })
        
        self.message_handler = MessageHandler()
        self.automation = ProspectAutomation()
        self.repository = ContactRepository(os.getenv('DATABASE_URL'))
        self.analytics = ConversionAnalytics()

    def process_new_company(self, company_name: str):
        """
        Processa uma nova empresa alvo.
        """
        # 1. Encontrar contatos-chave
        contacts = self.contact_finder.find_key_contacts(company_name)
        
        # 2. Enriquecer dados dos contatos
        for contact in contacts:
            enriched_contact = self.contact_finder.enrich_contact_data(contact)
            self.repository.save_contact(enriched_contact)
            
            # 3. Criar mensagem personalizada
            message = self.message_handler.create_personalized_message(enriched_contact)
            
            # 4. Definir estratégia de interação
            strategy = self.automation.generate_interaction_strategy(enriched_contact)
            
            # 5. Atualizar status no funil
            self.automation.update_conversion_status(enriched_contact, 'identified')

    def run_daily_tasks(self):
        """
        Executa tarefas diárias do agente.
        """
        # 1. Verificar contatos que precisam de follow-up
        contacts = self.repository.get_contacts_by_status('contacted')
        for contact in contacts:
            strategy = self.automation.generate_interaction_strategy(contact)
            if strategy['timing'].date() <= datetime.now().date():
                message = self.message_handler.create_personalized_message(contact)
                # Implementar lógica de envio
                
        # 2. Analisar métricas de conversão
        funnel_data = self.automation.conversion_funnel
        conversion_rates = self.analytics.calculate_conversion_rates(funnel_data)
        
        # 3. Identificar melhores práticas
        successful_contacts = self.repository.get_contacts_by_status('converted')
        best_practices = self.analytics.identify_best_practices(successful_contacts)

if __name__ == "__main__":
    agent = ZFPortalAgent()
    # Exemplo de uso
    agent.process_new_company("Empresa ABC")
