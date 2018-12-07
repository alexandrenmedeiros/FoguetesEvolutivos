""" Algoritimo evolutivo para encontrar caminho no espaco vetorial
    e interface grafica exibindo o progresso.
    ICMC USP 2018
    Alexandre Norcia Medeiros 10295583
    Giovani Decico Lucafo     10288779
    Luiz Henrique Lourencao   10284862
"""

import sys
import pygame
import random

# variaveis globais para controle do ag
TAM_POP = 10 # qtd de individuos em cada geracao
TAM_CROM = 500 # tamanho do cromossomo (qtd de vetores)
QTD_GER = 5 # qtd de geracoes para exibir
TAXA_MUT_VETOR = 0.4

POPULACAO = []

INFINITO = 1000000000.0 # maior distancia

FOGUETE_X = 10.0 # x,y iniciais dos foguetes
FOGUETE_Y = 10.0

OBJETIVO_X = 10.0 # coord do objetivo
OBJETIVO_Y = 700.0

# variaveis globais para controle da interface
TELA_X = 1200
TELA_Y = 750

PERIGO_X = 600
PERIGO_Y = 375
PERIGO_K = 10000

COR_DE_FUNDO = (15, 10, 90)

IMAGEM_FOGUETE = pygame.image.load('imagens/laranja.png')
IMAGEM_MELHOR_FOGUETE = pygame.image.load('imagens/verde.png')
IMAGEM_OBJETIVO = pygame.image.load('imagens/lua50.png')
IMAGEM_PERIGO = pygame.image.load('imagens/s100.png')


class Foguete():
    """ Classe que representa um individuo na populacao """
    global INFINITO, FOGUETE_X, FOGUETE_Y, TAM_CROM, TELA_Y, OBJETIVO_X, OBJETIVO_Y
    
    def __init__(self):
        """ Cria o individuo """

        self.nota = INFINITO # avaliacao, qnt menor melhor
        self.x = FOGUETE_X # x e y para mover na avaliacao
        self.y = FOGUETE_Y
        self.x2 = FOGUETE_X # x e y para mover na avaliacao
        self.y2 = FOGUETE_Y
        self.cromossomo = [] # lista com os vetores

        self.img = IMAGEM_FOGUETE
        self.rect = self.img.get_rect() # rect para exibir na tela

        # gera os cromossomos iniciais
        i = 0
        while i < TAM_CROM:
            i += 1
            x = random.uniform(-1, 1)  # float rand entre -1 e 1 para vetor
            y = random.uniform(-1, 1)
            n = random.uniform(20, TELA_Y/TAM_CROM)
            aux = [x, y, n]
            self.cromossomo.append(aux)
    
    def exibe_atributos(self):
        """ Funcao auxiliar para exibir individuo """
        print("nota = ", self.nota)
        for gene in self.cromossomo:
                print(gene[0], " ", gene[1], " ", gene[2])

    def avalia(self):
        """ Funcao auxiliar para avaliar individuo """
        for gene in self.cromossomo:
            # adiciona o vetor (move)
            self.x += gene[0] * gene[2]
            self.y += gene[1] * gene[2]
            
        dist = (self.x - OBJETIVO_X)**2 + (self.y - OBJETIVO_Y)**2
        self.nota = dist + PERIGO_K/((self.x - PERIGO_X)**2 + (self.y - PERIGO_Y)**2)

        if self.img == IMAGEM_MELHOR_FOGUETE:
            print("nota: ", self.nota, "x: ", self.x, " y: ", self.y, " obj x:", OBJETIVO_X, " obj y:", OBJETIVO_Y)
        # reseta o x e y dps
        self.x = FOGUETE_X 
        self.y = FOGUETE_Y
        self.x2 = FOGUETE_X 
        self.y2 = FOGUETE_Y
        self.rect.centerx = FOGUETE_X
        self.rect.centery = FOGUETE_Y
        self.img = IMAGEM_FOGUETE

def selecao_e_cross():
    """ Funcao que faz a reproducao na populacao """
    global INFINITO, FOGUETE_X, FOGUETE_Y, POPULACAO, IMAGEM_MELHOR_FOGUETE

    # selecao: melhor de todos
    melhor_nota = INFINITO

    for indiv in POPULACAO: # encontra o melhor de todos
        if indiv.nota < melhor_nota:
            melhor_nota = indiv.nota
            melhor_indiv = indiv
    
    #print("melhor nota: ", melhor_nota)
    #melhor_indiv.exibe_atributos()

    # reproducao: media normal com o melhor de todos
    for indiv in POPULACAO:
        if indiv.nota != melhor_nota:
            indiv.nota = INFINITO
            for gene, melhor_gene in zip(indiv.cromossomo, melhor_indiv.cromossomo):
                gene[0] = (gene[0] + melhor_gene[0]) / 2
                gene[1] = (gene[1] + melhor_gene[1]) / 2
                gene[2] = (gene[2] + melhor_gene[2]) / 2
        else:
            indiv.img = IMAGEM_MELHOR_FOGUETE
        
