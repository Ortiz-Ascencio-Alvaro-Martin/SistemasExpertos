"""
Algoritmo avanzado de decisión sobre tomar agua.

Este módulo genera un conjunto sintético de datos con múltiples variables y
entrena un modelo de clasificación **RandomForestClassifier** (bosque aleatorio)
para predecir si una persona debería beber agua. El sistema también incluye una
versión basada en "lógica difusa"/reglas para servir como comparación o respaldo.

# Algoritmo empleado

- Modelo: bosque aleatorio (`RandomForestClassifier` de scikit-learn)
- Alternativa: reglas basadas en umbrales y lógica difusa

Características consideradas:
  * temperatura ambiente (°C)
  * nivel de sed (0-10)
  * horas desde la última bebida
  * nivel de actividad física (0-10)
  * humedad (% relativa)

La etiqueta se genera combinando umbrales y términos no lineales de forma que el
problema sea algo más interesante que en el ejemplo anterior. El modelo puede
entrenarse y evaluarse con un simple conjunto de datos sintéticos, y el usuario
puede introducir valores interactivos para obtener una recomendación.

Requisitos:
  - Python 3.6+
  - numpy
  - scikit-learn
  - pandas (opcional, solo para visualización rápida)

Uso:
    python 02_Algoritmo_toma_agua.py
"""

import sys

try:
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.metrics import classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def generar_datos_sinteticos(n=1000, random_state=42):
    """Genera un dataset sintético con múltiples variables para beber agua.

    La etiqueta `beber` se determina con una función no lineal:
      beber = (sed > 6) or (horas > 3 and temperatura > 28) or
              (actividad > 7) or (humedad > 75)

    Además se añade ruido aleatorio para hacer el problema menos trivial.
    """
    rng = np.random.RandomState(random_state)
    temp = rng.uniform(15, 40, size=n)            # °C
    sed = rng.uniform(0, 10, size=n)              # escala 0-10
    horas = rng.uniform(0, 8, size=n)             # horas desde la última bebida
    actividad = rng.uniform(0, 10, size=n)        # escala 0-10
    humedad = rng.uniform(20, 100, size=n)        # porcentaje

    X = np.vstack([temp, sed, horas, actividad, humedad]).T
    y = ((sed > 6) | ((horas > 3) & (temp > 28)) |
         (actividad > 7) | (humedad > 75)).astype(int)

    # agregar ruido con pequeñas probabilidades de invertir la etiqueta
    flip = rng.rand(n) < 0.05
    y[flip] = 1 - y[flip]

    return X, y


def entrenar_modelo(X, y):
    """Construye y ajusta un clasificador de bosque aleatorio con búsqueda de red."""
    base = RandomForestClassifier(random_state=0)
    params = {
        'n_estimators': [50, 100],
        'max_depth': [None, 5, 10],
    }
    cv = GridSearchCV(base, params, cv=3, n_jobs=-1)
    cv.fit(X, y)
    print("Mejores parámetros:", cv.best_params_)
    return cv.best_estimator_


def decision_reglas(temp, sed, horas, actividad, humedad):
    """Versión de reglas/híbrida para decidir si beber agua.

    Se utiliza una combinación de umbrales y términos borrosos simples.
    """
    # reglas simples
    if sed > 7:
        return True
    if horas > 4 and temp > 30:
        return True
    if actividad > 8:
        return True
    if humedad > 80 and temp > 25:
        return True
    # por defecto no beber
    return False


def predecir(model, features):
    """Predice usando el modelo entrenado."""
    return bool(model.predict([features])[0])


def main():
    print("--- Algoritmo avanzado para decidir si tomar agua ---")

    try:
        temp = float(input("Temperatura ambiente (°C): "))
        sed = float(input("Nivel de sed (0-10): "))
        horas = float(input("Horas desde la última bebida: "))
        actividad = float(input("Nivel de actividad física (0-10): "))
        humedad = float(input("Humedad relativa (%): "))
    except ValueError:
        print("Entrada inválida, se esperaban números.")
        sys.exit(1)

    features = [temp, sed, horas, actividad, humedad]

    if SKLEARN_AVAILABLE:
        # entrenar un bosque aleatorio y evaluar
        X, y = generar_datos_sinteticos()
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.3,
                                                            random_state=0)
        model = entrenar_modelo(X_train, y_train)
        print("Evaluación sobre conjunto de prueba:")
        print(classification_report(y_test, model.predict(X_test)))
        decision = predecir(model, features)
        print("(predicción mediante modelo de bosque aleatorio)")
    else:
        decision = decision_reglas(temp, sed, horas, actividad, humedad)
        print("(predicción mediante reglas simples)")

    if decision:
        print("💧 Deberías tomar agua.")
    else:
        print("🚫 No es necesario beber agua ahora.")


if __name__ == '__main__':
    main()
