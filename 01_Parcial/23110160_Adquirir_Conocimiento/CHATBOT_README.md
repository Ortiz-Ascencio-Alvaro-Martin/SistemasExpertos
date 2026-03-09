# 🤖 Chatbot con Módulo de Adquisición de Conocimiento

## Descripción

Script Python profesional de un chatbot con capacidad de aprendizaje automático. Utiliza búsqueda difusa (fuzzy matching) para encontrar respuestas similares y adquirir nuevo conocimiento de forma interactiva.

## Características

✅ **Base de Datos SQLite**: Persistencia de conocimiento en archivo `chatbot_conocimiento.db`

✅ **Búsqueda Difusa**: Utiliza `thefuzz` para comparación inteligente de preguntas

✅ **Normalización de Texto**:
- Conversión a minúsculas
- Eliminación de acentos
- Remoción de signos de puntuación

✅ **Lógica de Similitud**:
- **> 85%** : Respuesta automática
- **60-85%** : Pregunta de confirmación
- **< 60%** : Módulo de adquisición (aprender respuesta)

✅ **Interfaz Limpia**: Bucle interactivo en terminal con menú de comandos

## Requisitos Previos

```bash
pip install thefuzz python-Levenshtein
```

## Instalación

1. Asegurate que estás en el directorio del proyecto
2. Instala las dependencias necesarias
3. ¡Listo! El script crea la BD automáticamente

## Uso

```bash
python3 chatbot_adquisicion_conocimiento.py
```

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| Cualquier pregunta | Interactúa con el chatbot |
| `:lista` | Muestra toda la base de conocimiento |
| `:limpiar` | Limpia la pantalla |
| `:ayuda` | Muestra el menú de ayuda |
| `:salir` | Termina el programa |
| `Ctrl+C` | Interrumpe el programa |

## Ejemplo de Uso

```
💬 Escribe tu pregunta (o ':ayuda' para ver comandos):

👤 Tú: Hola
🤖 Bot: ¡Hola! ¿Cómo estás?

👤 Tú: Como estas
❓ ¿Quisiste decir: '¿Cómo estás?'? (s/n): s
🤖 Bot: Muy bien, gracias por preguntar. ¿Y tú?

👤 Tú: Cuéntame sobre inteligencia artificial
❌ No sé cómo responder a eso.
📚 ¿Qué debería responder a 'Cuéntame sobre inteligencia artificial'?: 
La inteligencia artificial es una rama de la informática que estudia sistemas inteligentes.
✅ Nuevo conocimiento adquirido y guardado.

👤 Tú: :lista
📚 Base de Conocimiento (4 entradas)
============================================================
1. P: Hola
   R: ¡Hola! ¿Cómo estás?
...
```

## Estructura de la Base de Datos

Tabla: `conocimiento`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER | ID único (PK) |
| pregunta | TEXT | Pregunta del usuario |
| respuesta | TEXT | Respuesta del chatbot |
| creado_en | TIMESTAMP | Fecha de creación |

## Datos Iniciales

El chatbot precarga 3 entradas si la BD está vacía:

1. "Hola" → "¡Hola! ¿Cómo estás?"
2. "¿Cómo estás?" → "Muy bien, gracias por preguntar. ¿Y tú?"
3. "¿De qué te gustaría hablar?" → "Podemos hablar de robótica, programación o lo que quieras."

## Notas Técnicas

- **Token Set Ratio**: Utiliza `fuzz.token_set_ratio()` para mejor comparación de frases completas
- **Normalización**: Sistema robusto que maneja acentos y puntuación
- **Evita Duplicados**: Previene preguntas duplicadas en la BD
- **Row Factory**: SQLite retorna tuplas con acceso por nombre de columna

## Mejoras Futuras

- [ ] Guardar logs de conversaciones
- [ ] Estadísticas de uso de respuestas
- [ ] Exportar/importar conocimiento (JSON, CSV)
- [ ] Interfaz gráfica con tkinter
- [ ] Integración con NLP más avanzado
- [ ] Categorías de preguntas

## Autor

Desarrollado como una solución profesional en Python 3
