from OpenGL.GL import *
import random

class Muro:
    def __init__(self, config, x_poss, textura):
        self.ultrapassado = False
        self.config = config
        self.xpos = x_poss
        self.largura = config["MURO_LARGURA"]
        self.gap = config["GAP"]
        self.velocidade = config["MURO_SPEED"]
        self.textura = textura
        self.reset()

    #   QUANDO O MURO SAIR DA TELA VAI SER RESETADO COM UM GAP ALEATORIO
    def reset(self):
        self.ultrapassado = False
        total_altura = self.config["WINDOW_ALTURA"]
        self.altura_chao = random.randint(100, total_altura - self.gap - 100)
        self.topo_y = self.altura_chao + self.gap

    def update(self, delta_time):
        self.xpos -= self.velocidade * delta_time * 60
        if self.xpos + self.largura < 0:
            self.xpos = self.config["WINDOW_LARGURA"]
            self.reset()

    def colidiu(self, chinelo):
        cx, cy, cl, ca = chinelo.xpos, chinelo.ypos, chinelo.largura, chinelo.altura

        # Testa colisão horizontal (mesmo intervalo X)
        if (cx + cl > self.xpos) and (cx < self.xpos + self.largura):
            # Testa colisão com muro superior
            if cy < self.altura_chao:
                return True
            # Testa colisão com muro inferior
            if cy + ca > self.topo_y:
                return True
        return False

    def renderizar(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        glColor4f(1, 1, 1, 1)

        # Muro cima
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.xpos, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.xpos + self.largura, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.xpos + self.largura, self.altura_chao)
        glTexCoord2f(0, 1)
        glVertex2f(self.xpos, self.altura_chao)
        glEnd()

        # Muro baixo
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.xpos, self.topo_y)
        glTexCoord2f(1, 0)
        glVertex2f(self.xpos + self.largura, self.topo_y)
        glTexCoord2f(1, 1)
        glVertex2f(self.xpos + self.largura, self.config["WINDOW_ALTURA"])
        glTexCoord2f(0, 1)
        glVertex2f(self.xpos, self.config["WINDOW_ALTURA"])
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)