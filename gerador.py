import streamlit as st
import imgkit
import os
import tempfile

def editar_svg(svg_path, nome, cargo, telefone, email):
    with open(svg_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    svg_content = svg_content.replace('{{NOME_COMPLETO}}', nome)
    svg_content = svg_content.replace('{{CARGO}}', cargo)
    svg_content = svg_content.replace('{{TELEFONE}}', telefone)
    svg_content = svg_content.replace('{{EMAIL}}', email)

    return svg_content

def svg_para_png(svg_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file_path = temp_file.name
        
        config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')

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
        
    os.remove(temp_file_path)

    return img_bytes

st.title("Websign ✍💯")

nome = st.text_input("Nome Completo")
cargo = st.text_input("Empresa")
telefone = st.text_input("Telefone Empresarial")
email = st.text_input("Email Corporativo")

svg_path = "modelo.svg"

if st.button("Gerar Assinatura"):
    if nome and cargo and telefone and email:
        svg_editado = editar_svg(svg_path, nome, cargo, telefone, email)
        
        png_bytes = svg_para_png(svg_editado)
        
        st.image(png_bytes, caption='Assinatura Gerada', use_column_width=True)

        st.download_button(
            label="Baixar Assinatura PNG",
            data=png_bytes,
            file_name="assinatura.png",
            mime="image/png"
       
        )
    else:
        st.error("Por favor, preencha todos os campos.")
