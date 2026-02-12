import random # importamos random para que la ia haga movimientos al azar si tiene opciones igual de buenas 
import os   # le dice al sistema operativo que limpie la pantalla cada cierto periodo de tiempo 
import time # el lapso de tiempo en que la pantalla es limpiada y re impresa 

class Laberinto:   #creamos la clase que albergara todo el jurgo
    def __init__(self, ancho=10, alto=10): #empezamos definiendo los limites del mapa y la posicion de los personajes 
        self.ancho = ancho
        self.alto = alto
        self.pos_gato = (5, 5)
        self.pos_raton = (ancho - 1, alto - 1)
        self.pos_salida = (0, 0)
            
    def imprimir_tablero(self):   #lo que permite que veamos el juego
        print("\n" + "=" * (self.ancho * 3 + 2)) # imprimimos "===" para darle "techo" y "suelo" igual al ancho x3 +2
        for y in range(self.alto): # se empieza a dibujar el tablero fila por fila de arriba a abajo empezando en y0
            fila_piezas = [] #se almacenan los caracteres en una lista antes de ser impreso 
            for x in range(self.ancho):  #ahora de izquierda a derecha empezando en x0
                if (x, y) == self.pos_gato: 
                    fila_piezas.append(" 🐱")  #si en la x y en la y se encuentra posicionado el gato, se agrega el gato a a la lista
                elif (x, y) == self.pos_raton:
                    fila_piezas.append(" 🐭") #si en la x y en la y se encuentra posicionado el reton, se agrega el raton a la lista 
                elif (x, y) == self.pos_salida:
                    fila_piezas.append(" 🚪") #se agrega la posicion de la salida a la lista
                else:
                    fila_piezas.append(" . ") #si no hay nada se agrega un punto a la lista
            print("".join(fila_piezas))  #se imprime la lista de forma limpia y entendible 
        print("=" * (self.ancho * 3 + 2) + "\n")

    def realizar_movimiento_manual(self, personajes, tecla): #movimientos para el jugador 
        direcciones = {    #hacemos un diccionario y le asignamos claves y valores que puedan ser equivalentes a una coordenada 
            'w': (0, -1), # tecla Arriba : se resta 1 a y
            's': (0, 1),  # tecla Abajo: se resta 1 a y 
            'a': (-1, 0), # tecla Izquierda: se resta 1 a x
            'd': (1, 0)   #tecla Derecha: se suma 1 a x
        }
        if tecla not in direcciones:
            print('Tecla inválida, usa W, A, S, D.')  #si se presiona una tecla fuera del diccionario devuelve este mensaje
            return
        dx, dy = direcciones[tecla] # busca en el diccionario que coordenadas corresponde a cada tecla pulsada
        if personajes == 'gato':  
            x, y = self.pos_gato  #si el personaje es el gato toma las coordenadas actuales del gato 
        elif personajes == "raton": 
            x, y = self.pos_raton #si eres el raton toma las coordenadas actuales del raton
        else:
            return
        nuevo_x, nuevo_y = x + dx, y + dy # lectura y actualizacion de coordenadas
        if 0 <= nuevo_x < self.ancho and 0 <= nuevo_y < self.alto: # evita que te salgas de la delimitacion del mapa 
            if personajes == "gato":
                self.pos_gato = (nuevo_x, nuevo_y) #si la casilla es valida se actualiza la posicion del gato
            elif personajes == "raton":
                self.pos_raton = (nuevo_x, nuevo_y) # si la casilla es valida se actualiza la posicion del raton
        else:
            print("🚧 ¡Muro! No puedes avanzar por ahí.") # si trata de salirse de los margenes imprime este mensaje 

    def obtener_movimientos_validos(self, posicion): 
        x, y = posicion # recibe la posicion en la que estas 
        movimientos_posibles = [] #guarfa los movimientos legales que se encuentren
        direcciones = [
            (0, -1), (0, 1), (-1, 0), (1, 0)       #direcciones permitidas
        ]
        for dx, dy in direcciones: # itera por cada direccion posible asignando valor a las variables temporales dx,dy
            nuevo_x = x + dx #recibe una posicion pero no se mueve solo lo analiza
            nuevo_y = y + dy # la nueva posicion seria: la posicion actual (x) + el cambio (dx)
            if 0 <= nuevo_x < self.ancho and 0 <= nuevo_y < self.alto: #verifica que la casilla analizada este dentro del tablero 
                movimientos_posibles.append((nuevo_x, nuevo_y)) #si la casilla es valida pasa a la lista 
        return movimientos_posibles #despues de analizar los movimientos entrega una lista completa de opciones segutas a quien las pidio

    def distancia_manhattan(self, pos1, pos2): #distancia real que debe recorrer alguien que solo puede moverse en ángulos de 90 grados (Arriba, Abajo, Izquierda, Derecha).
        x1, y1 = pos1 # posicion de un personaje 
        x2, y2 = pos2 # posicion de otro personaje 
        return abs(x1 - x2) + abs(y1 - y2) # calcula a cuantos turnos de distacia se encuentra un personaje de otro  (abs Convierte "diferencia matemática" en "distancia física".)

    def minimax(self, pos_gato, pos_raton, profundidad, es_turno_gato): # es una funcion recursiva 
        if pos_gato == pos_raton:
            return 1000 + profundidad  #el gato atrapa al raton y gana 
        if pos_raton == self.pos_salida:
            return -1000 - profundidad #el raton logra llegar a la salida y escapa

        if profundidad == 0:   #Cuando la IA deja de predecir el futuro (profundidad 0), mide dos cosas: la distancia entre los animales y la distancia a la salida
            dist_gato_raton = self.distancia_manhattan(pos_gato, pos_raton) #¿Qué tan cerca está el depredador de la presa?
            dist_salida = self.distancia_manhattan(pos_raton, self.pos_salida) #¿Qué tan cerca está el Ratón de salvarse?
      
            puntaje = -dist_gato_raton + (dist_salida * 2) #fórmula matemática para convertir esas distancias en puntos.
                                                            #el gato gana puntos si se acerca a su presa, y el Ratón gane puntos (haciendo el número más bajo) si se acerca a la puerta. 
                                                            # El * 2 es simplemente para que el Ratón le dé más prioridad a escapar que a esconderse.
            return puntaje

        if es_turno_gato:
            max_puntuacion = -float('inf')
            movimientos = self.obtener_movimientos_validos(pos_gato)
            for move in movimientos:
                puntuacion = self.minimax(move, pos_raton, profundidad - 1, False)
                max_puntuacion = max(max_puntuacion, puntuacion)
            return max_puntuacion
        else:
            min_puntuacion = float('inf')
            movimientos = self.obtener_movimientos_validos(pos_raton)
            for move in movimientos:
                puntuacion = self.minimax(pos_gato, move, profundidad - 1, True)
                min_puntuacion = min(min_puntuacion, puntuacion)
            return min_puntuacion

    def mover_gato_inteligente(self):
        mejor_puntaje = -float('inf')
        mejores_opciones = []
        opciones = self.obtener_movimientos_validos(self.pos_gato)
        
        for opcion in opciones:
         
            puntaje = self.minimax(opcion, self.pos_raton, 4, False)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejores_opciones = [opcion]
            elif puntaje == mejor_puntaje:
                mejores_opciones.append(opcion)
        if mejores_opciones:        
            self.pos_gato = random.choice(mejores_opciones)

    def mover_raton_inteligente(self):
        mejor_puntaje = float('inf')
        mejores_opciones = []
        opciones = self.obtener_movimientos_validos(self.pos_raton)
        
        
        if self.pos_salida in opciones:
            self.pos_raton = self.pos_salida
            return
        
        for opcion in opciones:
            puntaje = self.minimax(self.pos_gato, opcion, 4, True)
            if puntaje < mejor_puntaje:
                mejor_puntaje = puntaje
                mejores_opciones = [opcion]
            elif puntaje == mejor_puntaje:
                mejores_opciones.append(opcion)
        if mejores_opciones:
            self.pos_raton = random.choice(mejores_opciones)

    def juego_terminado(self):
        if self.pos_gato == self.pos_raton:
            return True
        if self.pos_raton == self.pos_salida:
            return True
        return False