def mutacao():
    """ Funcao que faz a mutacao na populacao """
    global INFINITO, TAXA_MUT_VETOR, POPULACAO

    # todos mutam, menos o melhor de todos
    for indiv in POPULACAO:
        if indiv.nota == INFINITO:
            for gene in indiv.cromossomo:
                gene[0] += random.uniform(-1 * TAXA_MUT_VETOR, 1 * TAXA_MUT_VETOR)
                gene[1] += random.uniform(-1 * TAXA_MUT_VETOR, 1 * TAXA_MUT_VETOR)
                gene[2] += random.uniform(-1, 1)
                # analisa limitacoes
                if gene[0] > 1:
                    gene[0] = 1
                elif gene[0] < -1:
                    gene[0] = -1
                if gene[1] > 1:
                    gene[1] = 1
                elif gene[1] < -1:
                    gene[1] = -1
                if gene[2] < 1:
                    gene[2] = 1

def exibe(tela):
    """ Funcao auxiliar que exibe na tela o caminho da populacao atual """
    global FOGUETE_X, FOGUETE_Y, COR_DE_FUNDO, TAM_CROM, POPULACAO, IMAGEM_OBJETIVO, OBJETIVO_X, OBJETIVO_Y, PERIGO_X, PERIGO_Y

    obj_rect = IMAGEM_OBJETIVO.get_rect()
    obj_rect.centerx = OBJETIVO_X
    obj_rect.centery = OBJETIVO_Y

    obj2_rect = IMAGEM_PERIGO.get_rect()
    obj2_rect.centerx = PERIGO_X
    obj2_rect.centery = PERIGO_Y

    # se quiser exibir apenas o melhor
    #for pessoa in POPULACAO:
    #    if pessoa.nota != INFINITO:
    #        indiv = pessoa

    i = 0
    while i < TAM_CROM: # exibe cada movimento de cada individuo
        tela.fill(COR_DE_FUNDO)
        for indiv in POPULACAO: # exibe todos individuos
            indiv.x2 += indiv.cromossomo[i][0] * indiv.cromossomo[i][2]
            indiv.y2 += indiv.cromossomo[i][1] * indiv.cromossomo[i][2]
            indiv.rect.centerx = indiv.x2
            indiv.rect.centery = indiv.y2
            tela.blit(indiv.img, indiv.rect)
            
        tela.blit(IMAGEM_OBJETIVO, obj_rect)
        tela.blit(IMAGEM_PERIGO, obj2_rect)
        pygame.display.flip()
        i += 1

def evolutivo():
    """ Funcao principal que faz o loop do algoritimo evolutivo """
    global TELA_X, TELA_Y, TAM_POP, QTD_GER, IMAGEM_OBJETIVO, OBJETIVO_X, OBJETIVO_Y, POPULACAO, FOGUETE_X, FOGUETE_Y, PERIGO_X, PERIGO_Y

    pygame.init()  # inicializa os modulos do pygame corretamente
    # objeto que representa a tela
    tela = pygame.display.set_mode((TELA_X, TELA_Y))  # ((,)) pq eh um pair
    pygame.display.set_caption("FOGUETES EVOLUTIVOS!!")  # nome da janela
    
    # cria a populacao inicial
    i = 0
    while i < TAM_POP:
        aux = Foguete()
        POPULACAO.append(aux)
        i += 1
    
    #exibe(tela)

    i = 0
    # loop principal do alg evo e da janela que exibe
    while True:
        i += 1

        # verifica teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # fecha jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1: # botao esquerdo do mouse
                    # muda origem dos foguetes
                    FOGUETE_X = x
                    FOGUETE_Y = y
                elif event.button == 2: # scroll click
                    # muda origem do perigo.
                    PERIGO_X = x
                    PERIGO_Y = y
                elif event.button == 3: # botao direito do mouse
                    # muda origem do objetivo
                    OBJETIVO_X = x
                    OBJETIVO_Y = y

        # avalia
        for indiv in POPULACAO:
            indiv.avalia()
        # selecao (MELHOR DE TODOS) e reproducao
        selecao_e_cross()
        # mutacao
        mutacao()

        if i % QTD_GER == 0:
            exibe(tela)

# primeira funcao a ser executada
evolutivo()
