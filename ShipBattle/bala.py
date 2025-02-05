import pygame as pg
from propiedades import ANCHO_PANTALLA

class Bala(pg.sprite.Sprite):
    def __init__(self, pos, ancho, alto, bando):
        super().__init__()
        self.x = pos[0] #toma las posiciones de las balas
        self.y = pos[1]
        
        self.image = pg.image.load('img/bala.jpeg') #carga la imagen
        self.image = pg.transform.scale(self.image, (ancho, alto)) #la escala
        self.rect = self.image.get_rect(topleft = pos) #la coloca
        self.mask = pg.mask.from_surface(self.image) #crea un objeto mask para pintar la bala y detectar las colisiones
        
        if bando == "nave1": #si la bala pertenece a nave1 se mueve hacia la der
            self.move_speed = 20
        elif bando == "nave2": #si la bala pertenece a nave2 se mueve hacia la izq
            self.move_speed = (-20)

    def mover_bala(self): #pos de la bala respecto a la vel de la bala
        self.rect.x += self.move_speed

    def update(self): #método para pintar la bala en la pantalla en movimiento
        self.mover_bala()
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        if self.rect.x <= 0 or self.rect.x >= ANCHO_PANTALLA: #si salen de la pantalla se "mata" el sprite para evitar sobrecargar la app
            self.kill()