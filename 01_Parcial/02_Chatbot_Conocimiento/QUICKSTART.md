#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUÍA RÁPIDA: CHATBOT CON MÓDULO DE ADQUISICIÓN DE CONOCIMIENTO
================================================================

INICIO RÁPIDO:
1. Instala dependencias:
   pip install -r requirements.txt

2. Ejecuta el chatbot:
   python3 chatbot_adquisicion_conocimiento.py

3. O ve la demostración:
   python3 demo_chatbot.py


FLUJO DE FUNCIONAMIENTO:
========================

┌────────────────────────────────────┐
│   Usuario escribe pregunta         │
└────────────┬───────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│  Normalizar texto:                 │
│  • Minúsculas                      │
│  • Sin acentos                     │
│  • Sin puntuación                  │
└────────────┬───────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│  Búsqueda Fuzzy Matching           │
│  (token_set_ratio)                 │
└────────────┬───────────────────────┘
             │
      ┌──────┴──────┬─────────┬──────────┐
      │             │         │          │
      ▼             ▼         ▼          ▼
   > 85%        60-85%      < 60%       Sin match
      │             │         │          │
      │             │         │          │
   RESPUESTA   CONFIRMAR   APRENDER    ERROR
   AUTOMÁTICA  "¿Quisiste  "No sé,
               decir...?"  ¿Qué debería
                          responder?"


LÓGICA DE SIMILITUD:
====================

   ✅ > 85%:     Respuesta automática
                 Ejemplo: "Hola!!" → "Hola" (100%)

   ❓ 60-85%:    Pregunta de confirmación
                 Ejemplo: "¿Cómo vas?" → "¿Cómo estás?" (78%)

   ❌ < 60%:     Módulo de adquisición (aprender)
                 Ejemplo: "¿Hablas de IA?" (18%) → Preguntar respuesta


EJEMPLO DE SESIÓN:
==================

👤 Tú: Hola
🤖 Bot: ¡Hola! ¿Cómo estás?

👤 Tú: como estas
🤖 Bot: Muy bien, gracias por preguntar. ¿Y tú?

👤 Tú: como andas
❓ ¿Quisiste decir: '¿Cómo estás?'? (s/n): n
❌ No sé cómo responder a eso.
📚 ¿Qué debería responder a 'como andas'?: Ando bien, ¿y tú?
✅ Nuevo conocimiento adquirido y guardado.

👤 Tú: :lista
[muestra todas las preguntas y respuestas]

👤 Tú: :salir
👋 ¡Hasta luego!


COMANDOS DISPONIBLES:
====================

Comando                   Descripción
─────────────────────────────────────────────
Cualquier texto          Hace una pregunta al bot
:lista                   Lista toda la base de conocimiento
:limpiar                 Limpia la pantalla
:ayuda                   Muestra el menú de ayuda
:salir                   Termina el programa
Ctrl+C                   Interrumpe el programa


ESTRUCTURA DE ARCHIVOS:
======================

/workspaces/SistemasExpertos/
├── chatbot_adquisicion_conocimiento.py    ← SCRIPT PRINCIPAL
├── demo_chatbot.py                        ← DEMOSTRACIÓN
├── chatbot_conocimiento.db                ← BD (se crea automáticamente)
├── requirements.txt                       ← DEPENDENCIAS
├── CHATBOT_README.md                      ← DOCUMENTACIÓN COMPLETA
└── QUICKSTART.md                          ← ESTA GUÍA


CARACTERÍSTICAS TÉCNICAS:
========================

✓ Clase ChatbotKnowledgeModule con métodos especializados
✓ Normalización robusta de texto (acentos, puntuación)
✓ Fuzzy matching con fuzz.token_set_ratio()
✓ DB SQLite con timestamps y UNIQUE constraints
✓ Manejo de excepciones completo
✓ Código documentado y bien estructurado
✓ Interfaz limpia con emojis y colores
✓ Prevención de duplicados normalizados


PREGUNTAS FRECUENTES:
====================

Q: ¿Dónde se guarda la BD?
A: En el archivo 'chatbot_conocimiento.db' en el directorio actual

Q: ¿Puedo borrar la BD para empezar de cero?
A: Sí, simplemente elimina 'chatbot_conocimiento.db' y el bot creará una nueva

Q: ¿Qué pasa si digo 's' o 'n' a la confirmación?
A: Si dices 's' (sí), responde la pregunta similar.
   Si dices 'n' (no), entra en modo de adquisición de conocimiento.

Q: ¿Puedo editar directamente la BD?
A: Sí, es un archivo SQLite estándar. Puedes usar:
   sqlite3 chatbot_conocimiento.db

Q: ¿Cómo mejorar la similitud del fuzzy matching?
A: Varía los thresholds:
   SIMILARITY_HIGH = 85  (cambiar 85 por otro número)
   SIMILARITY_MEDIUM = 60


PRÓXIMAS MEJORAS SUGERIDAS:
==========================

• Exportar/importar conocimiento (JSON, CSV)
• Estadísticas de uso
• Logs de conversaciones
• Interfaz gráfica
• NLP más avanzado (spaCy, NLTK)
• Sinónimos automáticos
• Categorización de preguntas


═══════════════════════════════════════════════════════════════════════
Desarrollado como solución profesional en Python 3 por un desarrollador senior
═══════════════════════════════════════════════════════════════════════
"""

# Si ejecutas este archivo, simplemente imprime la guía
if __name__ == "__main__":
    print(__doc__)
