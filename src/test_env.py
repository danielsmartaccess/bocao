"""
Script para testar a configuração das variáveis de ambiente.
"""
import os
from dotenv import load_dotenv

def test_environment():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Lista de variáveis que precisamos verificar
    required_vars = [
        'LINKEDIN_USERNAME',
        'LINKEDIN_PASSWORD',
        'DATABASE_URL'
    ]
    
    # Verifica cada variável
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
        else:
            # Mostra apenas os primeiros caracteres das credenciais por segurança
            masked_value = value[:3] + '****' if var in ['LINKEDIN_PASSWORD'] else value
            print(f'{var} está configurado: {masked_value}')
    
    # Reporta se alguma variável está faltando
    if missing_vars:
        print('\nERRO: As seguintes variáveis não estão configuradas:')
        for var in missing_vars:
            print(f'- {var}')
    else:
        print('\nSucesso! Todas as variáveis de ambiente necessárias estão configuradas.')

if __name__ == '__main__':
    test_environment()
