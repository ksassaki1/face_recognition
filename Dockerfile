# Dockerfile (na raiz do repositório)

FROM python:3.10-slim

# 1) Instalar dependências de sistema (CMake, compiladores, libs de imagem, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk2.0-dev \
    libboost-python-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libglib2.0-0 \
    libjpeg-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Garante que a pasta known_faces exista (mesmo que vazia)
RUN mkdir -p app/known_faces

# 3) Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copia todo o diretório app/ (incluindo main.py, known_faces/, registered_faces/, etc.)
COPY app/ ./app

# 5) Expõe a porta 8000
EXPOSE 8005

# 6) Comando para iniciar o FastAPI via Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