if __name__ == "__main__":
    juego = Laberinto()
    MAX_TURNOS = 30
    turno = 1
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n🧀 --- BIENVENIDO AL LABERINTO --- 🐱")
    print("1. Jugar como el GATO (Cazar al Ratón IA)")
    print("2. Jugar como el RATÓN (Escapar del Gato IA)")
    print("3. Modo Espectador (IA vs IA)")
    
    modo = input("\nElige una opción (1, 2 o 3): ")
    
    while turno <= MAX_TURNOS:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"--- TURNO {turno} de {MAX_TURNOS} ---")
        juego.imprimir_tablero()
        
        if juego.juego_terminado():
            if juego.pos_raton == juego.pos_salida:
                print("\n🚪 ¡EL RATÓN HA ESCAPADO! ¡VICTORIA! 🚪")
            else:
                print("\n🏁 ¡EL GATO ATRAPÓ AL RATÓN! 🏁")
            break

       
        if modo == "2":
            move = input("Tu turno Ratón (WASD + Enter): ").lower()
            juego.realizar_movimiento_manual("raton", move)
        elif modo == "1" or modo == "3": 
            juego.mover_raton_inteligente()

        if juego.juego_terminado():
            if juego.pos_raton == juego.pos_salida:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"--- TURNO {turno} ---")
                juego.imprimir_tablero()
                print("\n🚪 ¡EL RATÓN HA ESCAPADO! ¡VICTORIA! 🚪")
                break
            elif juego.pos_gato == juego.pos_raton:
                 os.system('cls' if os.name == 'nt' else 'clear')
                 juego.imprimir_tablero()
                 print("\n🏁 ¡EL RATÓN CHOCÓ CON EL GATO! 🏁")
                 break

       
        if modo == "1": 
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"--- TURNO {turno} de {MAX_TURNOS} ---")
            juego.imprimir_tablero()
            move = input("Tu turno Gato (WASD + Enter): ").lower()
            juego.realizar_movimiento_manual("gato", move)
            
        elif modo == "2" or modo == "3":
            if modo == "2": 
                print("🤖 El Gato IA está pensando...")
                
            juego.mover_gato_inteligente()

        if juego.juego_terminado():
             os.system('cls' if os.name == 'nt' else 'clear')
             print(f"--- TURNO {turno} ---")
             juego.imprimir_tablero()
             print("\n🏁 ¡EL GATO ATRAPÓ AL RATÓN! 🏁")
             break
        
        if modo == "3":
            time.sleep(0.5)
        
        turno += 1
    
    if turno > MAX_TURNOS:
        print("\n⏳ ¡SE ACABÓ EL TIEMPO! El Ratón sobrevivió.")