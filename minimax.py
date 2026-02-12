import random 
import os   
import time 

class Laberinto:   
    def __init__(self, ancho=10, alto=10):
        self.ancho = ancho
        self.alto = alto
        self.pos_gato = (5, 5)
        self.pos_raton = (ancho - 1, alto - 1)
        self.pos_salida = (0, 0)
      
        self.evaluacion_posicional = [] 
            
    def imprimir_tablero(self):
        print("\n" + "=" * (self.ancho * 3 + 2))
        for y in range(self.alto):
            fila_piezas = []
            for x in range(self.ancho):
                if (x, y) == self.pos_gato:
                    fila_piezas.append(" 🐱")
                elif (x, y) == self.pos_raton:
                    fila_piezas.append(" 🐭")
                elif (x, y) == self.pos_salida:
                    fila_piezas.append(" 🚪")
                else:
                    fila_piezas.append(" . ")
            print("".join(fila_piezas))
        print("=" * (self.ancho * 3 + 2) + "\n")

    def realizar_movimiento_manual(self, personajes, tecla):
        direcciones = {
            'w': (0, -1), # Arriba
            's': (0, 1),  # Abajo
            'a': (-1, 0), # Izquierda
            'd': (1, 0)   # Derecha
        }
        
        if tecla not in direcciones:
            print('Tecla inválida, usa W, A, S, D.')
            return
            
        dx, dy = direcciones[tecla]
        
        # 1. OBTENER POSICIÓN ACTUAL
        if personajes == 'gato':
            x, y = self.pos_gato
        elif personajes == "raton":
            x, y = self.pos_raton
        else:
            return

        nuevo_x, nuevo_y = x + dx, y + dy 
        
        # 2. VERIFICAR SI CHOCA CON PAREDES Y ACTUALIZAR
        if 0 <= nuevo_x < self.ancho and 0 <= nuevo_y < self.alto:
            if personajes == "gato":
                self.pos_gato = (nuevo_x, nuevo_y)
            elif personajes == "raton":
                self.pos_raton = (nuevo_x, nuevo_y)
        else:
            print("🚧 ¡Muro! No puedes avanzar por ahí.")

    def obtener_movimientos_validos(self, posicion):
        x, y = posicion
        movimientos_posibles = []
        direcciones = [
            (0, -1), (0, 1), (-1, 0), (1, 0)
        ]
        for dx, dy in direcciones:
            nuevo_x = x + dx
            nuevo_y = y + dy
            if 0 <= nuevo_x < self.ancho and 0 <= nuevo_y < self.alto:
                movimientos_posibles.append((nuevo_x, nuevo_y))
        return movimientos_posibles

    def distancia_manhattan(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def minimax(self, pos_gato, pos_raton, profundidad, es_turno_gato):
        if pos_gato == pos_raton:
            return 1000 + profundidad 
        if pos_raton == self.pos_salida:
            return -1000 - profundidad # Negativo porque es bueno para raton (minimizador)

        if profundidad == 0:
            dist_gato_raton = self.distancia_manhattan(pos_gato, pos_raton)
            dist_salida = self.distancia_manhattan(pos_raton, self.pos_salida)
            
            # El gato quiere minimizar distancia al raton y maximizar distancia a salida
            # El raton quiere maximizar distancia al gato y minimizar distancia a salida
            # Formula: (Cerca Ratón) + (Ratón Lejos Salida)
            puntaje = -dist_gato_raton + (dist_salida * 2)
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
            # --- CORRECCIÓN CRÍTICA AQUÍ: Cambiamos 42 por 4 ---
            puntaje = self.minimax(opcion, self.pos_raton, 2, False)
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
        
        # Instinto de supervivencia: Si ve la salida, la toma
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

# --- ZONA DE JUEGO ---
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

        # --- TURNO DEL RATÓN ---
        if modo == "2": # Tu eres el Ratón
            move = input("Tu turno Ratón (WASD + Enter): ").lower()
            juego.realizar_movimiento_manual("raton", move)
        elif modo == "1" or modo == "3": # La IA es el Ratón
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

        # --- TURNO DEL GATO ---
        if modo == "1": # Tu eres el Gato
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"--- TURNO {turno} de {MAX_TURNOS} ---")
            juego.imprimir_tablero()
            move = input("Tu turno Gato (WASD + Enter): ").lower()
            juego.realizar_movimiento_manual("gato", move)
            
        elif modo == "2" or modo == "3": # La IA es el Gato
            if modo == "2": 
                print("🤖 El Gato IA está pensando...")
                # time.sleep(0.5) # Descomenta si quieres darle dramatismo
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