#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de configuración del Chatbot
Edita estos valores según tus necesidades
"""

# =============================================================================
# CONFIGURACIÓN DE SIMILITUD (0-100)
# =============================================================================

# Umbral para respuesta automática (> este valor = respuesta automática)
SIMILARITY_HIGH = 85

# Umbral mínimo para confirmación (entre este y SIMILARITY_HIGH = preguntar)
SIMILARITY_MEDIUM = 60

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================

# Nombre del archivo de base de datos
DB_FILE = "chatbot_conocimiento.db"

# =============================================================================
# DATOS INICIALES (PRECARGA)
# =============================================================================

DATOS_INICIALES = [
    ("Hola", "¡Hola! ¿Cómo estás?"),
    ("¿Cómo estás?", "Muy bien, gracias por preguntar. ¿Y tú?"),
    ("¿De qué te gustaría hablar?", "Podemos hablar de robótica, programación o lo que quieras.")
]

# =============================================================================
# MENSAJES PERSONALIZABLES
# =============================================================================

MENSAJES = {
    'inicio': "💬 Escribe tu pregunta (o ':ayuda' para ver comandos):\n",
    'respuesta_auto': "🤖 Bot: {}",
    'pregunta_confirmacion': "❓ ¿Quisiste decir: '{}'? (s/n): ",
    'no_sabe': "❌ No sé cómo responder a eso.",
    'adquirir_conocimiento': "📚 ¿Qué debería responder a '{}'?: ",
    'exito': "✅ Nuevo conocimiento adquirido y guardado.",
    'salida': "👋 ¡Hasta luego!",
    'interrupcion': "👋 Programa interrumpido. ¡Hasta luego!",
}

# =============================================================================
# OPCIONES DE FUZZY MATCHING
# =============================================================================

# Algoritmo a usar: 'token_set_ratio' (recomendado) o 'ratio'
FUZZY_ALGORITHM = 'token_set_ratio'

# =============================================================================
# INTERFAZ Y PRESENTACIÓN
# =============================================================================

# Mostrar emojis en la interfaz
USAR_EMOJIS = True

# Limpiar pantalla al iniciar
LIMPIAR_PANTALLA_INICIO = True

# Ancho del separador en caracteres
ANCHO_SEPARADOR = 60

# =============================================================================
# LOGGING Y DEBUG
# =============================================================================

# Modo debug (muestra más información)
DEBUG = False

# Guardar log de conversaciones
GUARDAR_LOG = False

ARCHIVO_LOG = "chatbot_conversaciones.log"

# =============================================================================
# EJEMPLO DE PERSONALIZACIÓN
# =============================================================================

"""
Para usar diferentes umbrales de similitud:

    # Más flexible (acepta coincidencias más lejanas)
    SIMILARITY_HIGH = 75
    SIMILARITY_MEDIUM = 45

    # Más estricto (solo coincidencias muy cercanas)
    SIMILARITY_HIGH = 95
    SIMILARITY_MEDIUM = 80

Para agregar datos iniciales personalizados:

    DATOS_INICIALES = [
        ("Hola", "¡Bienvenido!"),
        ("¿Quién eres?", "Soy tu asistente virtual"),
        ("¿Qué puedes hacer?", "Puedo responder preguntas y aprender nuevas respuestas")
    ]

Para cambiar mensajes:

    MENSAJES['respuesta_auto'] = "🎯 {}"
    MENSAJES['salida'] = "Hasta pronto, amigo!"
"""
