from OpenGL.GL import *
from core.Loader import carrega_textura

class Chinelo:
    def __init__(self, config):
        self.config = config

        self.imune = False
        self.imune_time = 0
        self.imune_duration = config["IMUNIDADE"]


        self.xpos = config["WINDOW_LARGURA"] / 2 - 256 #metade da tela e posiciona o chinelo mais a esquerda
        self.ypos = config["WINDOW_ALTURA"] / 2

        self.largura = config["CHINELO_LARGURA"]
        self.altura = config["CHINELO_ALTURA"]

        self.velocidade = 0

        self.gravidade = config["GRAVIDADE"]

        self.pulo = config["CHINELO_JUMP"]

        self.giro = 0 #valor em graus

        self.textura = carrega_textura("assets/chinelo.png")


    #   APLICA GRAVIDADE PARA ALTERAR VELOCIDADE E POS Y COM BASE NO DELTA_TIME
    #   IMPEDE QUE O CHINELO ULTRAPASSE OS LIMITES Y
    #   CONTROLA A IMUNIDADE
    def update(self, delta_time):
        self.velocidade += self.gravidade * delta_time * 60
        self.ypos += self.velocidade * delta_time * 60

        # Evitar sair da tela -- validar para remover vida se chegar nesses limites mais tarde
        if self.ypos < 0:
            self.ypos = 0
            self.velocidade = 0
        elif self.ypos + self.altura > self.config["WINDOW_ALTURA"]:
            self.ypos = self.config["WINDOW_ALTURA"] - self.altura
            self.velocidade = 0

        if self.imune:
            self.imune_time -= delta_time
            if self.imune_time <= 0:
                self.imune = False


    #   FAZO CHINELO PULAR CONFORME PARÂMETRO
    #   GIRA 30 GRAUS A CADA INTERAÇÃO
    def pular(self):
        self.velocidade = self.pulo
        self.giro -= 30  # rotação horária ?

    #   CENTRALIZA ROTAÇÃO DO CHINELO
    #   APLICA TEXTURA E BLENDING PARA TIRAR FUNDO PRETO BUGADO
    #   APLICA FILTRO VERMELHO EM CASO DE HIT
    def renderizar(self):
        chinelo_x = self.xpos + self.largura / 2
        chinelo_y = self.ypos + self.altura / 2

        glPushMatrix()
        glTranslatef(chinelo_x, chinelo_y, 0)   #para rotacionar no próprio eixo
        glRotatef(self.giro, 0, 0, 1)
        glTranslatef(-chinelo_x, -chinelo_y, 0) #reseta as coordenadas da translação

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.textura)

        if self.imune:
            # Brilha vermelho com alpha
            glColor4f(1.0, 0.2, 0.2, 0.5)
        else:
            glColor4f(1.0, 1.0, 1.0, 1.0)

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
        glPopMatrix()

    #   ATIVA A IMUNIDADE DO CHINELO
    def ativa_imunidade(self):
        self.imune = True
        self.imune_time = self.imune_duration
