import pygame as pg
import sys
from propiedades import ALTO_PANTALLA, ANCHO_PANTALLA
from boton import Boton
from leer_fichero import Leer_Fichero

#creo la variable necesaria para poner los componentes en pantalla y los fondos
pantalla_menu = pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA + 40))

class Menu:
    def __init__(self, fps, vol_musica, vol_sfx): #constructor
        #variables menú principal
        self.menu_disp = True
        self.menuPrincipal_disp = True #var para mostrar el menu principal
        self.menuTag_disp = False #var para mostrar el menu de selección de tags
        self.menuOpciones_disp = False #var para mostrar el menu de opciones
        self.menuHistorial_disp = False #var para mostrar el menu de historial
        self.musica = pg.mixer.music
        self.musica.load("music\Musica_Menu.mp3") #carga el .mp3
        
        #variables menú TAG
        self.tag_j1 = "AAA" #var para recibir los tags escritos
        self.tag_j2 = "BBB"
        self.texto_err_tag = "" #texto para mostrar error en la selección de tag
        self.escribir_tag1 = False #y para permitir escribir el tag1 o el tag2
        self.escribir_tag2 = False
        self.color_rectangulo1 = pg.Color('navy') #var para definir el color del rectángulo de selección de tag y mostrar al usuario si está escribiendo en él
        self.color_rectangulo2 = pg.Color('navy') #var para definir el color del rectángulo del segundo tag
                
        #variables menú opciones
        self.FPS = fps
        self.volumen_musica = vol_musica
        self.volumen_sfx = vol_sfx
            
        #objeto tipo Leer_Fichero para el menu_historial y 
        self.leer_fich = Leer_Fichero()
        self.texto_hist_10_partidas = "" #ver el historial de 10 partidas
        
    def mostrar_menu(self): #BUCLE MUESTRA CADA MENU CUANDO SE LE INDICA menuXXXX_disp = True
        self.musica.play(-1, 0.0) #para iniciar la música en un bucle infinito (loops, start_point)
        while self.menu_disp:
            while self.menuPrincipal_disp:
                if self.tag_j1.__len__() != 0: #vacía los tags anteriores cuando vuelve al menú principal
                    self.tag_j1 = ""
                if self.tag_j2.__len__() != 0:
                    self.tag_j2 = ""
                self.mostrar_Principal()
            while self.menuTag_disp: #menu seleccion tag
                self.mostrar_Tag()
            while self.menuOpciones_disp: #menu opciones
                self.mostrar_Opciones()
            while self.menuHistorial_disp: #menu historial
                self.mostrar_Historial() 
            self.menuPrincipal_disp = True #si sale del último bucle, volverá a mostrar el menu principal
                
    def mostrar_Principal(self): #INTERFAZ MENU PRINCIPAL
        pantalla_menu.blit(pg.transform.scale(pg.image.load("img\Fondo_MenuPrincipal.jpg"),(ANCHO_PANTALLA, ALTO_PANTALLA + 40)), (0, 0)) #variable para el fondo del menú, (0, 0))
        MENU_POS_RATON = pg.mouse.get_pos() #detecta pos del mouse
        
        #dibuja textos sin usar la funcion self.escribir_texto() porque son ligeramente diferentes a los textos 'default'
        nombre_autor = self.get_font(25).render("JORGE CORREYERO FERNANDEZ" ,True, "#b68f40") 
        nombre_juego = self.get_font(150).render("SHIP BATTLE" , True, "#FFFFFF")
        nombre_autor_rect = nombre_autor.get_rect(centerx=ANCHO_PANTALLA-150,centery=ALTO_PANTALLA-20)
        nombre_juego_rect = nombre_juego.get_rect(centerx=ANCHO_PANTALLA//2,centery=100)
        
        pantalla_menu.blit(nombre_autor,nombre_autor_rect)
        pantalla_menu.blit(nombre_juego,nombre_juego_rect)
        
        #dibuja botones
        BTN_PLAY = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 -125),txt_entr="JUGAR",font=self.get_font(50), base_color="White", color_flot="Green")  #iniciar el juego
        BTN_SALIR = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+250),txt_entr="SALIR", font=self.get_font(50),base_color="White", color_flot="Green")  #salir del juego  
        #BTN_PLAY.centrar(pantalla_menu) #no es necesario centrar los botones pq ya aparecen centrados
        BTN_OPCIONES = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2),txt_entr="OPCIONES",font=self.get_font(50), base_color="White", color_flot="Green")  #opciones del juego
        BTN_HIST = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+125),txt_entr="HISTORIAL",font=self.get_font(50), base_color="White", color_flot="Green")  #ver historial
                    
                    
        for boton in [BTN_PLAY, BTN_SALIR, BTN_HIST, BTN_OPCIONES]: #hover para los botones y cambiarlos de color
            boton.cambiarColor(MENU_POS_RATON)
            boton.update(pantalla_menu)

        eventos = pg.event.get() #comprueba si se pulsa X para salir o el boton del raton
        for event in eventos:
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.MOUSEBUTTONDOWN: #detecta si ha clickado algún botón
                if BTN_PLAY.verInputs(MENU_POS_RATON):
                    self.menuPrincipal_disp = False
                    self.menuTag_disp = True
                if BTN_OPCIONES.verInputs(MENU_POS_RATON):
                    self.menuPrincipal_disp = False
                    self.menuOpciones_disp = True
                if BTN_HIST.verInputs(MENU_POS_RATON):
                    self.menuPrincipal_disp = False
                    self.menuHistorial_disp = True
                if BTN_SALIR.verInputs(MENU_POS_RATON):
                    pg.quit()
                    sys.exit()
        
        self.cuadrado_ayuda(MENU_POS_RATON, eventos) #ICONO AYUDA

        pg.display.update()
    
    def mostrar_Tag(self): #INTERFAZ MENU SELECCION TAGS
        pantalla_menu.fill("black")
        pantalla_menu.blit(pg.image.load("img\Fondo_Espacio.jpg"), (0, 0)) #variable para el fondo del menú, posicion inicial img->(0, 0))
        MENU_POS_RATON = pg.mouse.get_pos() #detecta pos del mouse
        
        #dibuja botones
        BTN_PLAY = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+125),txt_entr="JUGAR",font=self.get_font(50), base_color="White", color_flot="Green")  #iniciar el juego
        BTN_VOLVER = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+250),txt_entr="VOLVER", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú
        
        color_activo = pg.Color('white') #rect seleccionado, escribiendo
        color_pasivo = pg.Color('navy') #rect NO seleccionado, no puede escribir
        
        #dibuja texto para pedir los TAG
        self.escribir_texto("TAG JUGADOR 1:",80, ANCHO_PANTALLA // 5, ALTO_PANTALLA // 2 -350)
        self.escribir_texto(self.tag_j1,80, ANCHO_PANTALLA // 5, ALTO_PANTALLA // 2 -250) #cuadrado input tag1
        rect_tag1 = self.dibujar_rect(ANCHO_PANTALLA // 5 -10, ALTO_PANTALLA // 2 -260, 170,80, self.color_rectangulo1, 2)
        
        self.escribir_texto("TAG JUGADOR 2:",80, ANCHO_PANTALLA*3 // 5, ALTO_PANTALLA // 2 -350)
        self.escribir_texto(self.tag_j2,80, ANCHO_PANTALLA*3 // 5, ALTO_PANTALLA // 2 -250) #cuadrado input tag2
        rect_tag2 = self.dibujar_rect(ANCHO_PANTALLA*3 // 5 -10, ALTO_PANTALLA // 2 -260, 170,80, self.color_rectangulo2, 2)
        
        #texto error: APARECE AUTOMATICAMENTE CUANDO SE INTENTA CLICKAR EN JUGAR NO SE HA COMPLETADO ALGUNO DE LOS 2 TAG o SI SE HA SELECCIONADO EL MISMO
        if self.tag_j1 == self.tag_j2:
            self.texto_err_tag = "Escoja TAGs distinos para cada jugador."
        elif self.tag_j1 == "" or self.tag_j2 == "":
            self.texto_err_tag = "Escriba ambos TAGs antes de continuar."
        else:
            self.texto_err_tag = ""
        self.escribir_texto(self.texto_err_tag,40, ANCHO_PANTALLA // 3, ALTO_PANTALLA // 2 -50)
        
        for boton in [BTN_PLAY, BTN_VOLVER]: #hover para los botones y cambiarlos de color
            boton.cambiarColor(MENU_POS_RATON)
            boton.update(pantalla_menu)

        eventos = pg.event.get() 
        for event in eventos:
            if event.type==pg.QUIT: #comprueba si se pulsa X para salir o el boton del raton
                pg.quit()
                sys.exit()
                
            if event.type==pg.KEYDOWN: #detecta si se pulsan teclas
                    if self.escribir_tag1:
                        if event.key == pg.K_BACKSPACE: #si es la tecla de borrar
                            self.tag_j1 = self.tag_j1[0:-1] #borra el ultimo caracter
                        elif self.tag_j1.__len__() < 3 and event.key != pg.K_TAB and event.key != pg.K_SPACE and event.key != pg.K_RETURN: #si no ha superado la longitud máxima y no presiona teclas de caracteres no permitidos (tab, enter, espacio)
                            self.tag_j1 += event.unicode
                            self.tag_j1 = self.tag_j1.upper() #lo que escribe lo para a mayúsculas
                            
                    if self.escribir_tag2: #igual con el segundo tag si tiene seleccionada la caja
                        if event.key == pg.K_BACKSPACE: #si es la tecla de borrar
                            self.tag_j2 = self.tag_j2[0:-1] #elimina la ultima letra
                        elif self.tag_j2.__len__() < 3 and event.key != pg.K_TAB and event.key != pg.K_SPACE and event.key != pg.K_RETURN:
                            self.tag_j2 += event.unicode
                            self.tag_j2 = self.tag_j2.upper()
                        
            if event.type==pg.MOUSEBUTTONDOWN:
                if rect_tag1.collidepoint(event.pos): #detecta si la caja del tag 1 se ha seleccionado
                    self.escribir_tag1 = True #habilita la escritura para el tag1
                    self.escribir_tag2 = False #y la deshabilita la escritura para el tag2
                    self.color_rectangulo1 = color_activo #muestra que está seleccionado el rectangulo para el tag1 poniendolo en blanco
                    self.color_rectangulo2 = color_pasivo #y desactiva el otro poniendolo en azul
                elif rect_tag2.collidepoint(event.pos): #o si se selecciona la de tag 2 lo mismo pero para los elementos del tag2
                    self.escribir_tag2 = True
                    self.escribir_tag1 = False
                    self.color_rectangulo2 = color_activo
                    self.color_rectangulo1 = color_pasivo
                else: #de lo contrario, se ha clickado fuera de ambas, se ponen en pasivo (no escritura) ambas y deshabilita las escrituras
                    self.escribir_tag1 = False
                    self.escribir_tag2 = False
                    self.color_rectangulo1 = color_pasivo
                    self.color_rectangulo2 = color_pasivo
                
                if BTN_PLAY.verInputs(MENU_POS_RATON) and self.tag_j1.__len__() > 0 and self.tag_j2.__len__() > 0 and self.tag_j1 != self.tag_j2: #para poder jugar no puede dejar los tags vacíos ni elegir el mismo para ambos jugadores
                    self.menu_disp = False
                    self.menuPrincipal_disp = False
                    self.menuTag_disp = False
                if BTN_VOLVER.verInputs(MENU_POS_RATON):
                    self.menuPrincipal_disp = True
                    self.menuTag_disp = False
        
        self.cuadrado_ayuda(MENU_POS_RATON, eventos)

        pg.display.update()
     
    def mostrar_Opciones(self): #INTERFAZ MENU OPCIONES (FPS, VOLUMEN MUSICA, VOLUMEN EFECTOS, VIDAS JUGADOR)
        pantalla_menu.blit(pg.image.load("img\Fondo_Espacio.jpg"), (0, 0)) #variable para el fondo del menú, posicion inicial img->(0, 0))
        MENU_POS_RATON = pg.mouse.get_pos() #detecta pos del mouse
                
        color_activo = pg.Color('white') #fps seleccionados
        color_pasivo = pg.Color('black') #fps NO seleccionados (no se ve el rectangulo)
                
        #SELECCION FPS
        match(self.FPS): #mostrar qué fps están seleccionados con un cuadrado blanco
            case 30:
                color_rectangulo30 = color_activo
                color_rectangulo60 = color_pasivo
                color_rectangulo120 = color_pasivo
            case 60:
                color_rectangulo30 = color_pasivo
                color_rectangulo60 = color_activo
                color_rectangulo120 = color_pasivo
            case 120:
                color_rectangulo30 = color_pasivo
                color_rectangulo60 = color_pasivo
                color_rectangulo120 = color_activo
                
        #dibujo los textos para la seleccion de fps
        self.escribir_texto("FPS:",80, ANCHO_PANTALLA // 3, ALTO_PANTALLA // 2 -350)
        self.escribir_texto("30",80, ANCHO_PANTALLA // 3 +150, ALTO_PANTALLA // 2 -350)
        self.escribir_texto("60",80, ANCHO_PANTALLA // 3 +230, ALTO_PANTALLA // 2 -350)
        self.escribir_texto("120", 80, ANCHO_PANTALLA // 3 +320, ALTO_PANTALLA // 2 -350)
        #rectangulos de seleccion fps
        rect_30 = self.dibujar_rect(ANCHO_PANTALLA // 3 +145,ALTO_PANTALLA // 2 -355, 70,70, color_rectangulo30, 2) #pos x, pos y, tam x, tam y, color, borde
        rect_60 = self.dibujar_rect(ANCHO_PANTALLA // 3 +225, ALTO_PANTALLA // 2 -355, 80,70, color_rectangulo60, 2)
        rect_120 = self.dibujar_rect(ANCHO_PANTALLA // 3 +315, ALTO_PANTALLA // 2 -355, 100,70,color_rectangulo120, 2)
        
        
        #SELECCION MUSICA ON/OFF
        if self.volumen_musica > 0: #establece la imagen de los botones ON/OFF según si el sonido está desactivado (es 0) o no
            imagen_ON_musica = pg.image.load("img/Boton_ON_activo.png")
            imagen_OFF_musica = pg.image.load("img/Boton_OFF_pasivo.png")
        else:
            imagen_ON_musica = pg.image.load("img/Boton_ON_pasivo.png")
            imagen_OFF_musica = pg.image.load("img/Boton_OFF_activo.png")
        #uso botones para la seleccion de ON/OFF
        self.escribir_texto("MUSICA:",80, ANCHO_PANTALLA // 3 - 100, ALTO_PANTALLA // 2 -250)
        BTN_ON_MUSICA = Boton(imagen_ON_musica, pos=(ANCHO_PANTALLA // 2 -50, ALTO_PANTALLA // 2 -220),txt_entr="", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú
        BTN_OFF_MUSICA = Boton(imagen_OFF_musica, pos=(ANCHO_PANTALLA // 2 +50, ALTO_PANTALLA // 2 -220),txt_entr="", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú
        
        #SELECCION VOLUMEN MUSICA
        self.escribir_texto("VOLUMEN MUSICA:",80, ANCHO_PANTALLA // 3 -340, ALTO_PANTALLA // 2 -150)
        
        pos_rect = 150
        num_rect_pasivo = int(10 - (10*self.volumen_musica)) #para poder usar el volumen_musica como contador lo paso a entero 1.0 -> 10
        num_rect_activo = int(10*self.volumen_musica)
        rect_vol_musica = []
        
        #cada 10% es un rectangulo para simular una barra de volumen para la musica y los efectos
        while num_rect_activo > 0: #añade a un array los rect activos
            rect_vol_musica.append(self.dibujar_rect(ANCHO_PANTALLA // 3 +pos_rect,  ALTO_PANTALLA // 2 -155, 50, 70, color_activo, 0)) #color = color_activo
            pos_rect += 50 #cada vez que dibuja un rect se mueve 50px a la derecha
            num_rect_activo -=1 #var contador act
        
        while num_rect_pasivo > 0: #añade a un array los rect pasivos
            rect_vol_musica.append(self.dibujar_rect(ANCHO_PANTALLA // 3 +pos_rect,  ALTO_PANTALLA // 2 -155, 50, 70, color_pasivo, 0)) #color = color_pasivo
            pos_rect += 50
            num_rect_pasivo -=1 #var contador pas
        
        #muestro el % de volumen en el que se encuentra la musica
        texto_vol_musica_actual = str(int(self.volumen_musica*100)) + "%" #convertir de 10 a 100
        self.escribir_texto(texto_vol_musica_actual,80, ANCHO_PANTALLA // 3 +700, ALTO_PANTALLA // 2 -150)
                
        
        #SELECCION SFX ON/OFF
        if self.volumen_sfx > 0: #establece la imagen de los botones ON/OFF según si el sonido está desactivado (es 0) o no
            imagen_ON_sfx = pg.image.load("img/Boton_ON_activo.png")
            imagen_OFF_sfx = pg.image.load("img/Boton_OFF_pasivo.png")
        else:
            imagen_ON_sfx = pg.image.load("img/Boton_ON_pasivo.png")
            imagen_OFF_sfx = pg.image.load("img/Boton_OFF_activo.png")
        
        self.escribir_texto("SFX:",80, ANCHO_PANTALLA // 3, ALTO_PANTALLA // 2 -50)   
        BTN_ON_SFX = Boton(imagen_ON_sfx, pos=(ANCHO_PANTALLA // 2 -50, ALTO_PANTALLA // 2 -20),txt_entr="", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú
        BTN_OFF_SFX = Boton(imagen_OFF_sfx, pos=(ANCHO_PANTALLA // 2 +50, ALTO_PANTALLA // 2 -20),txt_entr="", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú

        #SELECCION VOLUMEN SFX (igual que la musica pero -200 px abajo)
        self.escribir_texto("VOLUMEN SFX:",80, ANCHO_PANTALLA // 3 -250, ALTO_PANTALLA // 2 +50)
        
        pos_rect = 150
        num_rect_pasivo = int(10 - (10*self.volumen_sfx))
        num_rect_activo = int(10*self.volumen_sfx)
        rect_vol_sfx = []
        
        while num_rect_activo > 0: #añade a un array los rect activos
            rect_vol_sfx.append(self.dibujar_rect(ANCHO_PANTALLA // 3 +pos_rect,  ALTO_PANTALLA // 2 +45, 50, 70, color_activo, 0)) #color = color_activo
            pos_rect += 50 #cada vez que dibuja un rect se mueve 50px a la derecha
            num_rect_activo -=1 #var contador act
        
        while num_rect_pasivo > 0: #añade a un array los rect pasivos
            rect_vol_sfx.append(self.dibujar_rect(ANCHO_PANTALLA // 3 +pos_rect,  ALTO_PANTALLA // 2 +45, 50, 70, color_pasivo, 0)) #color = color_pasivo
            pos_rect += 50
            num_rect_pasivo -=1 #var contador pas
        
        #muestro el % de volumen en el que se encuentra la sfx
        texto_vol_sfx_actual = str(int(self.volumen_sfx*100)) + "%" #convertir de 10 a 100
        self.escribir_texto(texto_vol_sfx_actual,80, ANCHO_PANTALLA // 3 +700, ALTO_PANTALLA // 2 +50)
        

        #boton salir del menu opciones
        BTN_VOLVER = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+250),txt_entr="VOLVER", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú

        for boton in [BTN_VOLVER]: #hover para el btn
            boton.cambiarColor(MENU_POS_RATON)
            boton.update(pantalla_menu)
        #dibuja los botones de ON/OFF en su estado actual de musica y sfx
        BTN_ON_SFX.update(pantalla_menu)
        BTN_OFF_SFX.update(pantalla_menu)
        BTN_ON_MUSICA.update(pantalla_menu)
        BTN_OFF_MUSICA.update(pantalla_menu)

        eventos = pg.event.get() #comprueba si surgen eventos en teclado o raton
        for event in eventos:
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.MOUSEBUTTONDOWN:
                if rect_30.collidepoint(event.pos): #fps puestos a 30
                    self.FPS = 30
                elif rect_60.collidepoint(event.pos): #fps puestos a 60
                    self.FPS = 60
                elif rect_120.collidepoint(event.pos): #fps puestos a 120
                    self.FPS = 120
                
                contador = 1
                for rect_vol_mus in rect_vol_musica: #comprueba si se han clickado los cuadrados para subir/bajar volumen musica
                    if rect_vol_mus.collidepoint(event.pos):
                        self.volumen_musica = contador/10
                        pg.mixer.music.set_volume(self.volumen_musica) #establece el volumen de toda la musica cuando se cambia en el menu opciones (afecta menu y juego)
                    contador += 1
                
                contador = 1 #reset de contador
                for rect_vol_s in rect_vol_sfx: #comprueba si se han clickado los cuadrados para subir/bajar volumen sfx
                    if rect_vol_s.collidepoint(event.pos):
                        self.volumen_sfx = contador/10
                    contador += 1
                
                if BTN_ON_MUSICA.verInputs(MENU_POS_RATON):
                    if self.volumen_musica == 0: #si estaba apagado el sonido
                        self.volumen_musica = 0.1
                        pg.mixer.music.set_volume(self.volumen_musica) #establece el volumen al minimo
                
                if BTN_OFF_MUSICA.verInputs(MENU_POS_RATON):
                    self.volumen_musica = 0.0
                    pg.mixer.music.set_volume(self.volumen_musica) #establece el volumen a 0
                
                if BTN_ON_SFX.verInputs(MENU_POS_RATON):
                    if self.volumen_sfx == 0: #si el volumen es nulo
                        self.volumen_sfx = 0.1 #establece el volumen al minimo
                
                if BTN_OFF_SFX.verInputs(MENU_POS_RATON):
                    self.volumen_sfx = 0.0 #pone el volumen a 0
                
                if BTN_VOLVER.verInputs(MENU_POS_RATON): #pulsa el boton volver
                    self.menuPrincipal_disp = True #vuelve atras al menu principal
                    self.menuOpciones_disp = False
        
        self.cuadrado_ayuda(MENU_POS_RATON, eventos)
        
        pg.display.update()
    
    def mostrar_Historial(self):
        pantalla_menu.blit(pg.image.load("img\Fondo_Espacio.jpg"), (0, 0)) #variable para el fondo del menú, posicion inicial img->(0, 0))
        MENU_POS_RATON = pg.mouse.get_pos() #detecta pos del mouse
        
        #dibuja botones
        BTN_10_ULT_PART = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+125),txt_entr="VER 10 PARTIDAS",font=self.get_font(50), base_color="White", color_flot="Green")  #ver del historial las ultimas 10 partidas
        BTN_VOLVER = Boton(imagen=pg.image.load("img/Boton.png"), pos=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2+250),txt_entr="VOLVER", font=self.get_font(50),base_color="White", color_flot="Green")  #volver al menú

        color_activo = pg.Color('white') #rect seleccionado, escribiendo
        color_pasivo = pg.Color('navy') #rect NO seleccionado, no puede escribir
        
        #texto y rect de seleccion de tag para ver sus resultados
        self.escribir_texto("TAG:", 80, ANCHO_PANTALLA // 5 -100, ALTO_PANTALLA // 4 -160)
        #reutilizo las variables de la clase relacionadas con el TAG1 -> self.tag_j1, self.color_rectangulo1, self.escribir_tag1, self.texto_err_tag
        self.escribir_texto(self.tag_j1,80, ANCHO_PANTALLA // 5+50, ALTO_PANTALLA // 4 -160)
        rect_tag = self.dibujar_rect(ANCHO_PANTALLA // 5+40,ALTO_PANTALLA // 4 -170,170,80,self.color_rectangulo1,2)
        
        texto_res_tag = self.leer_fich.buscar_hist_jugador(self.tag_j1)
        texto_ganadas = ""
        texto_perdidas = ""
        texto_empatadas = ""
        if self.tag_j1 == "":
            texto_ganadas = ""
            texto_perdidas = ""
            texto_empatadas = ""
            texto_res_tag = "Escriba el TAG del jugador que quiera saber sus resultados."
        elif texto_res_tag == "":
            texto_ganadas = ""
            texto_perdidas = ""
            texto_empatadas = ""
            texto_res_tag = "TAG no encontrado"
        else:
            array_texto_res_tag = texto_res_tag.split(":")
            texto_res_tag = "ESTADÍSTICAS:"
            texto_ganadas = "GANADAS: " + array_texto_res_tag[1]
            texto_perdidas = "PERDIDAS: " + array_texto_res_tag[2]
            texto_empatadas = "EMPATADAS: " + array_texto_res_tag[3]
            
        self.escribir_texto(texto_res_tag, 30, ANCHO_PANTALLA // 5 -100, ALTO_PANTALLA // 4)
        self.escribir_texto(texto_ganadas, 30, ANCHO_PANTALLA // 5 -100, ALTO_PANTALLA // 4+100)
        self.escribir_texto(texto_perdidas, 30, ANCHO_PANTALLA // 5 -100, ALTO_PANTALLA // 4+200)
        self.escribir_texto(texto_empatadas, 30, ANCHO_PANTALLA // 5 -100, ALTO_PANTALLA // 4+300)
        #bucle para mostrar por pantalla cada partida en el historial
        pos_y = -100
        for txt in self.texto_hist_10_partidas:
            self.escribir_texto(txt, 30, ANCHO_PANTALLA*3 // 5 +50, ALTO_PANTALLA // 4+pos_y)
            pos_y += 70
        
        for boton in [BTN_10_ULT_PART, BTN_VOLVER]: #hover para los botones y cambiarlos de color
            boton.cambiarColor(MENU_POS_RATON)
            boton.update(pantalla_menu)

        eventos = pg.event.get() #comprueba eventos en el menu
        for event in eventos:
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type==pg.KEYDOWN: #detecta si se pulsan teclas
                    if self.escribir_tag1: #si tiene seleccionado el cuadro para escribir el tag
                        if event.key == pg.K_BACKSPACE: #si es la tecla de borrar
                            self.tag_j1 = self.tag_j1[0:-1] #borra el ultimo caracter
                        elif self.tag_j1.__len__() < 3  and event.key != pg.K_TAB and event.key != pg.K_SPACE and event.key != pg.K_RETURN: #si no ha superado la longitud máxima
                            self.tag_j1 += event.unicode
                            self.tag_j1 = self.tag_j1.upper() #lo que escribe lo para a mayúsculas
            
            if event.type==pg.MOUSEBUTTONDOWN:
                if rect_tag.collidepoint(event.pos): #detecta si la caja del tag se ha seleccionado
                    self.escribir_tag1 = True #habilita la escritura
                    self.color_rectangulo1 = color_activo #muestra que está seleccionado el rectangulo para el tag1 poniendolo en blanco
                else: #si no se ha clickado en el rect(por ejemplo en un boton o fuera)
                    self.escribir_tag1 = False #deshabilita la escritura
                    self.color_rectangulo1 = color_pasivo #y lo enseña desactivado poniendolo en azul
                if BTN_10_ULT_PART.verInputs(MENU_POS_RATON):
                    self.texto_hist_10_partidas = self.leer_fich.buscar_10_ult_partidas()
                    if self.texto_hist_10_partidas[0] == "": #si la primera linea está vacía, es que no hay historial que enseñar
                        self.texto_hist_10_partidas[0] = "NO SE HA ENCONTRADO NINGÚN HISTORIAL."
                    #de lo contrario, es que hay historial
                        
                if BTN_VOLVER.verInputs(MENU_POS_RATON):
                    self.texto_hist_10_partidas = ""
                    self.menuPrincipal_disp = True
                    self.menuHistorial_disp = False
        
        self.cuadrado_ayuda(MENU_POS_RATON, eventos) #ICONO AYUDA
        
        pg.display.update()
    
    def escribir_texto(self, texto, tam_letra, x, y): #método para escribir texto en pantalla
        texto_pan = self.get_font(tam_letra).render(texto, True, (255,255,255))
        pantalla_menu.blit(texto_pan,(x, y))
    
    def dibujar_rect(self, x, y, x_tam, y_tam, color, borde): #método para dibujar rectángulos sin necesidad de escribir las mismas dos lineas repetidas
        rect = pg.Rect(x, y, x_tam, y_tam)
        pg.draw.rect(pantalla_menu, color, rect, borde)
        return rect #devuelve rect para poder comprobar las colisiones con el cuadrado
    
    def cuadrado_ayuda(self, MENU_POS_RATON, eventos): #ICONO AYUDA CONTROLES -> (?)
        BTN_AYUDA = Boton(pg.image.load("img/Icono_Ayuda.png"), pos=(100, ALTO_PANTALLA-100),txt_entr="", font=self.get_font(50),base_color="White", color_flot="Green") #BTN ICONO AYUDA
        BTN_AYUDA.update(pantalla_menu)
        
        btn_pulsado = False #inicialmente no está pulsado de forma predeterminada
        for event in eventos:
            if event.type==pg.MOUSEBUTTONDOWN:
                if BTN_AYUDA.verInputs(MENU_POS_RATON):
                    btn_pulsado = True
        
        while btn_pulsado: #mientras el boton del raton siga pulsado
            imagen_ayuda = pg.image.load("img/Controles.png") #dibuja la imagen con los controles
            imagen_ayuda = pg.transform.scale(imagen_ayuda, (500, 281))
            pantalla_menu.blit(imagen_ayuda, (ANCHO_PANTALLA//3, ALTO_PANTALLA//3))
            
            eventos = pg.event.get() #comprueba si surgen eventos para salir del bucle
            for event in eventos:
                if event.type==pg.MOUSEBUTTONUP: #cuando suelta el boton del raton
                    if BTN_AYUDA.verInputs(MENU_POS_RATON):
                        btn_pulsado = False #sale del bucle que muestra la imagen
            pg.display.update()
    
    def get_font(self, size): #recibe fuentes
        return pg.font.Font("fuentes/Fuentes.ttf",size)