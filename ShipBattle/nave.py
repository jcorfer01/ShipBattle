import pygame as pg
from propiedades import ANCHO_NAVE, ALTO_NAVE, VEL_NAVE, ANCHO_BALA, ALTO_BALA
from bala import Bala

class Nave(pg.sprite.Sprite):
    def __init__(self, pos, bando, volumen_sfx): #constructor
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.disparo_sonido = pg.mixer.Sound("music\Sonido_Disparo.mp3") #var para el sonido de bala
        self.disparo_sonido.set_volume(volumen_sfx)
        self.image = pg.Surface([ALTO_NAVE, ANCHO_NAVE])
        self.image.fill("black")
        self.image.set_colorkey("black")
        self.bando = bando #bando necesario para saber si es izquierda o derecha
        self.inmunidad = False
        
        if bando == "nave1": #si es nave2 es la nave de la izquierda, por lo que se pinta de forma distinta
            self.image = pg.image.load("img/Nave_Izquierda.png")
            self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
            ''' DIBUJO SVG
            pg.draw.polygon(self.image, (255, 140, 26), [(0,0),(0,ALTO_NAVE/3),(ANCHO_NAVE/3,ALTO_NAVE/3)]) #ala superior
            pg.draw.polygon(self.image, (255, 140, 26), [(0,ALTO_NAVE),(0,(2*ALTO_NAVE)/3),(ANCHO_NAVE/3,(2*ALTO_NAVE)/3)]) #ala inferior
            pg.draw.polygon(self.image, (0, 102, 255), [(0,ALTO_NAVE/3),(0,(2*ALTO_NAVE)/3),((2*ANCHO_NAVE)/3,(2*ALTO_NAVE)/3),((2*ANCHO_NAVE)/3,ALTO_NAVE/3)]) #tronco
            pg.draw.polygon(self.image, (255, 140, 26), [((2*ANCHO_NAVE)/3,ALTO_NAVE/3),((2*ANCHO_NAVE)/3,(2*ALTO_NAVE)/3),(ANCHO_NAVE,(ALTO_NAVE)/2)]) #punta
            '''
        else: #si es nave1 es la nave de la derecha
            self.image = pg.image.load("img/Nave_Derecha.png")
            self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
            '''
            pg.draw.polygon(self.image, (230, 230, 0), [(ANCHO_NAVE,0),(ANCHO_NAVE,ALTO_NAVE/3),((2*ANCHO_NAVE)/3,ALTO_NAVE/3)]) #ala superior
            pg.draw.polygon(self.image, (230, 230, 0), [(ANCHO_NAVE,ALTO_NAVE),(ANCHO_NAVE,(2*ALTO_NAVE)/3),((2*ANCHO_NAVE)/3,(2*ALTO_NAVE)/3)]) #ala inferior
            pg.draw.polygon(self.image, (51, 204, 51), [(ANCHO_NAVE,ALTO_NAVE/3),(ANCHO_NAVE,(2*ALTO_NAVE)/3),(ANCHO_NAVE/3,(2*ALTO_NAVE)/3),(ANCHO_NAVE/3,ALTO_NAVE/3)]) #tronco
            pg.draw.polygon(self.image, (230, 230, 0), [(ANCHO_NAVE/3,ALTO_NAVE/3),(ANCHO_NAVE/3,(2*ALTO_NAVE)/3),(0,(ALTO_NAVE)/2)]) #punta
            '''
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pg.mask.from_surface(self.image) #objeto tipo mask para las colisiones
        self.velocidad_nave = VEL_NAVE
        self.grupo_balas = pg.sprite.Group() #se crea el grupo de balas
        self.vida = 3 #número de vidas

    # definimos los movimientos de la nave
    def izq(self): #izquierda
        self.rect.x -= self.velocidad_nave
    def der(self): #derecha
        self.rect.x += self.velocidad_nave
    def arr(self): #arriba
        self.rect.y -= self.velocidad_nave
    def abj(self): #abajo
        self.rect.y += self.velocidad_nave
        
    def disparar(self): #método para disparar
        pos_nave = (self.rect.centerx, self.rect.centery - ANCHO_BALA // 2) #se pone la bala delante de la nave
        self.grupo_balas.add(Bala(pos_nave, ANCHO_BALA, ALTO_BALA, self.bando))
        self.disparo_sonido.play() #se empieza el sonido de disparo
    
    def restar_vida(self):
        if self.vida > 0:
            self.grupo_balas.empty() #si impacta una bala sobre la nave enemiga, se quitan todas las balas que tengas en pantalla para que no puedas pegarle doble
            self.vida = self.vida - 1

    def update(self): #método para actualiarla posición de la nave y redibujarla donde y cómo se encuentre
        if self.inmunidad: #si es inmune
            if self.bando == "nave1": #si es nave2 es la nave de la izquierda, por lo que se pinta de forma distinta
                self.image = pg.image.load("img/Nave_Izquierda_Inmune.png")
                self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
            else: #si es nave1 es la nave de la derecha
                self.image = pg.image.load("img/Nave_Derecha_Inmune.png")
                self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
        elif self.inmunidad == False: #si NO es inmune
            if self.bando == "nave1": #si es nave2 es la nave de la izquierda, por lo que se pinta de forma distinta
                self.image = pg.image.load("img/Nave_Izquierda.png")
                self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
            else: #si es nave1 es la nave de la derecha
                self.image = pg.image.load("img/Nave_Derecha.png")
                self.image = pg.transform.scale(self.image, (ALTO_NAVE, ANCHO_NAVE))
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))   