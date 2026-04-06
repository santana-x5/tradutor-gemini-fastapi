from pydantic import BaseModel, Field
from typing import Optional

class TranslationRequest(BaseModel):
    # o input, defiene que é obrigatorio, que o tamanho minimo é 1, caso o usuario n envie sorce_lang/target_lang os valores padrão serão en -> pt-br
    text: str = Field(..., min_length=1, description="O texto que você deseja traduzir")
    source_lang: str = Field("en", description="Idioma de origem (ex: en, pt, es)")
    target_lang: str = Field("pt-br", description="Idioma de destino (ex: en, pt, es)")

class TranslationResponse(BaseModel):
    original_text: str #texto do usuario
    translated_text: str #o resultado do gemini
    source_lang: str #confirmação do indioma de origem
    target_lang: str #confirmação do indioma de destino


    from_cache: bool = False # Para o usuário saber se economizou tempo/tokens, indica se a resposta veio da IA ou do cache