import streamlit as st
import io
import os
import tempfile
import pandas as pd
from PIL import Image

# Definir configuração da página
st.set_page_config(
    page_title="Processador de PDF e Imagens",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.title("Processador de PDF e Imagens")
st.markdown("""
Selecione uma biblioteca para processar seus documentos PDF ou imagens.
**Nota**: Apenas PyPDF2 está disponível nesta versão mínima.
""")

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

# Opções de bibliotecas - apenas PyPDF2 nesta versão
library_options = {
    "PyPDF2": {"function": process_with_pypdf2, "description": "Extração básica de texto de PDFs", "accepts": ["pdf"]},
}

# Interface do usuário
with st.sidebar:
    st.header("Configurações")
    
    selected_library = "PyPDF2"  # Fixa PyPDF2 como única opção
    
    st.markdown(f"**Biblioteca disponível:** {selected_library}")
    st.markdown(f"**Descrição:** {library_options[selected_library]['description']}")
    st.markdown(f"**Aceita arquivos:** {', '.join(library_options[selected_library]['accepts'])}")
    
    accepted_files = library_options[selected_library]['accepts']
    
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
    st.info(f"Faça upload de um arquivo PDF para processá-lo com PyPDF2.")

# Limpar diretório temporário no final
st.session_state["temp_dir"] = temp_dir  # Guarda na sessão para garantir limpeza

# Rodapé com informações adicionais
st.markdown("---")
st.markdown("""
### Sobre a biblioteca disponível:

- **PyPDF2**: Extração básica de texto de PDFs
  
Esta é uma versão mínima da aplicação. Para usar outras bibliotecas (pdfminer.six, 
pytesseract, OpenCV, pdf2image, Camelot, Tabula-py, PDFPlumber, PyMuPDF, EasyOCR), 
é necessário instalar dependências adicionais (execute o script `install_deps.sh`).
""") 