#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas unitarias básicas para el Chatbot
Valida el funcionamiento correcto de los componentes principales
"""

import sqlite3
import sys
import os
from chatbot_adquisicion_conocimiento import ChatbotKnowledgeModule


def test_normalizacion_texto():
    """Test: Función de normalización de texto."""
    print("\n" + "="*70)
    print("🧪 TEST 1: NORMALIZACIÓN DE TEXTO")
    print("="*70)
    
    casos_prueba = [
        ("¡HOLA!", "hola"),
        ("Cómo estás?", "como estas"),
        ("Adiós, amigo.", "adios amigo"),
        ("señor José", "senor jose"),
    ]
    
    for entrada, esperado in casos_prueba:
        resultado = ChatbotKnowledgeModule.normalizar_texto(entrada)
        estado = "✅ PASS" if resultado == esperado else f"❌ FAIL (obtuvo: {resultado})"
        print(f"  '{entrada}' → '{resultado}' {estado}")
    
    print()


def test_conexion_bd():
    """Test: Conexión a base de datos."""
    print("="*70)
    print("🧪 TEST 2: CONEXIÓN A BASE DE DATOS")
    print("="*70)
    
    try:
        chatbot = ChatbotKnowledgeModule()
        
        # Verificar que la tabla existe
        cursor = chatbot.conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conocimiento'")
        tabla_existe = cursor.fetchone() is not None
        
        print(f"  Tabla 'conocimiento' existe: {'✅ PASS' if tabla_existe else '❌ FAIL'}")
        
        # Verificar que hay datos iniciales
        cursor.execute("SELECT COUNT(*) as count FROM conocimiento")
        count = cursor.fetchone()['count']
        print(f"  Datos iniciales cargados: {'✅ PASS' if count == 3 else f'❌ FAIL (tiene {count} en lugar de 3)'}")
        
        chatbot.cerrar()
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
    
    print()


def test_fuzzy_matching():
    """Test: Búsqueda fuzzy matching."""
    print("="*70)
    print("🧪 TEST 3: FUZZY MATCHING")
    print("="*70)
    
    try:
        chatbot = ChatbotKnowledgeModule()
        
        # Pruebas de similitud
        pruebas = [
            ("Hola", "✅", 100),           # Exacta
            ("hola!!!", "✅", 100),        # Con puntuación
            ("¿Cómo estás?", "✅", 100),   # Exacta
            ("como estas", "✅", 100),     # Normalizada
            ("¿Cómo vas?", "❓", 60),      # Parcial (60-85%)
            ("Python", "❌", 0),           # Muy diferente
        ]
        
        for pregunta, esperado_emoji, similitud_minima in pruebas:
            coincidencias = chatbot.buscar_respuesta_fuzzy(pregunta)
            if coincidencias:
                similitud = coincidencias[0]['similitud']
                
                # Determinar emoji esperado
                if similitud > 85:
                    emoji = "✅"
                elif similitud >= 60:
                    emoji = "❓"
                else:
                    emoji = "❌"
                
                estado = "✅ PASS" if emoji == esperado_emoji else f"❌ FAIL (obtuvo {emoji})"
                print(f"  '{pregunta}' → {emoji} ({similitud}%) {estado}")
        
        chatbot.cerrar()
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
    
    print()


def test_guardar_conocimiento():
    """Test: Guardar nuevo conocimiento."""
    print("="*70)
    print("🧪 TEST 4: GUARDAR NUEVO CONOCIMIENTO")
    print("="*70)
    
    try:
        chatbot = ChatbotKnowledgeModule()
        
        # Contar iniciales
        cursor = chatbot.conexion.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM conocimiento")
        count_inicial = cursor.fetchone()['count']
        
        # Guardar nuevo conocimiento
        exito = chatbot.guardar_par_pregunta_respuesta(
            "¿Cuál es tu color favorito?",
            "Me gusta el azul."
        )
        
        # Contar finales
        cursor.execute("SELECT COUNT(*) as count FROM conocimiento")
        count_final = cursor.fetchone()['count']
        
        incremento_correcto = (count_final - count_inicial) == 1
        estado = "✅ PASS" if (exito and incremento_correcto) else "❌ FAIL"
        
        print(f"  Guardar conocimiento: {estado}")
        print(f"  Registros: {count_inicial} → {count_final} (incremento: {count_final - count_inicial})")
        
        chatbot.cerrar()
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
    
    print()


def test_evitar_duplicados():
    """Test: Evitar duplicados."""
    print("="*70)
    print("🧪 TEST 5: EVITAR DUPLICADOS")
    print("="*70)
    
    try:
        chatbot = ChatbotKnowledgeModule()
        
        # Intentar guardar una pregunta existente
        resultado = chatbot.guardar_par_pregunta_respuesta(
            "Hola",  # Ya existe
            "Respuesta diferente"
        )
        
        estado = "✅ PASS" if not resultado else "❌ FAIL (permitió duplicado)"
        print(f"  Prevención de duplicados: {estado}")
        
        chatbot.cerrar()
    except Exception as e:
        print(f"  ❌ FAIL: {e}")
    
    print()


def resumen_tests():
    """Imprime un resumen visual de los tests."""
    print("="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    print("""
Los tests anteriores validan:

✅ Normalización de texto (minúsculas, acentos, puntuación)
✅ Conexión a base de datos SQLite
✅ Creación automática de tabla 'conocimiento'
✅ Carga de datos iniciales
✅ Búsqueda fuzzy matching (similitud)
✅ Guardado de nuevo conocimiento
✅ Prevención de duplicados

Si todos los tests muestran ✅, el chatbot está listo para usar.
    """)
    print("="*70 + "\n")


def main():
    """Ejecuta todos los tests."""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█  🧪 SUITE DE PRUEBAS: CHATBOT CON ADQUISICIÓN DE CONOCIMIENTO" + " "*2 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    test_normalizacion_texto()
    test_conexion_bd()
    test_fuzzy_matching()
    test_guardar_conocimiento()
    test_evitar_duplicados()
    resumen_tests()
    
    print("\n💡 Para usar el chatbot interactivamente, ejecuta:")
    print("   python3 chatbot_adquisicion_conocimiento.py\n")


if __name__ == "__main__":
    main()
