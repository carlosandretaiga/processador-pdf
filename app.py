import streamlit as st
import io
import os
import tempfile
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Definir configuração da página
st.set_page_config(
    page_title="Processador de PDF e Imagens",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.title("Processador de PDF e Imagens")
st.markdown("Selecione uma biblioteca para processar seus documentos PDF ou imagens.")

# Criar diretório temporário para arquivos
temp_dir = tempfile.TemporaryDirectory()

# Função para processar o arquivo com PyPDF2
def process_with_pypdf2(file_bytes):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += f"\n--- Página {page_num + 1} ---\n"
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Erro ao processar com PyPDF2: {str(e)}"

# Função para processar o arquivo com PyPDF4
def process_with_pypdf4(file_bytes):
    try:
        from PyPDF4 import PdfFileReader
        reader = PdfFileReader(io.BytesIO(file_bytes))
        text = ""
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            text += f"\n--- Página {page_num + 1} ---\n"
            text += page.extractText()
        return text
    except Exception as e:
        return f"Erro ao processar com PyPDF4: {str(e)}"

# Função para processar o arquivo com pdfminer.six
def process_with_pdfminer(file_bytes):
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(io.BytesIO(file_bytes))
        return text
    except Exception as e:
        return f"Erro ao processar com pdfminer.six: {str(e)}"

# Função para processar imagem com pytesseract
def process_with_pytesseract(file_bytes):
    try:
        import pytesseract
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image, lang='por')
        return text
    except Exception as e:
        return f"Erro ao processar com pytesseract: {str(e)}"

# Função para processar com OpenCV
def process_with_opencv(file_bytes):
    try:
        import cv2
        import pytesseract
        
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Pré-processamento para melhorar o OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Mostrar imagem processada
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax1.set_title('Original')
        ax1.axis('off')
        ax2.imshow(thresh, cmap='gray')
        ax2.set_title('Processada (Threshold)')
        ax2.axis('off')
        st.pyplot(fig)
        
        # OCR na imagem processada
        text = pytesseract.image_to_string(thresh, lang='por')
        return text
    except Exception as e:
        return f"Erro ao processar com OpenCV: {str(e)}"

# Função para processar com pdf2image
def process_with_pdf2image(file_bytes):
    try:
        from pdf2image import convert_from_bytes
        import pytesseract
        
        # Salvar o PDF em um arquivo temporário
        temp_file = os.path.join(temp_dir.name, 'temp.pdf')
        with open(temp_file, 'wb') as f:
            f.write(file_bytes)
        
        # Converter PDF para imagens
        images = convert_from_bytes(file_bytes, dpi=300)
        
        text = ""
        for i, image in enumerate(images):
            text += f"\n--- Página {i + 1} ---\n"
            text += pytesseract.image_to_string(image, lang='por')
            
            if i == 0:  # Mostrar apenas a primeira página como exemplo
                st.image(image, caption=f"Página {i+1}", use_column_width=True)
        
        return text
    except Exception as e:
        return f"Erro ao processar com pdf2image: {str(e)}"

# Função para processar tabelas com Camelot
def process_with_camelot(file_bytes):
    try:
        import camelot
        
        # Salvar o PDF em um arquivo temporário
        temp_file = os.path.join(temp_dir.name, 'temp.pdf')
        with open(temp_file, 'wb') as f:
            f.write(file_bytes)
        
        # Extrair tabelas
        tables = camelot.read_pdf(temp_file, pages='all')
        
        result = f"Total de tabelas encontradas: {len(tables)}\n"
        
        for i, table in enumerate(tables):
            result += f"\n--- Tabela {i+1} (Página {table.page}) ---\n"
            df = table.df
            result += df.to_string() + "\n"
            
            # Exibir a tabela como DataFrame
            st.write(f"Tabela {i+1} (Página {table.page}):")
            st.dataframe(df)
        
        return result
    except Exception as e:
        return f"Erro ao processar com Camelot: {str(e)}"

