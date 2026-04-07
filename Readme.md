# 🌐 Tradutor com LLM

> Serviço de tradução de alta precisão utilizando Large Language Models, com suporte a múltiplos idiomas.

---

## 📋 Escopo do Projeto

### O que o projeto faz
API de tradução de textos construída com Python e FastAPI, que utiliza uma LLM externa para realizar traduções com maior precisão e sensibilidade ao contexto do que serviços tradicionais.

### Funcionalidades previstas
- Tradução de texto via requisição HTTP (endpoint `POST /translate`)
- Suporte inicial ao par **EN → PT-BR**, com expansão para outros idiomas
- Listagem de idiomas disponíveis via `GET /languages`
- Cache em memória para evitar chamadas repetidas à LLM
- Validação de entrada (limite de caracteres, idioma válido, texto não vazio)

### Fora do escopo (por enquanto)
- Autenticação de usuários
- Histórico de traduções
- Banco de dados
- Interface mobile

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python + FastAPI |
| Servidor | Uvicorn |
| Tradução | Gemini 2.5 flash |
| Cache | Dicionário em memória (Python) |
| Frontend | HTML + CSS + JavaScript puro |
| Deploy backend |  Render |
| Deploy frontend | Vercel |

---

## 📁 Estrutura de Pastas

```
tradutor-gemini-fastapi/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── index.js
├── src/
│   ├── models/
│   ├── services/
│   └── main.py
├── venv/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
-->
```

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
# Chave de API do provedor de LLM escolhido
LLM_API_KEY=your_key_here

# Limite de caracteres por requisição
MAX_CHARS=2000

# Ambiente de execução
ENV=development
```

> ⚠️ Nunca suba o arquivo `.env` real para o GitHub. Ele já está no `.gitignore`.

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone <!-- URL do repositório -->
cd <!-- nome da pasta -->

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com sua chave de API
```

### Executando

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
A documentação interativa (Swagger) estará em `http://localhost:8000/docs`.

---

## 📡 Endpoints da API

### `POST /translate`
Recebe um texto e retorna a tradução.

**Request body:**
```json
{
  "text": "Hello, how are you?",
  "source_lang": "en",
  "target_lang": "pt-br"
}
```

**Response:**
```json
{
  "translated_text": "Olá, como vai você?",
  "source_lang": "en",
  "target_lang": "pt-br"
}
```

---

### `GET /languages`
Retorna a lista de idiomas suportados.

**Response:**
```json
{
  "languages": ["en", "pt-br", "es", "fr", "de"]
}
```

---

## 🌍 Idiomas Suportados

| Código | Idioma |
|--------|--------|
| `en` | Inglês |
| `pt-br` | Português (Brasil) |
| `es` | Espanhol |
| `de` | alemão |
| `fr` | francês |
| `it` | italiano |

---

## 🏗️ Decisões de Arquitetura

- **FastAPI** foi escolhido sobre Flask por suporte nativo a código assíncrono e geração automática de documentação Swagger.
- **Sem banco de dados** no escopo inicial — o sistema funciona como intermediário stateless entre o cliente e a LLM.
- **Cache em memória** (dicionário Python) para requisições repetidas. Redis pode ser considerado futuramente se o volume escalar.
- **LLM via API externa** — nenhum modelo é hospedado localmente. A tradução é delegada a um provedor, mantendo a infraestrutura simples.

---

## 📌 Status do Projeto

- [x] Definição de escopo
- [x] Integração com LLM
- [x] Endpoints implementados
- [x] Frontend básico
- [x] Deploy

---

# 🔗 Links do Projeto
Deploy Frontend: [Link_vercel](tradutor-gemini-fastapi.vercel.app)

API Endpoint:[Link_render](https://tradutor-gemini-fastapi.onrender.com)

Documentação Swagger (API):[Link_API](https://tradutor-gemini-fastapi.onrender.com/docs)

## 👤 Autor

**Klinger felix xavier santana**  
Linkedlin: [Link_linkedin](https://www.linkedin.com/in/klinger-felix-xavier-santana-83a3112a6/)
---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.