import streamlit as st
import os
import json

# Função para salvar imagem
def save_uploaded_file(uploaded_file, directory="images"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Carregar ou criar JSON
json_path = "clothes_data.json"
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        clothes_data = json.load(f)
else:
    clothes_data = []

# Upload de imagem
uploaded_file = st.file_uploader("Upload a piece of clothing", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.image(file_path, caption="Uploaded Image", use_column_width=True)
    
    # Descrição da peça
    piece_type = st.selectbox("Select type of clothing", ["Blouse", "Pants", "Dress", "Accessory"])
    description = st.text_area("Description of the piece")
    
    if st.button("Save piece"):
        new_piece = {
            "file_path": file_path,
            "type": piece_type,
            "description": description
        }
        clothes_data.append(new_piece)
        
        # Salvar no JSON
        with open(json_path, "w") as f:
            json.dump(clothes_data, f)
        
        st.success("Piece saved successfully!")

# Mostrar peças salvas
if st.checkbox("Show saved pieces"):
    st.write(clothes_data)
