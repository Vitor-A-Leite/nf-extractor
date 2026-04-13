FROM python:3.11-slim

# Evita prompts interativos no apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Dependências do sistema (pdfplumber precisa de algumas)
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]