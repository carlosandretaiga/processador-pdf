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

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

## Requisitos

- Python 3.8+
- Tesseract OCR (para pytesseract)
- Java Runtime Environment (para tabula-py) 