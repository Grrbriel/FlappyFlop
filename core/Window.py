import glfw
from OpenGL.GL import *

def init_window(largura, altura):
    if not glfw.init():
        raise Exception("Falha na inicialização")

    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, "Flappy-Flop", None, None)

    if not window:
        glfw.terminate()
        raise Exception("Erro ao criar a janela")
    glfw.make_context_current(window)
    return window

def setup_opengl(largura, altura):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, largura, 0, altura, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
