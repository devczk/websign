import streamlit as st
import imgkit
import os
import tempfile

# Função para substituir os campos no SVG
def editar_svg(svg_path, nome, cargo, telefone, email):
    with open(svg_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    # Substitui os placeholders pelos dados fornecidos
    svg_content = svg_content.replace('{{NOME_COMPLETO}}', nome)
    svg_content = svg_content.replace('{{CARGO}}', cargo)
    svg_content = svg_content.replace('{{TELEFONE}}', telefone)
    svg_content = svg_content.replace('{{EMAIL}}', email)

    return svg_content

# Função para converter SVG para PNG usando imgkit
def svg_para_png(svg_content):
    # Cria um arquivo temporário para o PNG
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file_path = temp_file.name
        
        # Configurar o caminho do executável do wkhtmltoimage
        config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')

        # Define opções para redimensionamento da imagem
        options = {
            'format': 'jpg',
            'width': '120',  # Largura da imagem
            'height': '194',  # Altura da imagem
            'quality': '100',            
            'zoom': '1.6',
            'crop-x': '90',
            'crop-y': '20'
        }        
        imgkit.from_string(svg_content, temp_file_path, config=config, options=options)

    with open(temp_file_path, 'rb') as img_file:
        img_bytes = img_file.read()
        
    # Remove o arquivo temporário
    os.remove(temp_file_path)

    return img_bytes

st.title("Websign ✍💯")

nome = st.text_input("Nome Completo")
cargo = st.text_input("Empresa")
telefone = st.text_input("Telefone Empresarial")
email = st.text_input("Email Corporativo")

# Caminho do arquivo SVG modelo
svg_path = "modelo.svg"  # Certifique-se que o arquivo SVG esteja no mesmo diretório

if st.button("Gerar Assinatura"):
    if nome and cargo and telefone and email:
        # Edita o SVG com os dados fornecidos
        svg_editado = editar_svg(svg_path, nome, cargo, telefone, email)
        
        # Converte o SVG editado para PNG
        png_bytes = svg_para_png(svg_editado)
        
        # Exibe a imagem gerada
        st.image(png_bytes, caption='Assinatura Gerada', use_column_width=True)

        # Botão para download da imagem PNG
        st.download_button(
            label="Baixar Assinatura PNG",
            data=png_bytes,
            file_name="assinatura.png",
            mime="image/png"
       
        )
    else:
        st.error("Por favor, preencha todos os campos.")
