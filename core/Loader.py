import json
from OpenGL.GL import *
from PIL import Image
import numpy as np

def carregar_config(path="assets/config.json"):
    with open(path, "r") as file:
        return json.load(file)

def carrega_textura(path):
    image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    image_data = np.array(image).flatten()
    largura, altura = image.size

    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return textura

def carregar_numeros(folder_path="assets/digitos/"):
    textura_numeros = []
    for i in range(10):
        path = f"{folder_path}{i}.png"
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        largura, altura = image.size
        data = np.array(image).flatten()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        textura_numeros.append((texture, largura, altura))  # salva tamanho junto
    return textura_numeros
