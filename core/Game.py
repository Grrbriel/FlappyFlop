import glfw
from core.Window import init_window, setup_opengl
from core.Loader import carregar_config, carrega_textura, carregar_numeros
from entities.Chinelo import Chinelo
import time
from entities.Muro import Muro
from OpenGL.GL import *
from entities.Coletavel import Coletavel

class Game:
    def __init__(self):

        self.pontos = 0
        self.jogando = True
        self.config = carregar_config()
        self.vidas = self.config["VIDAS"]
        self.window = init_window(self.config["WINDOW_LARGURA"], self.config["WINDOW_ALTURA"])

        setup_opengl(self.config["WINDOW_LARGURA"], self.config["WINDOW_ALTURA"])

        self.img_fundo = carrega_textura("assets/background2.png")
        self.fundo_pos = 0  # posição horizontal do fundo

        self.game_over_img = carrega_textura("assets/gameover.png")
        self.chinelo_img = carrega_textura("assets/chinelo.png")
        self.muro_img = carrega_textura("assets/muro.png")
        self.numero_img = carregar_numeros("assets/digitos/")
        self.heart_img = carrega_textura("assets/coracao.png")
        self.itens = [
            Coletavel(self.config, self.heart_img)
        ]
        self.chinelo = Chinelo(self.config)

        self.muros = [
            Muro(self.config, self.config["WINDOW_LARGURA"], self.muro_img),
            Muro(self.config, self.config["WINDOW_LARGURA"] + 300, self.muro_img),
            Muro(self.config, self.config["WINDOW_LARGURA"] + 600, self.muro_img)
        ]

        self.last_time = time.time()
        self.delta_time = 0

    def run(self):
        while not glfw.window_should_close(self.window):
            current_time = time.time()
            self.delta_time = current_time - self.last_time
            self.last_time = current_time

            self.handle_input()
            self.update()
            self.render()
            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def handle_input(self):
        if glfw.get_key(self.window, glfw.KEY_SPACE) == glfw.PRESS and self.jogando:
            self.chinelo.pular()

        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def update(self):
        if not self.jogando:
            return

        self.chinelo.update(self.delta_time)

        for muro in self.muros:
            muro.update(self.delta_time)

            if not muro.ultrapassado and self.chinelo.xpos > muro.xpos + muro.largura:
                self.pontos += 1
                muro.ultrapassado = True

            if not self.chinelo.imune and muro.colidiu(self.chinelo):
                if self.vidas > 0:
                    self.vidas -= 1
                    self.chinelo.ativa_imunidade()

                if self.vidas == 0:
                    self.jogando = False

            for item in self.itens:
                item.update(self.delta_time)
                if item.colidiu(self.chinelo):
                    self.vidas += 1

        fundo_vel = self.config["MURO_SPEED"] * 0.25 * 60  # pixels por segundo
        self.fundo_pos += fundo_vel * self.delta_time

        # reset no loop
        fundo_largura = self.config.get("WINDOW_LARGURA")
        if self.fundo_pos > fundo_largura:
            self.fundo_pos -= fundo_largura

    def render(self):
        self.renderizar_fundo()
        self.chinelo.renderizar()

        for item in self.itens:
            item.renderizar()

        for muro in self.muros:
            muro.renderizar()

        if not self.jogando:
            self.renderizar_gameover()
            self.renderizar_pontos()
            self.renderizar_vidas()
        else:
            self.renderizar_pontos()
            self.renderizar_vidas()


    def renderizar_gameover(self):
        go_largura, go_altura = 400, 200
        x = (self.config["WINDOW_LARGURA"] - go_largura) / 2
        y = (self.config["WINDOW_ALTURA"] - go_altura) / 2

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.game_over_img)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(x, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + go_largura, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + go_largura, y + go_altura)
        glTexCoord2f(0, 1)
        glVertex2f(x, y + go_altura)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def renderizar_pontos(self):
        x = 0
        y = self.config["WINDOW_ALTURA"] - 50  # canto superior esquerdo

        for numero in str(self.pontos):
            img, largura, altura = self.numero_img[int(numero)]
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, img)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor3f(1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(x, y)
            glTexCoord2f(1, 0)
            glVertex2f(x + largura, y)
            glTexCoord2f(1, 1)
            glVertex2f(x + largura, y + altura)
            glTexCoord2f(0, 1)
            glVertex2f(x, y + altura)
            glEnd()
            glDisable(GL_BLEND)
            glDisable(GL_TEXTURE_2D)
            x += largura  # espaço entre os números

    def renderizar_vidas(self):
        numero = str(self.vidas)
        largura, altura = 50, 50

        # Canto superior direito
        total_largura = len(numero) * (largura) + largura   #qtd numeros * a largura + largura do coração
        x = self.config["WINDOW_LARGURA"] - total_largura
        y = self.config["WINDOW_ALTURA"] - 60 #posicionar no topo da tela com uma folga

        # Desenha o coração
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.heart_img)
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(x, y)
        glTexCoord2f(1, 0)
        glVertex2f(x + largura, y)
        glTexCoord2f(1, 1)
        glVertex2f(x + largura, y + altura)
        glTexCoord2f(0, 1)
        glVertex2f(x, y + altura)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        x += largura  # espaço entre coração e dígitos

        # Desenha o número de vidas
        for digito in numero:
            img, _, _ = self.numero_img[int(digito)] # precisa do _ para ignorar atributo da tupla
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glBindTexture(GL_TEXTURE_2D, img)
            glColor4f(1, 1, 1, 1)

            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(x, y)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(x + largura, y)
            glTexCoord2f(1.0, 1.0)
            glVertex2f(x + largura, y + altura)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(x, y + altura)
            glEnd()

            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

            x += largura

    def renderizar_fundo(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.img_fundo)
        glColor4f(1, 1, 1, 1)

        largura = self.config["WINDOW_LARGURA"]
        altura = self.config["WINDOW_ALTURA"]
        offset = -self.fundo_pos

        for i in range(2):  # desenha duas vezes, lado a lado
            x = offset + i * largura
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(x, 0)
            glTexCoord2f(1, 0)
            glVertex2f(x + largura, 0)
            glTexCoord2f(1, 1)
            glVertex2f(x + largura, altura)
            glTexCoord2f(0, 1)
            glVertex2f(x, altura)
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
