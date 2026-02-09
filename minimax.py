import random
class Laberinto:
    def __init__(self,ancho=6, alto=6): #dimensiones del tablero 
        self.ancho=ancho
        self.alto= alto
        self.pos_gato= (0,0)   #posicon inicial dle gatp
        self.pos_raton= (ancho - 1 , alto -1)   #posicion inicial del raton
    def imprimir_tablero (self):
        print("\n" + "=" * 20)
        for y in range(self.alto):# Recorremos cada fila (y)
            fila_piezas=[]
            for x in range (self.ancho):
                if (x, y) == self.pos_gato:
                    # 2. Usamos .append() para agregar a la lista (es mas seguro para el editor)
                    fila_piezas.append('g')
                elif (x,y)== self.pos_raton:
                    fila_piezas.append ('R')
                else:
                    fila_piezas.append ('. ')
                    # 3. Al final, usamos "".join() para "pegar" todas las piezas de la lista
            print("".join(fila_piezas))
        print("=" * 20 + "\n")

    def obtener_movimientos_validos(self, posicion):
        x,y = posicion
        movimientos_posibles =[]
        #definimos los 4 movimientos posibles
        #(dx, dy) significa cambio en x o cambio en y
        direcciones=[
            (0,-1), #arriba 
            (0,1), #abajo
            (-1,0), #izquierda
            (1,0)#derecha
        ]
        for dx,dy in direcciones: # Verificamos que no se salga del tablero (Límites)
            nuevo_x= x+ dx
            nuevo_y= y + dy
            if 0 <= nuevo_x < self.ancho and 0 <= nuevo_y < self.alto:
                movimientos_posibles.append((nuevo_x,nuevo_y))
        return movimientos_posibles

    def moviemiento_raton_aleatorio(self):
        opciones= self.obtener_movimientos_validos(self.pos_raton)# 1. Preguntamos: "¿A dónde puedo ir desde mi posición actual?"
        if opciones:# 2. Si hay opciones, elegimos una al azar
            nueva_posicion= random.choice(opciones)
            self.pos_raton= nueva_posicion
    def juego_terminado (self):
        if self.pos_gato== self.pos_raton:
            return True # Devuelve True si el gato atrapó al ratón
        return False
if __name__ == "__main__":
    juego=Laberinto()
    print('el raton ha despertado!')
    for turno in range (5): # Vamos a simular 5 turnos
        print (f'/n---TURNO {turno + 1}---')
        juego.moviemiento_raton_aleatorio()   # 1. Movemos al Ratón (Aleatorio)
        juego.imprimir_tablero()                 # 3. Dibujamos el mapa
        if juego.juego_terminado():
            print('JUEGO TERMINADO!')
            break

