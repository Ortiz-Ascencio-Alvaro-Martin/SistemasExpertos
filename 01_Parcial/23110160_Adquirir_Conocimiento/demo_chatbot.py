#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demostración del Chatbot con Módulo de Adquisición de Conocimiento
Muestra cómo funciona el fuzzy matching y la adquisición de conocimiento
"""

from chatbot_adquisicion_conocimiento import ChatbotKnowledgeModule


def demo_fuzzy_matching():
    """Demostración de fuzzy matching sin interacción del usuario."""
    print("\n" + "="*70)
    print("📊 DEMOSTRACIÓN: FUZZY MATCHING Y SIMILITUD")
    print("="*70 + "\n")
    
    chatbot = ChatbotKnowledgeModule()
    
    # Preguntas de prueba con diferentes niveles de similitud
    preguntas_prueba = [
        "Hola",           # Exacta
        "hola!!",         # Con puntuación y mayúsculas
        "¿Cómo vas?",     # Similar a "¿Cómo estás?"
        "como estas",     # Normalizada
        "¡HOLA!",         # Con mayúsculas y puntuación
        "¿Hablar de qué?", # Baja similitud
        "Python",         # Muy baja similitud
    ]
    
    print("Análisis de similitud para cada pregunta:\n")
    
    for pregunta in preguntas_prueba:
        print(f"Pregunta: '{pregunta}'")
        coincidencias = chatbot.buscar_respuesta_fuzzy(pregunta)
        
        if coincidencias:
            top_3 = coincidencias[:3]
            for idx, match in enumerate(top_3, 1):
                similitud = match['similitud']
                
                # Colorear según rango de similitud
                if similitud > 85:
                    emoji = "✅"
                    accion = "→ Respuesta automática"
                elif similitud >= 60:
                    emoji = "❓"
                    accion = "→ Pedir confirmación"
                else:
                    emoji = "❌"
                    accion = "→ No coincide (aprender)"
                
                print(f"  {idx}. {emoji} '{match['pregunta_original']}' "
                      f"[Similitud: {similitud}%] {accion}")
        
        print()
    
    chatbot.cerrar()


def demo_base_de_datos():
    """Demostración del contenido de la base de datos."""
    print("\n" + "="*70)
    print("📚 DEMOSTRACIÓN: CONTENIDO DE LA BASE DE DATOS")
    print("="*70)
    
    chatbot = ChatbotKnowledgeModule()
    chatbot.listar_conocimiento()
    chatbot.cerrar()


def main():
    """Ejecuta la demostración."""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█  🤖 DEMOSTRACIÓN: CHATBOT CON ADQUISICIÓN DE CONOCIMIENTO" + " " * 7 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # Mostrar demostración de fuzzy matching
    demo_fuzzy_matching()
    
    # Mostrar base de datos
    demo_base_de_datos()
    
    print("\n" + "="*70)
    print("✅ Demostración completada")
    print("="*70)
    print("\n💡 Para usar el chatbot interactivamente, ejecuta:")
    print("   python3 chatbot_adquisicion_conocimiento.py\n")


if __name__ == "__main__":
    main()
