# configurações da aplicação separadas do código. Para o seu projeto:

# config/settings.py — carrega as variáveis do .env e centraliza as configurações (limite de caracteres, nome do modelo da LLM, idiomas disponíveis). Assim você não repete os.getenv(...) espalhado pelo código todo.config