# Função para processar tabelas com Tabula
def process_with_tabula(file_bytes):
    try:
        import tabula
        
        # Salvar o PDF em um arquivo temporário
        temp_file = os.path.join(temp_dir.name, 'temp.pdf')
        with open(temp_file, 'wb') as f:
            f.write(file_bytes)
        
        # Extrair tabelas
        tables = tabula.read_pdf(temp_file, pages='all')
        
        result = f"Total de tabelas encontradas: {len(tables)}\n"
        
        for i, df in enumerate(tables):
            result += f"\n--- Tabela {i+1} ---\n"
            result += df.to_string() + "\n"
            
            # Exibir a tabela como DataFrame
            st.write(f"Tabela {i+1}:")
            st.dataframe(df)
        
        return result
    except Exception as e:
        return f"Erro ao processar com Tabula: {str(e)}"

# Função para processar com PDFPlumber
def process_with_pdfplumber(file_bytes):
    try:
        import pdfplumber
        
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                text += f"\n--- Página {i + 1} ---\n"
                text += page.extract_text() or "Nenhum texto extraído nesta página."
                
                # Extrair tabelas da página
                tables = page.extract_tables()
                if tables:
                    text += f"\n  {len(tables)} tabelas encontradas nesta página.\n"
                    
                    for j, table in enumerate(tables):
                        df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                        text += f"\n  Tabela {j+1}:\n"
                        text += df.to_string() + "\n"
                        
                        # Exibir somente a primeira tabela da primeira página como exemplo
                        if i == 0 and j == 0:
                            st.write(f"Exemplo de tabela extraída (Página {i+1}):")
                            st.dataframe(df)
            
            return text
    except Exception as e:
        return f"Erro ao processar com PDFPlumber: {str(e)}"

# Função para processar com PyMuPDF
def process_with_pymupdf(file_bytes):
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        
        for i, page in enumerate(doc):
            text += f"\n--- Página {i + 1} ---\n"
            text += page.get_text()
            
            # Mostrar a primeira página como exemplo
            if i == 0:
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                img_bytes = pix.tobytes("png")
                st.image(img_bytes, caption=f"Página {i+1}", use_column_width=True)
        
        doc.close()
        return text
    except Exception as e:
        return f"Erro ao processar com PyMuPDF: {str(e)}"

# Função para processar com EasyOCR
def process_with_easyocr(file_bytes):
    try:
        import easyocr
        
        # Criar leitor para português
        reader = easyocr.Reader(['pt'], gpu=False)
        
        # Processar a imagem
        image = Image.open(io.BytesIO(file_bytes))
        image_np = np.array(image)
        
        # Mostrar a imagem
        st.image(image, caption="Imagem carregada", use_column_width=True)
        
        # Executar OCR
        results = reader.readtext(image_np)
        
        # Extrair texto
        text = ""
        for detection in results:
            text += detection[1] + "\n"
        
        # Visualizar detecções
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(image_np)
        
        for detection in results:
            box = detection[0]
            text = detection[1]
            
            # Desenhar caixa
            points = np.array(box, np.int32).reshape((-1, 1, 2))
            ax.plot([p[0][0] for p in points] + [points[0][0][0]], 
                    [p[0][1] for p in points] + [points[0][0][1]], 
                    'r-', linewidth=2)
            
            # Adicionar texto
            ax.text(points[0][0][0], points[0][0][1], text[:20] + ('...' if len(text) > 20 else ''),
                   fontsize=9, color='blue', backgroundcolor='white')
        
        ax.axis('off')
        st.pyplot(fig)
        
        return text
    except Exception as e:
        return f"Erro ao processar com EasyOCR: {str(e)}"

