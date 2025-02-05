class Boton():
    def __init__(self, imagen, pos, txt_entr, font, base_color, color_flot): #constuctor
        self.imagen = imagen 
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color_base, self.color_hover = base_color, color_flot #color y color de hover
        self.txt_entr = txt_entr
        self.text = self.font.render(self.txt_entr, True, self.color_base) #font
        if self.imagen is None: 
            self.imagen = self.text #si no tiene img, se le pone el texto como dibujo
        self.rect = self.imagen.get_rect(center=(self.x_pos,self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, pantalla): #actualiza el estado del boton
        if self.imagen is not None:
            pantalla.blit(self.imagen, self.rect)
        pantalla.blit(self.text, self.text_rect)
        
    def verInputs(self, posicion): #metodo para saber si se pulsa el boton
        if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def centrar(self, pantalla): #centra el boton en la pantalla
        ancho, alto = pantalla.get_size()
        self.image_rect = self.imagen.get_rect(center=(ancho // 2, alto // 2))

    def cambiarColor(self, posicion): #cambia el color para el hover
        if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.txt_entr, True, self.color_hover)
        else: 
            self.text = self.font.render(self.txt_entr, True, self.color_base)