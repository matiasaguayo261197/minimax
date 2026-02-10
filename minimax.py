import random #para movimientos aleatorios
import os   # poder limpiar la pantalla
import time # Para pausar entre turnos

class Laberinto:   # hacemos la clase "laberinto" y definimos el tamanho
    def __init__(self, ancho=6, alto=6):
        self.ancho = ancho
        self.alto = alto
        self.pos_gato = (0, 0)
        self.pos_raton = (ancho - 1, alto - 1)

    def imprimir_tablero(self):
        print("\n" + "=" * 20)
        for y in range(self.alto):
            fila_piezas = []
            for x in range(self.ancho):
                if (x, y) == self.pos_gato:
                    fila_piezas.append(" 🐱 ")
                elif (x, y) == self.pos_raton:
                    fila_piezas.append(" 🐭 ")
                else:
                    fila_piezas.append(" .  ")
            print("".join(fila_piezas))
        print("=" * 20 + "\n")

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
            return 1000 - profundidad 
        if profundidad == 0:
            return -self.distancia_manhattan(pos_gato, pos_raton)
            
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
        mejor_movimiento = self.pos_gato
        opciones = self.obtener_movimientos_validos(self.pos_gato)
        
        for opcion in opciones:
            puntaje = self.minimax(opcion, self.pos_raton, 4, False)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_movimiento = opcion
        self.pos_gato = mejor_movimiento

    def mover_raton_aleatorio(self):
        opciones = self.obtener_movimientos_validos(self.pos_raton)
        if opciones:
            self.pos_raton = random.choice(opciones)

    def juego_terminado(self):
        if self.pos_gato == self.pos_raton:
            return True
        return False

# --- ZONA DE JUEGO (ANIMADA) ---
if __name__ == "__main__":
    juego = Laberinto()
    
    # Bucle infinito (o hasta que termine el juego)
    turno = 1
    while True:
        # 1. BORRAR PANTALLA
        # Este comando detecta si estas en Windows ('nt') y usa 'cls', 
        # o si estas en Mac/Linux y usa 'clear'.
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"--- TURNO {turno} ---")
        juego.imprimir_tablero()
        
        # 2. Verificamos si ya terminó antes de mover
        if juego.juego_terminado():
            print("\n🏁 ¡JUEGO TERMINADO! El gato atrapó al ratón. 🏁")
            break
            
        # 3. Mueven los personajes
        juego.mover_raton_aleatorio()
        
        # Verificamos otra vez por si el ratón chocó con el gato
        if juego.juego_terminado():
            # Limpiamos una ultima vez para ver el choque
            os.system('cls' if os.name == 'nt' else 'clear')
            juego.imprimir_tablero()
            print("\n🏁 ¡El Ratón chocó con el Gato! GANA EL GATO. 🏁")
            break
            
        juego.mover_gato_inteligente()
        
        # 4. PAUSA (Animación)
        # Esperamos 0.8 segundos para que el ojo humano vea el movimiento
        time.sleep(0.8) 
        
        turno += 1