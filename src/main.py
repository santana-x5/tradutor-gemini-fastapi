import time # Adicionado para medir o tempo entre requisições
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models.translation import TranslationRequest, TranslationResponse
from services.llm_service import TranslationService

app = FastAPI(title="Gemini Translator API")

# 1. Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ADIÇÃO DE SEGURANÇA: RATE LIMITING (Fase 4 - Item 2) ---
# Dicionário em memória para guardar o tempo da última requisição de cada IP
last_request_time = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Aplicamos o limite apenas na rota de tradução, que é a mais "cara"
    if request.method == "POST" and request.url.path == "/translate":
        client_ip = request.client.host
        current_time = time.time()
        
        # Define um limite de 3 segundos entre traduções por usuário
        if client_ip in last_request_time:
            if current_time - last_request_time[client_ip] < 3:
                raise HTTPException(
                    status_code=429, 
                    detail="Muitas requisições. Aguarde 3 segundos para traduzir novamente."
                )
        
        last_request_time[client_ip] = current_time
    
    return await call_next(request)
# -----------------------------------------------------------

translator = TranslationService()

@app.get("/")
async def home():
    return {"status": "Online", "message": "Acesse /docs para testar a API"}

@app.get("/languages")
async def get_supported_languages():
    return {
        "languages": [
            {"code": "en", "name": "Inglês"},
            {"code": "pt-br", "name": "Português"},
            {"code": "es", "name": "Espanhol"},
            {"code": "fr", "name": "Francês"}
        ]
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    try:
        cache_key = f"{request.source_lang}:{request.target_lang}:{request.text.strip()}"
        is_cached = cache_key in translator.cache
        
        result = await translator.translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=result,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            from_cache=is_cached
        )
    except Exception as e:
        # Se for um erro de Rate Limit vindo do middleware, ele passa direto
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))