import yaml
import re
import json
import openai
import streamlit as st
from src.LLM import Estilista

def extract_image_paths(text):
    # Usando regex para encontrar os caminhos das imagens
    pattern = r'Link para imagem do item: (images/[\w\d]+\.jpg)'
    paths = re.findall(pattern, text)
    return paths

# Configuração da API da OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

st.markdown("# My Closet")
st.sidebar.markdown("# Planejando meu look")

# Page title
st.title('Bora preparar um look juntos')

st.image('./Image/legalmenteLoira.jpg', caption='Clueless-style')

# Load personas from the YAML file
with open("src/estilos.yaml", "r", encoding="utf-8") as file:
    estilos = yaml.safe_load(file)

# Load wardrobe from the JSON file
with open("/home/dell/Documentos/Mestrado/ProjetoAM/clothes_data.json", "r", encoding="utf-8") as file:
    wardrobe = json.load(file)

# Select persona
selected_persona = st.sidebar.selectbox("Selecione a Persona:", list(estilos.keys()))

# Text inputs
input_text = st.text_area('Me conte sobre seu evento / programação do dia:', height=200)
input_text2 = st.text_area('Me conte se existe alguma restrição:', height=100)

# Check if the selected persona is available
if selected_persona in estilos:
    persona_text = estilos[selected_persona]["text"]
    engine = "gpt-3.5-turbo"
    chatbot = Estilista(engine, persona_text)


    if st.button("Gerar Resposta"):
        # Get Prompt from User
        prompt = input_text
        prompt2 = input_text2

        # Generate Response from ChatBot
        print("----------------------------------------------------------")
        print(len(prompt2))
        print("----------------------------------------------------------")
        
        if len(prompt) > 0:
            response = chatbot.generate_response(prompt)
            st.info(f"Look Sugerido (Sem levar em consideração as restrições):\n{response}")
        

        if len(prompt2) > 0:
            response2 = chatbot.generate_nova_resposta(prompt2)
            st.info(f"Look Sugerido (Com as restrições):\n{response2}")

        # Converter os itens do armário em uma string de texto
        wardrobe_text = "\n".join([f"{item['categoria']}: {item['description']}, localizado em {item['file_path']}" for item in wardrobe])
        response3 = chatbot.busca_do_armario(response, wardrobe_text)
        image_paths = extract_image_paths(response3)
        print(image_paths) 
        st.info(f"Itens do armário:\n{response3}")

        # Mostrando as imagens na página Streamlit
        st.title('Itens do Armário')

        for path in image_paths:
            st.image(path)

else:
    st.error("Estilo selecionada não está disponível.")