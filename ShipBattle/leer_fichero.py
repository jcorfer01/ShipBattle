class Leer_Fichero:
    def __init__(self): #constructor vacio
        pass
        
    def buscar_10_ult_partidas(self):
        fichero_jugadores = open("ficheros/Historial_Partidas.txt","r")
        i = 1 #var contador
        
        lineas = fichero_jugadores.readlines() #guardo las lineas en una lista de str
        lineas_10 = ["","","","","","","","","",""] #establezco la lista de 10 lineas con str vacios de forma predeterminada
        
        while i <= 10 and i <= lineas.__len__(): #recorro 10 lineas del fichero o si tiene menos las que haya
            lineas_10[i-1] = lineas[lineas.__len__()-i] #guarda cada linea en la lista
            i+=1 #pasa a la siguiente linea
        
        fichero_jugadores.close() #cierro el fichero
        return lineas_10 #devuelve todas las lineas
    
    def buscar_hist_jugador(self,jugador):
        fichero_jugadores = open("ficheros/Historial_Jugadores.txt","r")
        i = 0 #var contador
        historial_jugador = ""
        
        lineas = fichero_jugadores.readlines() #guardo las lineas en una lista de str
        for l in lineas: #recorro toda la lista de lineas
            array_linea = l.split(":") #separo la linea en otra lista (jugador:p_ganados:p_perdidos:p_perdidos:\n)
            
            if jugador == array_linea[0]: #si coincide el tag del jugador con el que hay en el fichero
                historial_jugador = l
                fichero_jugadores.close()
                return historial_jugador #devuelve la linea completa [str()]
            
            i+=1 #pasa a la siguiente linea
        
        fichero_jugadores.close()
        historial_jugador = ""
        return historial_jugador #devuelve una var vacía la cual indica que no se ha encontrado
'''
if __name__ == "__main__":
    e = Leer_Fichero()
    print(e.buscar_10_ult_partidas())
    print(e.buscar_hist_jugador("IZQ"))
    print(e.buscar_hist_jugador("XD"))
'''