"""
Algoritmo de decisión para determinar si se debe hacer despensa.

Este script genera un conjunto de datos sintéticos para entrenamiento de un modelo
(solo con fines ilustrativos) y usa **regresión logística** como clasificador cuando
`scikit-learn` está disponible. Si no lo está, recurre a un sencillo sistema de reglas.

# Algoritmo empleado

- Modelo: regresión logística (scikit-learn)
- Alternativa: reglas basadas en umbrales

* inventario (número de unidades de alimentos disponibles)
* días sin comida
* presupuesto disponible

Se provee también una regla simple fall-back en caso de que scikit-learn no esté
instalado o se prefiera un sistema basado en reglas.

El usuario puede ejecutar el script, introducir valores y recibir una recomendación.

Uso:
    python 01_Algotirmo1.py

Requisitos:
    - Python 3.6+
    - numpy
    - scikit-learn (opcional, el script funciona con reglas simples si no está presente)

"""

import sys

try:
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def generar_datos_sinteticos(n=200):
    """Genera datos sintéticos para entrenamiento.

    Las características son:
    - inventario: entre 0 y 20 unidades
    - dias_sin_comida: entre 0 y 7 días
    - presupuesto: entre 0 y 500 (moneda local)

    La etiqueta se calcula con una regla simple: se considera necesario hacer despensa
    si el inventario es bajo, los días sin comida son altos o el presupuesto es grande.
    Esta etiqueta se usará solo para entrenar un modelo de ejemplo.
    """
    X = np.zeros((n, 3))
    y = np.zeros(n, dtype=int)

    for i in range(n):
        inv = np.random.rand() * 20
        dias = np.random.rand() * 7
        pres = np.random.rand() * 500
        X[i] = [inv, dias, pres]
        # regla de generación de etiquetas
        y[i] = int((inv < 5) or (dias > 2) or (pres > 100))

    return X, y


def entrenar_modelo(X, y):
    """Entrena un modelo de regresión logística con los datos proporcionados."""
    model = LogisticRegression()
    model.fit(X, y)
    return model


def decision_regla(inventario, dias_sin_comida, presupuesto):
    """Sistema basado en reglas a modo de respaldo.

    La decisión se basa en umbrales sencillos:
    - inventario < 5 → comprar
    - dias_sin_comida > 2 → comprar
    - presupuesto > 100 → comprar
    """
    return (inventario < 5) or (dias_sin_comida > 2) or (presupuesto > 100)


def predecir(model, inventario, dias_sin_comida, presupuesto):
    """Predice con el modelo si se debe hacer despensa."""
    x = np.array([[inventario, dias_sin_comida, presupuesto]])
    return bool(model.predict(x)[0])


def main():
    print("--- Sistema de decisión para hacer despensa ---")

    # pedir entradas al usuario
    try:
        inventario = float(input("Inventario actual (unidades): "))
        dias = float(input("Días sin comida: "))
        presupuesto = float(input("Presupuesto disponible: "))
    except ValueError:
        print("Entrada no válida. Use números.")
        sys.exit(1)

    if SKLEARN_AVAILABLE:
        # generar y entrenar modelo de regresión logística
        X, y = generar_datos_sinteticos()
        modelo = entrenar_modelo(X, y)
        decision = predecir(modelo, inventario, dias, presupuesto)
        print("(decisión calculada por modelo de regresión logística)")
    else:
        # usar la alternativa basada en reglas simples
        decision = decision_regla(inventario, dias, presupuesto)
        print("(decisión calculada por el sistema de reglas)")

    if decision:
        print("👉 Deberías hacer despensa.")
    else:
        print("✅ No necesitas hacer despensa por ahora.")


if __name__ == "__main__":
    main()
