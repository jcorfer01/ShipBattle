import tkinter as tk

#creo una variable de tkinter para obtener la resolucion de la pantalla
root = tk.Tk()
ANCHO_PANTALLA = root.winfo_screenwidth()
ALTO_PANTALLA = root.winfo_screenheight()
#ANCHO_PANTALLA = 1280 #var para probar resolucion 720p
#ALTO_PANTALLA = 720

ANCHO_NAVE, ALTO_NAVE = 40, 40 #tamaño nave

VEL_NAVE = 5 #su vel

ANCHO_BALA, ALTO_BALA = 10, 5 #tamaño bala
