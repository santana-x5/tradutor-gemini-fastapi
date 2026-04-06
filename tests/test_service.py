# tests/ — testes automatizados. 

import asyncio
import sys
import os

# Ajuste do caminho para encontrar a pasta src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'src'))

from services.llm_service import TranslationService

async def interactive_shell():
    service = TranslationService()
    
    print("\n" + "="*40)
    print("Digite 'sair' para encerrar.")
    print("="*40)

    while True:
        # 1. Simula o Input do Usuário
        text = input("\nTexto em Inglês: ")
        
        if text.lower() == 'sair':
            break

        if not text.strip():
            continue

        print("Wait... 🤔")
        
        # 2. Chama o serviço (Exatamente como o FastAPI fará)
        # O parâmetro source e target podem ser fixos para o teste
        result = await service.translate_text(text, "en", "pt-br")
        
        # 3. Exibe o Output
        print(f"Tradução: {result}")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_shell())
    except KeyboardInterrupt:
        print("\nEncerrando...")

#FUNCIONA!!!