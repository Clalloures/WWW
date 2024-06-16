from openai import OpenAI
import openai
import json
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key='sk-proj-Tg76JcRqcIExWXGNYbfMT3BlbkFJ5qEF65eWDiNLpNjAktZs',
)


class Estilista:
    def __init__(self, engine, persona_text):
        # Initialize conversation with a system message
        self.conversation = [{"role": "system", "content": persona_text}]
        self.engine = engine

    def add_message(self, role, content):
        # Adds a message to the conversation.
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        # Add user prompt to conversation
        self.add_message("user", prompt)
        # Make a request to the API using the chat-based endpoint with conversation context
        response = client.chat.completions.create(messages=self.conversation, model=self.engine)
        # Extract the response
        assistant_response = response.choices[0].message.content.strip()
        # Add assistant response to conversation
        self.add_message("assistant", assistant_response)
        # Return the response
        return assistant_response
    
    def generate_nova_resposta(self, prompt2):
        text_ref = "A cliente sugeriu algumas restrições para o look, com base nessas restrições gere uma nova sugestão de look: "
        text_ref = text_ref + prompt2
        # Add user prompt to conversation
        self.add_message("user", text_ref)
        # Make a request to the API using the chat-based endpoint with conversation context
        response = client.chat.completions.create(messages=self.conversation, model=self.engine)
        # Extract the response
        assistant_response = response.choices[0].message.content.strip()
        # Add assistant response to conversation
        self.add_message("assistant", assistant_response)
        # Return the response
        return assistant_response
    
    def busca_do_armario(self, prompt3, lista_itens):
        print(lista_itens)
        text_ref = "Com base na sugestão do estilista busque 1 item de cada TIPO (Uma blusa, um vestipo, uma calç, etc) do armário que sirva de sugestão para o usuário. Lista de itens "+ lista_itens + """
                    Sua mensagem deve seguir o seguinte formato:
                    
                    Tipo de item: [Inserir TIPO]
                    * [Inserir motivo que faz esse item ser uma boa escolha, [SEMPRE coloque essa informação]
                    * Link para imagem do item: []é o caminho que está em "localizado em", sempre coloque o caminho do diretório igual ao do texto, não crie como um link apenas coloque o caminho]
                    
                    Faça isso para cada um dos itens selecionados """
        text_ref = text_ref + prompt3
        # Add user prompt to conversation
        self.add_message("user", text_ref)
        # Make a request to the API using the chat-based endpoint with conversation context
        response = client.chat.completions.create(messages=self.conversation, model=self.engine)
        print(response)
        # Extract the response
        assistant_response = response.choices[0].message.content.strip()
        # Add assistant response to conversation
        self.add_message("assistant", assistant_response)
        # Return the response
        return assistant_response
