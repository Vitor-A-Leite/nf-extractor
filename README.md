# NF-e Extractor API

REST API to extract structured data from Brazilian fiscal notes (NF-e) PDFs using OpenAI and FastAPI.

## How it works

1. You send a NF-e PDF to the API
2. The text is extracted from the PDF using `pdfplumber`
3. The text is sent to GPT-4o-mini, which returns structured JSON
4. The JSON is validated with Pydantic and returned in the response

## Requirements

- Docker and Docker Compose
- OpenAI API key

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/nfe-extractor-api.git
cd nfe-extractor-api
```

**2. Configure environment variables**
```bash
cp .env.template .env
```

Edit `.env` with your keys:
```env
OPENAI_API_KEY=your-openai-key-here
API_KEY=your-api-key-here
```

To generate a secure `API_KEY`:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**3. Start the server**
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Endpoints

### `POST /nfe/extrair`
Receives a NF-e PDF and returns the extracted structured data.

**Authentication:** requires the `X-API-Key` header.

**Request:**
```bash
curl -X POST http://localhost:8000/nfe/extrair \
  -H "X-API-Key: your-api-key-here" \
  -F "file=@nota_fiscal.pdf"
```

**Response:**
```json
{
  "numero": "000123",
  "serie": "1",
  "data_emissao": "01/04/2026",
  "emitente_nome": "Empresa Exemplo LTDA",
  "emitente_cnpj": "00.000.000/0001-00",
  "emitente_uf": "SP",
  "destinatario_nome": "Cliente Exemplo",
  "destinatario_cnpj_cpf": "000.000.000-00",
  "valor_produtos": 100.00,
  "valor_frete": 0.0,
  "valor_desconto": 0.0,
  "valor_total": 100.00,
  "itens": [
    {
      "descricao": "Produto Exemplo",
      "quantidade": 1.0,
      "unidade": "UN",
      "valor_unitario": 100.00,
      "valor_total": 100.00
    }
  ]
}
```

### `GET /nfe/health`
Returns the API status. No authentication required.

```bash
curl http://localhost:8000/nfe/health
```

## Interactive docs

FastAPI generates interactive documentation automatically. With the server running, access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [OpenAI API](https://platform.openai.com/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Docker](https://www.docker.com/)