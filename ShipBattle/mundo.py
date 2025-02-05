import pygame as pg
from escribir_fichero import Escribir_Fichero
from nave import Nave
from propiedades import ALTO_PANTALLA, ANCHO_PANTALLA, ANCHO_NAVE
from boton import Boton
from menu import Menu

"""NAVE DERECHA => nave2; NAVE IZQUIERDA => nave1"""
class Mundo:
    def __init__(self, pantalla, tag_j1, tag_j2, volumen_sfx): #constructor recibe pantalla del juego, y los tags escogidos en el menu
        self.ganador = "" #var para definir quien gana
        self.coli_tiempo = pg.time.get_ticks() #var para saber cúando fue la última vez que colisiona algun sprite
        self.pantalla = pantalla
        self.nave1 = pg.sprite.GroupSingle() #se crea un grupo de sprite único para cada nave
        self.nave2 = pg.sprite.GroupSingle()
        self.fin_partida = False
        self.volver_menu = False
        self.tag_j1 = tag_j1 #tag j1
        self.tag_j2 = tag_j2 #tag j2
        
        self.musica_fondo = pg.mixer.music #variable para general la musica
        self.musica_fondo.load("music/Musica_Pelea.mp3") #carga .mp3
        self.musica_fondo.play(-1)
        self.parar_musica = True
        
        #var para efectos de sonido
        self.volumen_sfx = volumen_sfx
        self.sonido_impact = pg.mixer.Sound("music/Sonido_Impacto.mp3") #carga .mp3 para el sonido de impacto
        self.sonido_impact.set_volume(self.volumen_sfx) #establece el volumen elegido en opciones
        
        #img vidas
        self.imagen_v1 = pg.image.load('img/Corazon.png').convert() #carga la imagen
        self.imagen_v1 = pg.transform.scale(self.imagen_v1, (50, 50)) #la escala
        self.pantalla.blit(self.imagen_v1, (ANCHO_PANTALLA-120, ALTO_PANTALLA-80))
        self.mask = pg.mask.from_surface(self.imagen_v1)
        
        self.imagen_v2 = pg.image.load('img/Corazon.png').convert() #carga la imagen
        self.imagen_v2 = pg.transform.scale(self.imagen_v2, (50, 50)) #la escala
        self.pantalla.blit(self.imagen_v2, (0, ALTO_PANTALLA-80))
        
        self.pausa = False #var para pausar el juego
        
        self.generando_mundo() #se genera el mundo al final del constructor
        
    def generando_mundo(self): #crea el mundo
        pos_x1 = 0
        pos_y1 = ALTO_PANTALLA // 2
        pos_nave1 = (pos_x1, pos_y1) #pone la nave1 en el medio izquierda
        self.nave1.add(Nave(pos_nave1, "nave1", self.volumen_sfx)) #lo añade al grupo de sprite único
        pos_x2 = ANCHO_PANTALLA - ANCHO_NAVE
        pos_y2 = ALTO_PANTALLA // 2
        pos_nave2 = (pos_x2, pos_y2) #pone la nave2 en el medio derecha
        self.nave2.add(Nave(pos_nave2, "nave2", self.volumen_sfx)) #y lo añade a su grupo de sprite único
    
    def update(self):
        if not self.fin_partida and not self.pausa:
            self.partida()
                    
        while not self.fin_partida and self.pausa: #tanto el menu de 'pausa' como el menu de 'game over' los meto en un bucle para evitar retardo en la búsqueda de eventos de pulsar botones
            if self.parar_musica: #para la música una vez al entrar en "pausa"
                self.musica_fondo.pause() #se para la musica de pelea
                self.parar_musica = False
            self.menu_pausa()
            
        while self.fin_partida:
            if self.parar_musica: #para la música y guarda los resultados una única vez al entrar en "gameover"
                self.musica_fondo.pause() #se para la musica de pelea
                self.parar_musica = False
                escribir_resultado = Escribir_Fichero(self.tag_j1,self.tag_j2,self.ganador)
                escribir_resultado.escribir_historial_jugador(self.tag_j1) #escribe/actualiza las partidas ganadas:perdidas:empatadas de ambos jugadores
                escribir_resultado.escribir_historial_jugador(self.tag_j2)
                escribir_resultado.escribir_historial_partida() #y guarda el resultado de la partida

            self.game_over()    
        
    def nave_mov(self):
        if not self.fin_partida: #mientras que no acabe la partida
            teclas = pg.key.get_pressed() #detecta las teclas pulsadas y se mueve acorde
            
            #movimientos nave1 -> W A S D
            if teclas[pg.K_a]:
                if self.nave1.sprite.rect.left > 0:
                    self.nave1.sprite.izq()
            if teclas[pg.K_d]:
                if self.nave1.sprite.rect.right < ANCHO_PANTALLA:
                    self.nave1.sprite.der()
            if teclas[pg.K_w]:
                if self.nave1.sprite.rect.top > 0:
                    self.nave1.sprite.arr()
            if teclas[pg.K_s]:
                if self.nave1.sprite.rect.bottom < ALTO_PANTALLA-127:
                    self.nave1.sprite.abj()
                    
            #movimientos nave1 -> ↑ ← ↓ →
            if teclas[pg.K_LEFT]:
                if self.nave2.sprite.rect.right > 50:
                    self.nave2.sprite.izq()
            if teclas[pg.K_RIGHT]:
                if self.nave2.sprite.rect.right < ANCHO_PANTALLA:
                    self.nave2.sprite.der()
            if teclas[pg.K_UP]:
                if self.nave2.sprite.rect.top > 0:
                    self.nave2.sprite.arr()
            if teclas[pg.K_DOWN]:
                if self.nave2.sprite.rect.bottom < ALTO_PANTALLA-127:
                    self.nave2.sprite.abj()
    
    def nave_disp(self):
        if not self.fin_partida: #mientras que no acabe la partida
            teclas = pg.key.get_pressed() #detecta las teclas que se pulsan
            ticks = pg.time.get_ticks()
            segs = int(ticks/20) #cantidad de balas por disparo
            
            if segs % 12 == 0: #intervalo entre disparos
                if teclas[pg.K_LCTRL]:
                    self.nave1.sprite.disparar()
                if teclas[pg.K_RCTRL]: #CAMBIAR TECLA DE DISPARO A K_RCTRL PARA WINDOWS, K_RSHIFT PARA LINUX
                    self.nave2.sprite.disparar()

    def partida(self):
        #dibujo las imagenes de corazón
        self.pantalla.blit(self.imagen_v1, (ANCHO_PANTALLA-120, ALTO_PANTALLA-80))
        self.pantalla.blit(self.imagen_v2, (0, ALTO_PANTALLA-80))
            
        #y el num de vidas que queda a cada jugador
        numv1 = "X " + str(self.nave1.sprite.vida)
        numv2 = "X " + str(self.nave2.sprite.vida)
        vidas_p1 = pg.font.Font("fuentes/Fuentes.ttf", 40).render(numv1, True, "#FFFFFF")
        vidas_p1_rect = vidas_p1.get_rect(centerx=ANCHO_PANTALLA-40,centery=ALTO_PANTALLA-50)
        self.pantalla.blit(vidas_p1, vidas_p1_rect)
        vidas_p2 = pg.font.Font("fuentes/Fuentes.ttf", 40).render(numv2, True, "#FFFFFF")
        vidas_p2_rect = vidas_p2.get_rect(centerx=80,centery=ALTO_PANTALLA-50)
        self.pantalla.blit(vidas_p2, vidas_p2_rect)
        
        #dibujo el contador de inmunidad
        if not self.no_inmunidad(): #si son inmunes dibuja el contador
            t_inmune = int(((pg.time.get_ticks() - self.coli_tiempo)/1000) -4) * (-1)
            contador_inmunidad = pg.font.Font("fuentes/Fuentes.ttf", 40).render(str(t_inmune), True, "#FFFFFF")
            contador_inmunidad_rect = contador_inmunidad.get_rect(centerx=ANCHO_PANTALLA//2,centery=ALTO_PANTALLA//2)
            self.pantalla.blit(contador_inmunidad, contador_inmunidad_rect)
                                    
        self.nave1.update() #actualiza el estado del sprite (posición, movimiento...)
        self.nave1.draw(self.pantalla) #lo pinta en la pantalla
        self.nave2.update()
        self.nave2.draw(self.pantalla)
            
        self.nave1.sprite.grupo_balas.update() #lo mismo con el grupo de sprites de balas de cada bando
        self.nave1.sprite.grupo_balas.draw(self.pantalla)
            
        self.nave2.sprite.grupo_balas.update()
        self.nave2.sprite.grupo_balas.draw(self.pantalla)
            
        pg.display.flip()
        self.detectar_colision() #cada vez que actualiza la pantalla detecta colisiones
            
        teclas = pg.key.get_pressed()
        if teclas[pg.K_ESCAPE]: #si detecta que se ha pulsado escape
            self.pausa = True #pausa el juego

    def game_over(self):
        POS_RATON = pg.mouse.get_pos()
        self.pantalla.fill("black")
        
        GAME_OVER = pg.font.Font("fuentes/Fuentes.ttf", 70).render("GAME OVER" , True, "#8B0000")
            
        if self.ganador != "EMPATE!":
            texto_victoria = self.ganador + " WINS!"
        else:
            texto_victoria = self.ganador
        player = pg.font.Font("fuentes/Fuentes.ttf", 40).render(texto_victoria, True, "#FFFFFF")
        player_rect = player.get_rect(centerx=ANCHO_PANTALLA // 2,centery=100)
            
        GAME_OVER_RECT = GAME_OVER.get_rect(center=(ANCHO_PANTALLA // 2, 200))
            
        self.pantalla.blit(GAME_OVER,GAME_OVER_RECT)
        self.pantalla.blit(player,player_rect)
            
        BTN_REPLAY = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2),txt_entr="REINICIAR",font=self.get_font(50), base_color="White", color_flot="Green")  #reiniciar el juego
        BTN_VOLVER = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+250),txt_entr="VOLVER MENU", font=self.get_font(50),base_color="White", color_flot="Green")  #salir al menu principal  
        
        for boton in [BTN_REPLAY, BTN_VOLVER]:  
            boton.cambiarColor(POS_RATON)
            boton.update(self.pantalla)
            
        eventos = pg.event.get()
        for event in eventos:
            if event.type == pg.MOUSEBUTTONDOWN:
                if BTN_REPLAY.verInputs(POS_RATON):
                    self.coli_tiempo = pg.time.get_ticks()
                    self.generando_mundo()
                    self.musica_fondo.set_pos(0.0) #si se reinicia la partida, se vuelve a poner la musica desde el segundo 0.0
                    self.musica_fondo.unpause()
                    self.fin_partida = False
                    self.volver_menu = False
                    self.parar_musica = True
                if BTN_VOLVER.verInputs(POS_RATON):
                    if self.musica_fondo.get_busy():
                        self.musica_fondo.stop() #si se elige salir al menú, la música se para por completo
                    self.fin_partida = False #sale del menu de game over
                    self.volver_menu = True
        pg.display.update()

    def menu_pausa(self):
        POS_RATON = pg.mouse.get_pos()
        self.pantalla.fill("black")
        
        TXT_PAUSA = pg.font.Font("fuentes/Fuentes.ttf", 70).render("JUEGO EN PAUSA" , True, "#8B0000")
        self.pantalla.blit(TXT_PAUSA,TXT_PAUSA.get_rect(center=(ANCHO_PANTALLA // 2, 100)))
        
        BTN_RESUME = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 -150),txt_entr="CONTINUAR",font=self.get_font(50), base_color="White", color_flot="Green")  #continuar el juego
        BTN_REPLAY = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2),txt_entr="REINICIAR",font=self.get_font(50), base_color="White", color_flot="Green")  #reiniciar el juego
        BTN_VOLVER = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+150),txt_entr="VOLVER MENU", font=self.get_font(50),base_color="White", color_flot="Green")  #salir al menu principal  
        
        for boton in [BTN_RESUME, BTN_REPLAY, BTN_VOLVER]:  
            boton.cambiarColor(POS_RATON)
            boton.update(self.pantalla)
            
        eventos = pg.event.get()
        for event in eventos:
            if event.type == pg.MOUSEBUTTONDOWN:
                if BTN_RESUME.verInputs(POS_RATON):
                    self.musica_fondo.unpause()
                    self.parar_musica = True
                    self.pausa = False
                if BTN_REPLAY.verInputs(POS_RATON): #si se reinicia la partida
                    self.coli_tiempo = pg.time.get_ticks()
                    self.generando_mundo() #se vuelve a general el mundo
                    self.musica_fondo.set_pos(0.0)
                    self.musica_fondo.unpause()
                    self.parar_musica = True
                    self.pausa = False
                if BTN_VOLVER.verInputs(POS_RATON):
                    self.musica_fondo.stop() #si se elige salir al menú, la música se para por completo
                    self.pausa = False #sale del menu de pausa
                    self.volver_menu = True
        
        Menu.cuadrado_ayuda(self, POS_RATON, eventos)
        
        pg.display.update()

    def get_font(self, size): #para obtener el tipo de fuente
        return pg.font.Font("fuentes/Fuentes.ttf",size)
    
    def detectar_colision(self):
        nave1_coli_nave2 = pg.sprite.groupcollide(self.nave2, self.nave1.sprite.grupo_balas, False, False) #detecta colisiones entre las balas de la nave1 y la propia nave2
        nave2_coli_nave1 = pg.sprite.groupcollide(self.nave1, self.nave2.sprite.grupo_balas, False, False) #y viceversa
        coli_naves = pg.sprite.groupcollide(self.nave1, self.nave2, False, False) #detecta si ambas naves se chocan
        
        if self.no_inmunidad(): #si no hay inmunidad
            if coli_naves:
                self.nave1.sprite.restar_vida()
                self.nave2.sprite.restar_vida()
                self.sonido_impact.play() #reproduce el efecto de sonido de impacto
                self.coli_tiempo = pg.time.get_ticks() #establece el tiempo de la ultima colision al actual
                if self.nave2.sprite.vida < 1 and self.nave1.sprite.vida < 1: #si no quedan vidas a alguno de los dos, se acaba la partida
                    self.fin_partida = True
                    self.ganador = "EMPATE!"
                elif self.nave1.sprite.vida < 1:
                    self.fin_partida = True
                    self.ganador = self.tag_j1
                elif self.nave2.sprite.vida < 1:
                    self.fin_partida = True
                    self.ganador = self.tag_j2
            #colision nave - bala
            elif nave1_coli_nave2: #si se detecta colisión1
                self.sonido_impact.play() #reproduce el efecto de sonido de impacto
                self.coli_tiempo = pg.time.get_ticks() #establece el tiempo de la ultima colision al actual
                self.nave1.sprite.restar_vida() #le quita 1 vida
                if self.nave1.sprite.vida < 1: #si no quedan vidas, se acaba la partida
                    self.fin_partida = True
                    self.ganador = self.tag_j1
            elif nave2_coli_nave1: #idem pero balas nave2 con la propia nave2
                self.sonido_impact.play() #reproduce el efecto de sonido de impacto
                self.coli_tiempo = pg.time.get_ticks()
                self.nave2.sprite.restar_vida()
                if self.nave2.sprite.vida < 1:
                    self.fin_partida = True
                    self.ganador = self.tag_j2

    def no_inmunidad(self):
        if pg.time.get_ticks() - self.coli_tiempo > 3000:
            self.nave1.sprite.inmunidad = False
            self.nave2.sprite.inmunidad = False
            return True
        else: #si el tiempo actual - tiempo ultima colision < 3000ms es inmune
            self.nave1.sprite.inmunidad = True
            self.nave2.sprite.inmunidad = True
            return False
        
    def mostrarmenu(self):
        if self.volver_menu:
            return True
        else:
            return False