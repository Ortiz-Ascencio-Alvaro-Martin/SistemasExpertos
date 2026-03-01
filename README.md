# SistemasExpertos
Repositorio con fines educativos 

## Ejemplo de algoritmo de decisión (01_Algotirmo1.py)

El archivo `01_Algotirmo1.py` implementa un sencillo algoritmo de "IA" para
ayudar a decidir si es necesario hacer la despensa. **Algoritmo principal:**
regresión logística (con `scikit-learn`). Si el paquete no está instalado, el
programa recurre a un conjunto de reglas basadas en umbrales como alternativa.

El modelo se entrena con datos sintéticos que combinan inventario, días sin
comida y presupuesto, y luego predice la etiqueta `hacer despensa`.

### Ejecutar

Asegúrate de usar el intérprete del entorno virtual creado para el proyecto:

```bash
# activar el entorno (si no está activo)
source .venv/bin/activate

# o invocar directamente el ejecutable
/workspaces/SistemasExpertos/.venv/bin/python 01_Parcial/01_Practica/01_Algotirmo1.py
```

Los demás ejemplos se ejecutan de forma análoga, cambiando el nombre del
ejecutable.

## Algoritmo con Dijkstra (03_Dijkstra.py)

Ejemplo de aplicación del algoritmo de Dijkstra a una **decisión compleja**:
aceptar o rechazar una nueva oferta de trabajo. El programa:

1. consulta varios criterios al usuario y su importancia (1–5) para cada
   uno. Los criterios son:
      * salario competitivo
      * ubicación conveniente
      * beneficios atractivos
      * cultura de la empresa
      * opción de trabajo remoto
      * reputación de la empresa
   Cada respuesta se traduce en un peso que penaliza la opción contraria.
2. construye un grafo dinámico con dos cadenas paralelas que representan los
   caminos hacia **Accept** o **Reject**, usando los pesos calculados a partir de
   las respuestas y las importancias,
3. aplica Dijkstra para obtener el costo total de cada alternativa y la ruta
   seguida,
4. muestra un desglose detallado por criterio (cuánto contribuye cada factor)
   y sugiere la opción de menor costo.

El algoritmo se implementa manualmente sin bibliotecas externas. La visualización
incluye tanto el grafo (pesos de las aristas) como la explicación completa de la
elección.

```bash
python 01_Parcial/01_Practica/03_Dijkstra.py
```

El resto de los ejemplos se ejecutan de forma similar.
### Dependencias opcionales

- `numpy`
- `scikit-learn`
- `pandas` (opcional, solo para mostrar tablas de datos)

Ambas pueden instalarse con:

```bash
pip install numpy scikit-learn pandas
```

## Algoritmo de toma de agua (02_Algoritmo_toma_agua.py)

Un ejemplo más avanzado que el anterior. **Algoritmo principal:** bosque
aleatorio (`RandomForestClassifier` de scikit-learn) entrenado sobre un dataset
sintético con cinco variables. Si `scikit-learn` (junto a `numpy`/`pandas`) no
están disponibles, el programa usa un sistema de reglas/híbrido para tomar la
decisión.

Ejecutar:

```bash
python 01_Parcial/01_Practica/02_Algoritmo_toma_agua.py
```
