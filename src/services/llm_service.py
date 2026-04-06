import os
import logging
import asyncio  # ADICIONADO: Para controlar o tempo de resposta
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("Chave API GEMINI_API_KEY não encontrada no .env!")
            raise ValueError("Configuração ausente: GEMINI_API_KEY")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash" 
        self.cache = {}

        self.system_prompt = (
            "Você é um sistema de tradução de alta precisão. "
            "Sua tarefa é traduzir textos mantendo o significado exato, o tom e as nuances culturais. "
            "REGRAS CRÍTICAS:\n"
            "1. Não adicione saudações como 'Aqui está a tradução'.\n"
            "2. Não explique gramática ou escolhas de palavras.\n"
            "3. Retorne APENAS o texto traduzido.\n"
            "4. Se o texto contiver gírias, busque o equivalente cultural mais próximo."
        )

    async def translate_text(self, text: str, source_lang: str, target_lang: str, use_cache: bool = True):
        cache_key = f"{source_lang}:{target_lang}:{text.strip()}"

        if use_cache and cache_key in self.cache:
            logger.info(f"🚀 Cache Hit: {text[:20]}...")
            return self.cache[cache_key]

        user_content = f"Traduza de '{source_lang}' para '{target_lang}':\n\n{text}"
        
        try:
            # --- ADIÇÃO DE TIMEOUT (Item 3 da Fase 4) ---
            # Espera no máximo 15 segundos pela resposta do Gemini
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_id,
                    config={
                        "system_instruction": self.system_prompt,
                        "temperature": 0.3,
                    },
                    contents=user_content
                ),
                timeout=15.0
            )
            
            if not response.text:
                return "Erro: O modelo não gerou conteúdo."

            translated_text = response.text.strip()
            
            if use_cache:
                self.cache[cache_key] = translated_text
                
            return translated_text
            
        except asyncio.TimeoutError:
            logger.error("A requisição ao Gemini excedeu o tempo limite de 15s.")
            return "Erro: A tradução demorou muito. Tente novamente."
        except Exception as e:
            logger.error(f"Erro na tradução: {e}")
            return f"Erro: {str(e)}"