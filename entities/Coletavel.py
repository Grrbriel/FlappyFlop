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
        self.xpos = self.config["WINDOW_LARGURA"] + 2500
        self.ypos = random.randint(50, self.config["WINDOW_ALTURA"] - 50)
        self.coletado = False

    def update(self, delta_time):
        self.xpos -= self.config["ITEM_SPEED"] * delta_time * 60
        if self.xpos + self.largura < 0:
            self.reset()

    def colidiu(self, chinelo):
        cx, cy, cl, ca = chinelo.xpos, chinelo.ypos, chinelo.largura, chinelo.altura
        if self.coletado:
            return False

        # Testa colisão horizontal - somar largura e depois checar altura
        if (cx + cl > self.xpos) and (cx < self.xpos + self.largura):
            if cy + ca > self.ypos and cy < self.ypos + self.altura:
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
        glVertex2f(self.xpos, self.ypos)
        glTexCoord2f(1, 0)
        glVertex2f(self.xpos + self.largura, self.ypos)
        glTexCoord2f(1, 1)
        glVertex2f(self.xpos + self.largura, self.ypos + self.altura)
        glTexCoord2f(0, 1)
        glVertex2f(self.xpos, self.ypos + self.altura)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)