import streamlit as st
import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration

# Carregar modelo BLIP
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Carregar modelo T5
t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
t5_tokenizer = T5Tokenizer.from_pretrained("t5-base", model_max_length=512)

# Função para salvar imagem
def save_uploaded_file(uploaded_file, directory="images"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Função para gerar uma legenda básica da peça usando BLIP
def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = blip_processor(images=image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

# Função para expandir a legenda em uma descrição detalhada usando T5
def generate_description(caption):
    #prompt = f"Expand the following caption into a detailed description: {caption}"
    #input_ids = t5_tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
    #output = t5_model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    #description = t5_tokenizer.decode(output[0], skip_special_tokens=True)
    
    return caption


# Carregar ou criar JSON
json_path = "clothes_data.json"
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        clothes_data = json.load(f)
else:
    clothes_data = []

# Upload de imagem
uploaded_file = st.file_uploader("Upload a piece of clothing", type=["png", "jpg", "jpeg"])
description = ""

if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.image(file_path, caption="Uploaded Image", use_column_width=True)
    
    # Gerar descrição automaticamente
    caption = generate_caption(file_path)
    description = generate_description(caption)
    st.text_area("Description of the piece", description)
    
    # Selecionar tipo de peça
    piece_type = st.selectbox("Select the type of clothing", ["Unknown", "Shirt", "Pants", "Dress", "Skirt", "Jacket", "Coat", "Shoes", "Accessories"])
    
    # Salvar peça
    if piece_type != "Unknown" and description:
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
