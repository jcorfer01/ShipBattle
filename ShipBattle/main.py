import pygame as pg
import sys
from propiedades import ANCHO_PANTALLA, ALTO_PANTALLA
from mundo import Mundo
from menu import Menu

#inicializo los componentes de pygame y creo los componentes visuales del fondo del juego
pg.init()
pg.mixer.init()

pg.display.set_caption("Ship Battle") #nombre de la app
pantalla_juego = pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA + 40)) #creo la ventana del juego con los datos del fichero de propiedades
fondo_juego = pg.transform.scale(pg.image.load("img/Fondo_Espacio.jpg"),(ANCHO_PANTALLA, ALTO_PANTALLA + 40)) #y para el fondo del juego

class Main():
    def __init__(self): #constructor
        self.tag_j1 = ""
        self.tag_j2 = ""
        #cambio de estado
        self.menu_disp = True #inicia la pantalla en el menu
        #opciones
        self.cantidad_FPS = 60 #inicialmente el juego tendrá 60 fps
        self.volumen_musica = 1.0 #y la musica y efectos de sonido estarán al 100% de volumen
        self.volumen_sfx = 1.0
        #objetos para los fps
        self.FPS = pg.time.Clock()
        
    def juego_ejecucion(self): #ejecución de juego
        mundo = Mundo(pantalla_juego,self.tag_j1,self.tag_j2, self.volumen_sfx)
        
        while not self.menu_disp: #mientras que no enseñe el menú, muestra el juego
            pantalla_juego.fill("black")
            pantalla_juego.blit(fondo_juego,(0,0))
            
            for event in pg.event.get(): #detecta si se presiona la X de la ventana para salir
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            mundo.nave_mov() #métodos para que se pueda interactuar con el juego y actualizar pantalla/sprites
            mundo.nave_disp()
            mundo.update()
            pg.display.update()
            self.FPS.tick(self.cantidad_FPS)
            self.menu_disp = mundo.volver_menu #comprueba si el juego ha acabado
    
    def menu_ejecucion(self): #ejecución menú
        menu = Menu(self.cantidad_FPS, round(pg.mixer.music.get_volume(), 1), self.volumen_sfx) #se guardan los ajustes elegidos en el menú de opciones
        
        while self.menu_disp:
            menu.mostrar_menu()
            #valores recibidos en el menú
            self.cantidad_FPS = menu.FPS
            self.tag_j1 = menu.tag_j1
            self.tag_j2 = menu.tag_j2
            #guarda los ajustes seleccionados en el menu de opciones
            self.volumen_sfx = menu.volumen_sfx
            self.menu_disp = menu.menu_disp #comprueba si la variable de la clase mostrar menú, se ha puesto en false para salir
            pg.display.update()

if __name__ == "__main__":
    M = Main()
    while True: #bucle infinito para que la aplicación nunca deje de ejecutarse hasta que salga el usuario presionando X de la ventana
        if M.menu_disp:
            m1 = M.menu_ejecucion()
        else:
            m2 = M.juego_ejecucion()