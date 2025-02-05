from datetime import datetime

class Escribir_Fichero:
    def __init__(self, tag_j1, tag_j2, ganador): #constructor el ganador, y los tags escogidos en el menu
        self.tag_j1 = tag_j1
        self.tag_j2 = tag_j2
        self.ganador = ganador
        self.meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        
    def escribir_historial_partida(self):
        fecha_hora = self.get_fecha_hora_actual() #recibo la lista con la fecha y hora
        fichero_partidas = open("ficheros/Historial_Partidas.txt","a")
        texto_resultado = ""
        #escribo el texto que voy a guardar en el fichero de historial con el resultado de la partida y su fecha y hora correspondientes
        if self.ganador == "EMPATE!":
            texto_resultado = self.tag_j1 + " & " + self.tag_j2 + " EMPATAN EL " + fecha_hora[0] + " a las " + fecha_hora[1] +"\n"
        elif self.ganador == self.tag_j1:
            texto_resultado = self.ganador + " GANA A " + self.tag_j2 + " EL " + fecha_hora[0] + " a las " + fecha_hora[1] +"\n"
        elif self.ganador == self.tag_j2:
            texto_resultado = self.ganador + " GANA A " + self.tag_j1 + " EL " + fecha_hora[0] + " a las " + fecha_hora[1] +"\n"   
        else:
            texto_resultado = "Hubo un ERROR al escribir el resultado de la partida.\n"

        fichero_partidas.write(texto_resultado)
        
        fichero_partidas.close()
        
    def escribir_historial_jugador(self, jugador):
        fichero_jugadores = open("ficheros/Historial_Jugadores.txt","a")
        #var para historial de partidas del jugador
        p_ganadas = 0
        p_empatadas = 0
        p_perdidas = 0

        encontado_lineas = self.buscar_jugador(jugador) #busca el tag del jugador en el fichero Historial_Jugadores.txt
        linea_encontrado = encontado_lineas[0] #en que linea se encuentra el jugador buscado
        lista_lineas = encontado_lineas[1]
        
        open('ficheros/Historial_Jugadores.txt', 'w').close() #vacia el contenido del fichero
        
        if linea_encontrado == -1: #si no ha sido encontrado la linea_encontrado == -1
            if self.ganador == "EMPATE!":
                p_empatadas += 1
            elif self.ganador == jugador:
                p_ganadas += 1
            else:
                p_perdidas += 1 #tras establecer si es o no el que gana la partida
            #(jugador:p_ganados:p_perdidos:p_perdidos:\n) --> formato
            linea = str(jugador) + ":" + str(p_ganadas) + ":" + str(p_perdidas) + ":" + str(p_empatadas) + ":\n" #crea la linea con el formato correcto
            lista_lineas.append(linea) #y lo añade al final de la lista de lineas
        else:
            linea_jugador = lista_lineas[linea_encontrado].split(":") #vuelvo a dividir la linea que quiero en una lista de str
            p_empatadas =  int(linea_jugador[3]) #partidas empatadas
            p_ganadas = int(linea_jugador[1]) #partidas ganadas
            p_perdidas = int(linea_jugador[2]) #partidas perdidas
            if self.ganador == "EMPATE!":
                p_empatadas =  p_empatadas + 1
            elif self.ganador == jugador:
                p_ganadas = p_ganadas + 1
            else:
                p_perdidas = p_perdidas + 1 #tras modificar las partidas ganadas/perdidas/empatadas
            
            linea = str(jugador) + ":" + str(p_ganadas) + ":" + str(p_perdidas) + ":" + str(p_empatadas) + ":\n" #crea la linea con el formato correcto
            lista_lineas[linea_encontrado] = linea #sustituye el historial anterior por el nuevo

        for l in lista_lineas:
            fichero_jugadores.write(l) #escribe todos los historiales en el fichero
        
        fichero_jugadores.close() #y lo cierra al final   
    
    def buscar_jugador(self,jugador):
        fichero_jugadores = open("ficheros/Historial_Jugadores.txt","r")
        i = 0 #var contador
        
        lineas = fichero_jugadores.readlines() #guardo las lineas en una lista de str
        for l in lineas: #recorro toda la lista de lineas
            array_linea = l.split(":") #separo la linea en otra lista (jugador:p_ganados:p_perdidos:p_perdidos:\n)
            
            if jugador == array_linea[0]: #si coincide el tag del jugador con el que hay en el fichero
                lista = [i, lineas] #guarda en una lista la linea en la que se encuenta (0 = linea 1, 1 = linea 2, 2 = linea 3...)
                fichero_jugadores.close()
                return lista #si lo encuentra envía la linea en la que se ha encontrado junto al resto de lineas
            
            i+=1 #pasa a la siguiente linea
        
        fichero_jugadores.close()    
        lista = [-1, lineas] #si no encuentra al jugador 
        return lista #devuelve todas las lineas y el número que indica que no se ha encontrado
            
    def get_fecha_hora_actual(self):
        fecha_hora = datetime.now().strftime('%d %m %Y, %H:%M:%S')
        
        hora = fecha_hora[12:fecha_hora.__len__()] #cojo la hora dada por la var fecha_hora (Hora:Min:Seg)
        
        fecha = list(fecha_hora[:10]) #recibe la fecha de la var fecha_hora
        
        mes = int(fecha[3] + fecha[4]) #cojo los dos digitos del mes de la variable fecha_hora
        fecha[3] = "de "
        fecha[4] = self.meses[mes-1] + " de" #lo actualizo al nombre en español de la lista del constructor y le añado "de" delante y detrás de mes
        fecha = "".join(fecha) #guardo la fecha formateada
        
        fecha_hora_formateada = ["",""] #creo una lista vacia con los dos elementos [fecha, hora]
        fecha_hora_formateada[0] = fecha
        fecha_hora_formateada[1] = hora
        return fecha_hora_formateada #los guardo en la lista y la devuelvo