# 🧀🐱 Laberinto del Gato y el Ratón - Minimax Lab

Bienvenido a mi solución para el simulador de persecución estratégica. Este proyecto es una batalla matemática y lógica de supervivencia en consola, donde un ratón con movimientos aleatorios intenta escapar de un gato impulsado por inteligencia artificial.

## 🎯 ¿Qué creé?
Desarrollé un simulador de tablero bidimensional (8x8) desde cero usando solo Python estándar. El juego enfrenta a dos entidades:
* **El Ratón (R):** Se mueve de forma evasiva pero aleatoria, buscando cualquier casilla válida a su alrededor.
* **El Gato (G):** Utiliza el **Algoritmo Minimax** para predecir los movimientos del ratón hasta con 3 turnos de profundidad en el futuro. Evalúa sus opciones usando la distancia Manhattan para acorralar a su presa.
* **El Tablero:** Un motor visual en consola que se limpia y actualiza dinámicamente (`os.system`) para crear un efecto de animación real, evaluando límites físicos (paredes) en cada turno.

## 💥 ¿Qué funcionó y qué fue un desastre?

### Lo que funcionó muy bien:
* **La modularidad:** Separar la lógica en funciones pequeñas (el "arquitecto" que crea el mapa, el "guardia" que valida los límites, y el "radar" que busca direcciones) hizo que el código final fuera muy fácil de leer y escalar.
* **La Distancia Manhattan:** Funcionó perfectamente como heurística para que el algoritmo Minimax pudiera "puntuar" qué tan buena o mala era una decisión imaginaria.

### El desastre (Retos técnicos):
* **La Matrix y los Tipos de Datos:** Al principio, intentar construir la matriz resultó en clonar la misma fila varias veces (el efecto espejo) o lidiar con errores como `TypeError` por intentar modificar una cadena de texto (`str`) en lugar de una lista (`list`). 
* **La confusión de las Coordenadas:** Navegar por una lista de listas requirió reacostumbrar el cerebro a que primero se accede a la Fila (Y) y luego a la Columna (X), lo contrario al plano cartesiano clásico. Hubo varios `IndexError` cayendo por el precipicio del tablero antes de lograr afinar la función de límites.

## 💡 Mi mejor "¡Ajá!" (Aha moment)
El momento en que la lógica hizo clic fue darme cuenta de que **los personajes no están realmente "dentro" del tablero**. El tablero es solo un plano estático, y el Gato y el Ratón son solo dos variables de coordenadas `[y, x]`. El verdadero truco de magia ocurre al usar esas variables como "llaves" para sobreescribir temporalmente la matriz y dibujarlos en cada turno. 

Además, entender cómo Minimax crea "universos paralelos" copiando coordenadas temporales sin mover a las piezas reales en el tablero principal fue alucinante.

## 🚀 Cómo ejecutar el proyecto
1. Asegúrate de tener Python 3.x instalado.
2. Clona este repositorio 
3. Ejecuta el archivo desde tu terminal:
   ```bash
   python minimax_lab.py