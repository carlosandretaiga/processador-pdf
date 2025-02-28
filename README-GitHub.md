# Processador de PDF e Imagens

Aplicação Streamlit para processamento de documentos PDF e imagens usando diversas bibliotecas especializadas.

## Funcionalidades

- Upload de arquivos PDF e imagens
- Escolha entre múltiplas bibliotecas de processamento:
  - PyPDF2/PyPDF4: Extração básica de texto de PDFs
  - pdfminer.six: Extração detalhada de texto, layout e metadados
  - pytesseract: OCR para extrair texto de imagens
  - OpenCV: Pré-processamento de imagens
  - pdf2image: Conversão de PDFs para imagens
  - Camelot: Extração de tabelas de PDFs
  - Tabula-py: Extração de tabelas
  - PDFPlumber: Extração de texto, tabelas e metadados
  - PyMuPDF: Processamento versátil de PDFs
  - EasyOCR: OCR multilíngue

## Implantação com Docker

Esta aplicação pode ser facilmente implantada usando Docker:

```bash
docker-compose up -d
```

A aplicação estará disponível em http://localhost:8501 ou no endereço configurado no seu servidor.

## Requisitos

A imagem Docker inclui todas as dependências necessárias:
- Tesseract OCR (para pytesseract)
- Poppler (para pdf2image)
- Java Runtime Environment (para tabula-py)
- Bibliotecas Python especificadas em requirements.txt

## Uso Local

Para desenvolvimento local:

1. Clone este repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale os componentes do sistema:
   ```bash
   ./install_deps.sh
   ```
4. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

## Configurações

A aplicação não requer configurações adicionais para funcionar, mas você pode personalizar:

- Porta: Altere a porta no comando de execução do Streamlit
- Diretório de dados: Monte um volume em `/app/data` para persistência 