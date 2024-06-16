import os
import sys
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import *
from collections import Counter
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from fashion_clip.fashion_clip import FashionCLIP, FCLIPDataset
from fashion_clip.utils import get_cache_directory, display_images



fclip = FashionCLIP('fashion-clip')

# Loading a local dataset
catalog = [
    {'id': 1, 'image': '16867424.jpg','type': 'T-shirt', 'caption': 'light red polo shirt'},
    {'id': 2, 'image': '16790484.jpg','type': 'Shoes', 'caption': 'an adidas sneaker'},
    {'id': 3, 'image': '16198646.jpg','type': 'T-shirt', 'caption': 'dark red polo shirt'},
    {'id': 4, 'image': '123456.jpg','type': 'Dress', 'caption': 'a colorful dress' }
]
dataset = FCLIPDataset('farfetch_local',
                       image_source_path='./images',
                       image_source_type='local',
                       catalog=catalog)

# Diretório onde as imagens estão localizadas
image_source_path = './images/'

# Criando uma lista das imagens
images = [os.path.join(image_source_path, item['image']) for item in catalog]

# Criando uma lista das descrições
texts = [item['caption'] for item in catalog]

# we create image embeddings and text embeddings
image_embeddings = fclip.encode_images(images, batch_size=32)
text_embeddings = fclip.encode_text(texts, batch_size=32)

# we normalize the embeddings to unit norm (so that we can use dot product instead of cosine similarity to do comparisons)
image_embeddings = image_embeddings/np.linalg.norm(image_embeddings, ord=2, axis=-1, keepdims=True)
text_embeddings = text_embeddings/np.linalg.norm(text_embeddings, ord=2, axis=-1, keepdims=True)

fixed_height = 224

text_embedding = fclip.encode_text(["a dress"], 32)[0]
threshold = 2  # Defina o limite de similaridade aqui

# Calcula o produto escalar entre o texto e os embeddings de imagem
similarities = text_embedding.dot(image_embeddings.T)

# Encontra o índice da imagem com o maior produto escalar
id_of_matched_object = np.argmax(similarities)

# Obtém a maior similaridade encontrada
max_similarity = similarities[id_of_matched_object]

# Verifica se a maior similaridade é maior que o limite definido
if max_similarity > threshold:
    # Se a similaridade é alta o suficiente, mostra a imagem correspondente
    image = catalog[id_of_matched_object]['image']
    image = Image.open(f"{image_source_path}{image}")
    height_percent = (fixed_height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    image = image.resize((width_size, fixed_height), Image.NEAREST)
    print(max_similarity)

else:
    # Se a similaridade não é alta o suficiente, não mostra nenhuma imagem
    print("Nenhuma imagem encontrada com similaridade suficiente.")
