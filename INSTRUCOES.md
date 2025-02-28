# Instruções de Uso - Processador de PDF e Imagens

## Requisitos Prévios

Antes de executar a aplicação, você precisa instalar alguns componentes adicionais:

1. **Tesseract OCR** - Necessário para as bibliotecas que usam OCR (pytesseract, OpenCV)
   - Ubuntu/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
   - Windows: Baixe o instalador em https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract tesseract-lang`

2. **Poppler** - Necessário para pdf2image
   - Ubuntu/Debian: `sudo apt-get install poppler-utils`
   - Windows: Baixe binários em https://github.com/oschwartz10612/poppler-windows/releases/
   - macOS: `brew install poppler`

3. **Java** - Necessário para Tabula-py
   - Ubuntu/Debian: `sudo apt-get install default-jre`
   - Windows: Baixe em https://www.oracle.com/java/technologies/javase-jre8-downloads.html
   - macOS: `brew install java`

## Instalação

1. Clone o repositório ou faça o download dos arquivos
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Executando a Aplicação

Execute o seguinte comando no terminal:

```
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

## Uso da Aplicação

1. Na barra lateral, escolha a biblioteca que deseja usar
2. Carregue um arquivo (PDF ou imagem, dependendo da biblioteca escolhida)
3. Aguarde o processamento
4. Visualize os resultados na área principal
5. Use o botão "Baixar resultado" para salvar o texto extraído

## Funcionalidades por Biblioteca

1. **PyPDF2/PyPDF4**
   - Extração básica de texto de PDFs
   - Boa para documentos simples com texto claro

2. **pdfminer.six**
   - Extração detalhada de texto
   - Mantém melhor o layout do documento

3. **pytesseract**
   - OCR para imagens
   - Requer Tesseract OCR instalado no sistema

4. **OpenCV (cv2)**
   - Pré-processamento de imagens antes do OCR
   - Melhora a qualidade do reconhecimento

5. **pdf2image**
   - Converte PDFs em imagens
   - Útil para PDFs que são principalmente imagens

6. **Camelot**
   - Especializada em extrair tabelas de PDFs
   - Excelente para documentos com dados tabulares

7. **Tabula-py**
   - Também para extração de tabelas
   - Alternativa ao Camelot

8. **PDFPlumber**
   - Extrai texto e tabelas
   - Bom controle sobre o layout

9. **PyMuPDF (fitz)**
   - Biblioteca versátil e rápida
   - Bom para processamento geral de PDFs

10. **EasyOCR**
    - OCR multilíngue
    - Bom para documentos em português

## Resolução de Problemas

- **Erro com Tesseract**: Verifique se o Tesseract OCR está instalado e no PATH do sistema
- **Erro com pdf2image**: Verifique se o Poppler está instalado corretamente
- **Erro com Tabula-py**: Verifique se o Java está instalado e no PATH do sistema
- **Memória insuficiente**: Tente reduzir a resolução das imagens ou processe arquivos menores 