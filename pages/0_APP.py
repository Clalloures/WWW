import yaml
import streamlit as st
from src.LLM import Estilista

st.markdown("# My Closet")
st.sidebar.markdown("# Planejando meu look")


# Page title
#st.set_page_config(page_title='🦜🔗 Ask the Doc App')
st.title('Bora preparar um look juntos')

st.image('./Image/legalmenteLoira.jpg', caption='Clueless-style')

# File upload
# input_text = st.file_uploader('Upload an article', type='txt')

# Carregar personas do arquivo YAML
with open("src/estilos.yaml", "r", encoding="utf-8") as file:
    estilos = yaml.safe_load(file)


# Selecionar persona
selected_persona = st.sidebar.selectbox("Selecione a Persona:", list(estilos.keys()))


# Text input
input_text = st.text_area('Me conte sobre seu evento / programação do dia:', height=200)


# Text input
input_text2 = st.text_area('Me conte se existe alguma restrição:', height=200)


# Verificar se a persona selecionada está disponível
if selected_persona in estilos:
    persona_text = estilos[selected_persona]["text"]
    engine = "gpt-3.5-turbo"
    chatbot = Estilista(engine, persona_text)

    if st.button("Gerar Resposta"):
        # Get Prompt from User
        prompt = input_text

        # Generate Response from ChatBot
        response = chatbot.generate_response(prompt)

        prompt2 = input_text2

        # Generate Response from ChatBot
        response2 = chatbot.generate_nova_resposta(prompt2)


        # Display Response
        if len(response) > 0:
            st.info(f"Texto reescrito:\n{response}")

        # Display Response
        if len(response) > 0:
            st.info(f"Texto reescrito:\n{response2}")

else:
    st.error("Estilo selecionada não está disponível.")



# https://www.youtube.com/watch?v=8PgO_zIeAA8
            
