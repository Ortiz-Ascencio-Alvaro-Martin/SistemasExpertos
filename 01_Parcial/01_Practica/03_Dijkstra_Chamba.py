"""
Ejemplo de uso de Dijkstra para tomar una decisión cotidiana.

El algoritmo de Dijkstra se emplea aquí para encontrar la "ruta" de menor costo
entre dos puntos de un grafo. Para contextualizarlo como una decisión cotidiana,
consideramos el problema de elegir el camino más rápido para ir de casa al trabajo
pasando por distintas paradas (camino, transporte público, tráfico, etc.).

Características del script:
 - Define un grafo ponderado donde cada nodo representa un lugar y cada arista
   un segmento de desplazamiento con un "tiempo" o "costo".
 - Implementa Dijkstra manualmente para no depender de bibliotecas externas.
 - Permite añadir nodos y aristas, y calcular la ruta óptima entre dos nodos
   introducidos por el usuario.

Uso:
    python 01_Parcial/01_Practica/03_Dijkstra.py

Requisitos:
    - Python 3.6+ (no se usan librerías externas)
"""

import sys
import heapq


def dijkstra(graph, start):
    """Devuelve dos diccionarios: distancias mínimas y predecesores.

    `graph` es un dict donde graph[u] es otro dict {v: weight, ...}.
    """
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > distances[u]:
            continue
        for v, weight in graph[u].items():
            alt = current_dist + weight
            if alt < distances[v]:
                distances[v] = alt
                previous[v] = u
                heapq.heappush(heap, (alt, v))

    return distances, previous


def reconstruir_camino(previous, target):
    """Reconstruye la ruta desde el nodo inicial hasta `target`.

    Retorna la lista de nodos en el camino (incluyendo inicio y destino).
    """
    path = []
    u = target
    while u is not None:
        path.append(u)
        u = previous[u]
    return list(reversed(path))


def crear_grafo_decision_oferta(salario_bueno, ubicacion_buena,
                                   beneficios_buenos, cultura_buena,
                                   remoto, reputacion):
    """Construye un grafo para comparar aceptar o rechazar una oferta de trabajo.

    El grafo contiene dos cadenas paralelas que representan el camino hacia
    "Accept" y "Reject". Cada tramo lleva un peso que penaliza una elección
    poco favorable:
      * cadena A (aceptar): penaliza cuando un aspecto es malo
      * cadena R (rechazar): penaliza cuando un aspecto es bueno

    Los pesos son arbitrarios y solo sirven para ilustrar cómo Dijkstra puede
    combinar múltiples criterios.
    """
    # costes para cada criterio (más alto = peor para la cadena)
    pesos_accept = [0 if salario_bueno else 5,
                    0 if ubicacion_buena else 4,
                    0 if beneficios_buenos else 3,
                    0 if cultura_buena else 2,
                    0 if remoto else 3,
                    0 if reputacion else 2]
    pesos_reject = [0 if not salario_bueno else 5,
                    0 if not ubicacion_buena else 4,
                    0 if not beneficios_buenos else 3,
                    0 if not cultura_buena else 2,
                    0 if not remoto else 3,
                    0 if not reputacion else 2]

    g = {'Start': {}}
    # construir la cadena de aceptación
    prev = 'Start'
    for i, w in enumerate(pesos_accept, start=1):
        nodo = f'A_{i}'
        g.setdefault(prev, {})[nodo] = w
        g[nodo] = {}
        prev = nodo
    g[prev]['Accept'] = 0
    g['Accept'] = {}

    # construir la cadena de rechazo
    prev = 'Start'
    for i, w in enumerate(pesos_reject, start=1):
        nodo = f'R_{i}'
        g.setdefault(prev, {})[nodo] = w
        g[nodo] = {}
        prev = nodo
    g[prev]['Reject'] = 0
    g['Reject'] = {}

    return g


