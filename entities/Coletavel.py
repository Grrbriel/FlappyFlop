from OpenGL.GL import *
import random

class Coletavel:
    def __init__(self, config, textura):
        self.config = config
        self.textura = textura
        self.largura = 48
        self.altura = 48
        self.reset()

    def reset(self):
        self.x = self.config["WINDOW_LARGURA"] + 10000
        self.y = random.randint(50, self.config["WINDOW_ALTURA"] - 50)
        self.coletado = False

    def update(self, delta_time):
        self.x -= self.config["MURO_SPEED"] * delta_time * 60
        if self.x + self.largura < 0:
            self.reset()

    def colidiu(self, chinelo):
        if self.coletado:
            return False

        cx, cy, cw, ch = chinelo.xpos, chinelo.ypos, chinelo.largura, chinelo.altura
        if (self.x < cx + cw and self.x + self.largura > cx and
            self.y < cy + ch and self.y + self.altura > cy):
            self.coletado = True
            return True
        return False

    def renderizar(self):
        if self.coletado:
            return

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.x, self.y)
        glTexCoord2f(1, 0)
        glVertex2f(self.x + self.largura, self.y)
        glTexCoord2f(1, 1)
        glVertex2f(self.x + self.largura, self.y + self.altura)
        glTexCoord2f(0, 1)
        glVertex2f(self.x, self.y + self.altura)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)