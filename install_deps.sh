#!/bin/bash

# Script para instalar dependências necessárias para o Processador de PDF e Imagens
echo "Instalando dependências do sistema para o Processador de PDF e Imagens..."

# Detectar sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Ubuntu/Debian
    echo "Sistema Linux detectado. Usando apt-get..."
    
    sudo apt-get update
    sudo apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-por \
        poppler-utils \
        default-jre \
        python3-pip \
        python3-dev \
        build-essential \
        libpoppler-cpp-dev \
        pkg-config \
        python3-opencv
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Sistema macOS detectado. Usando brew..."
    
    # Verificar se o Homebrew está instalado
    if ! command -v brew &> /dev/null; then
        echo "Homebrew não encontrado. Instalando..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install \
        tesseract \
        tesseract-lang \
        poppler \
        openjdk \
        python \
        opencv
    
else
    echo "Sistema operacional não reconhecido automaticamente."
    echo "Para Windows, instale manualmente:"
    echo "1. Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "2. Poppler: https://github.com/oschwartz10612/poppler-windows/releases/"
    echo "3. Java JRE: https://www.oracle.com/java/technologies/javase-jre8-downloads.html"
    echo "4. Python e pip: https://www.python.org/downloads/windows/"
fi

# Instalar dependências Python
echo "Instalando dependências Python..."
pip install -r requirements.txt

echo "Instalação concluída!"
echo "Execute 'streamlit run app.py' para iniciar a aplicação." 