def mostrar_grafo(graph):
    print("Grafo de decisión (peso de cada arista):")
    for u, edges in graph.items():
        for v, w in edges.items():
            print(f"  {u} -> {v}: {w}")


def main():
    print("--- Decisión de aceptar o rechazar una oferta de trabajo ---")

    # pedir criterios al usuario
    def pregunta_bool(texto):
        r = input(texto + " (s/n): ").strip().lower()
        return r.startswith('s')

    def pregunta_importancia(texto):
        while True:
            try:
                val = int(input(texto + " (1=baja .. 5=alta): ").strip())
                if 1 <= val <= 5:
                    return val
            except ValueError:
                pass
            print("Por favor ingresa un número entre 1 y 5.")

    salario_bueno = pregunta_bool("¿La oferta tiene un salario competitivo?")
    ubicacion_buena = pregunta_bool("¿La ubicación es conveniente?")
    beneficios_buenos = pregunta_bool("¿Los beneficios son atractivos?")
    cultura_buena = pregunta_bool("¿La cultura de la empresa te convence?")
    remoto = pregunta_bool("¿Existe opción de trabajo remoto?")
    reputacion = pregunta_bool("¿La empresa tiene buena reputación?")

    # importancia de cada criterio
    imp_salario = pregunta_importancia("Importancia del salario")
    imp_ubicacion = pregunta_importancia("Importancia de la ubicación")
    imp_beneficios = pregunta_importancia("Importancia de los beneficios")
    imp_cultura = pregunta_importancia("Importancia de la cultura")
    imp_remoto = pregunta_importancia("Importancia del trabajo remoto")
    imp_reputacion = pregunta_importancia("Importancia de la reputación")

    graph = crear_grafo_decision_oferta(salario_bueno, ubicacion_buena,
                                        beneficios_buenos, cultura_buena,
                                        remoto, reputacion)
    mostrar_grafo(graph)

    start = 'Start'
    end_accept = 'Accept'
    end_reject = 'Reject'

    distances, previous = dijkstra(graph, start)

    cost_accept = distances.get(end_accept, float('inf'))
    cost_reject = distances.get(end_reject, float('inf'))

    # cálculo detallado por criterio
    breakdown = {
        'salario': (0 if salario_bueno else 5 * imp_salario,
                    5 * imp_salario if salario_bueno else 0),
        'ubicacion': (0 if ubicacion_buena else 4 * imp_ubicacion,
                      4 * imp_ubicacion if ubicacion_buena else 0),
        'beneficios': (0 if beneficios_buenos else 3 * imp_beneficios,
                       3 * imp_beneficios if beneficios_buenos else 0),
        'cultura': (0 if cultura_buena else 2 * imp_cultura,
                    2 * imp_cultura if cultura_buena else 0),
        'remoto': (0 if remoto else 3 * imp_remoto,
                   3 * imp_remoto if remoto else 0),
        'reputacion': (0 if reputacion else 2 * imp_reputacion,
                       2 * imp_reputacion if reputacion else 0),
    }

    path_accept = reconstruir_camino(previous, end_accept)
    path_reject = reconstruir_camino(previous, end_reject)

    print(f"\nCosto camino a aceptar: {cost_accept}  (ruta: {' -> '.join(path_accept)})")
    print(f"Costo camino a rechazar: {cost_reject}  (ruta: {' -> '.join(path_reject)})")

    print("\nDetalle por criterio (accept_cost, reject_cost):")
    for crit, (c_acc, c_rej) in breakdown.items():
        print(f"  {crit.capitalize()}: aceptar={c_acc}, rechazar={c_rej}")

    if cost_accept < cost_reject:
        print("\n→ La decisión sugerida por Dijkstra es: ACEPTAR la oferta.")
    elif cost_reject < cost_accept:
        print("\n→ La decisión sugerida por Dijkstra es: RECHAZAR la oferta.")
    else:
        print("\n→ Ambos caminos tienen el mismo costo; la decisión queda abierta.")


if __name__ == '__main__':
    main()