# Opções de bibliotecas
library_options = {
    "PyPDF2": {"function": process_with_pypdf2, "description": "Extração básica de texto de PDFs", "accepts": ["pdf"]},
    "PyPDF4": {"function": process_with_pypdf4, "description": "Extração básica de texto de PDFs", "accepts": ["pdf"]},
    "pdfminer.six": {"function": process_with_pdfminer, "description": "Extração detalhada de texto, layout e metadados", "accepts": ["pdf"]},
    "pytesseract": {"function": process_with_pytesseract, "description": "OCR para extrair texto de imagens", "accepts": ["png", "jpg", "jpeg", "tiff"]},
    "OpenCV (cv2)": {"function": process_with_opencv, "description": "Pré-processamento de imagens para OCR", "accepts": ["png", "jpg", "jpeg"]},
    "pdf2image": {"function": process_with_pdf2image, "description": "Conversão de PDFs em imagens para OCR", "accepts": ["pdf"]},
    "Camelot": {"function": process_with_camelot, "description": "Extração de tabelas de PDFs", "accepts": ["pdf"]},
    "Tabula-py": {"function": process_with_tabula, "description": "Extração de tabelas de PDFs", "accepts": ["pdf"]},
    "PDFPlumber": {"function": process_with_pdfplumber, "description": "Extrai texto, tabelas e metadados", "accepts": ["pdf"]},
    "PyMuPDF (fitz)": {"function": process_with_pymupdf, "description": "Processamento versátil de PDFs", "accepts": ["pdf"]},
    "EasyOCR": {"function": process_with_easyocr, "description": "OCR multilíngue para imagens", "accepts": ["png", "jpg", "jpeg"]}
}

# Interface do usuário
with st.sidebar:
    st.header("Configurações")
    
    selected_library = st.selectbox(
        "Escolha uma biblioteca:", 
        options=list(library_options.keys()),
        format_func=lambda x: f"{x} - {library_options[x]['description']}"
    )
    
    st.markdown(f"**Biblioteca selecionada:** {selected_library}")
    st.markdown(f"**Descrição:** {library_options[selected_library]['description']}")
    st.markdown(f"**Aceita arquivos:** {', '.join(library_options[selected_library]['accepts'])}")
    
    accepted_files = library_options[selected_library]['accepts']
    file_types = {
        "pdf": "application/pdf",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "tiff": "image/tiff"
    }
    
    accepted_file_types = [file_types[ext] for ext in accepted_files if ext in file_types]
    
    uploaded_file = st.file_uploader(
        "Carregar arquivo", 
        type=accepted_files,
        accept_multiple_files=False
    )

# Área principal
if uploaded_file:
    file_details = {
        "Nome": uploaded_file.name,
        "Tipo": uploaded_file.type,
        "Tamanho": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.write("### Detalhes do arquivo")
    for k, v in file_details.items():
        st.write(f"**{k}:** {v}")
    
    st.write("### Processando arquivo...")
    with st.spinner("Aguarde um momento..."):
        file_bytes = uploaded_file.getvalue()
        processing_function = library_options[selected_library]["function"]
        result = processing_function(file_bytes)
    
    st.write("### Resultado")
    st.text_area("Texto extraído:", value=result, height=400)
    
    # Adicionar opção para download do resultado
    st.download_button(
        label="Baixar resultado como arquivo de texto",
        data=result,
        file_name=f"{uploaded_file.name}_resultado.txt",
        mime="text/plain",
    )
else:
    st.info(f"Faça upload de um arquivo ({', '.join(accepted_files)}) para processá-lo com {selected_library}.")

# Limpar diretório temporário no final
st.session_state["temp_dir"] = temp_dir  # Guarda na sessão para garantir limpeza

# Rodapé com informações adicionais
st.markdown("---")
st.markdown("""
### Sobre as bibliotecas disponíveis:

- **PyPDF2/PyPDF4**: Extração básica de texto de PDFs
- **pdfminer.six**: Extração detalhada de texto, layout e metadados de PDFs
- **pytesseract**: OCR para extrair texto de imagens
- **OpenCV (cv2)**: Pré-processamento de imagens antes do OCR
- **pdf2image**: Converte PDFs em imagens para processamento com OCR
- **Camelot**: Especializada em extrair tabelas de PDFs
- **Tabula-py**: Python wrapper para Tabula (extração de tabelas)
- **PDFPlumber**: Extrai texto, tabelas e metadados com bom controle sobre o layout
- **PyMuPDF (fitz)**: Biblioteca rápida e versátil para processamento de PDFs
- **EasyOCR**: OCR multilíngue com boa precisão
""") 