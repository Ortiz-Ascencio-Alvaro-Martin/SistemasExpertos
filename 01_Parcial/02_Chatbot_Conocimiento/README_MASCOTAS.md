# 🐾 Chatbot de Cuidado de Mascotas con Casos Clínicos

## Descripción

Sistema inteligente para gestionar información de mascotas, casos clínicos y generar reportes personalizados. Orientado al cuidado preventivo y registro médico de animales de compañía.

## Características Principales

✅ **Registro de Mascotas**
- Almacenar información: nombre, tipo, raza, edad, peso
- Propietario y fecha de registro

✅ **5 Tipos de Mascotas**
- Perros
- Gatos
- Conejos
- Aves (Loros, Canarios)
- Peces

✅ **Información de Cuidados**
- Descripción y características
- Cuidados básicos
- Alimentación recomendada
- Vacunaciones necesarias
- Esperanza de vida

✅ **Casos Clínicos**
- Registro de síntomas
- Diagnósticos
- Tratamientos
- Medicamentos prescritos
- Veterinario que atiende
- Notas adicionales

✅ **Enfermedades Comunes**
- Base de datos de 5+ enfermedades por mascota
- Síntomas característicos
- Prevención
- Tratamiento

✅ **Generación de Reportes**
- Reportes en TXT con toda la información
- Historial clínico completo
- Información de cuidados
- Timestamp automático

✅ **Base de Datos Robusta**
- 6 tablas SQLite relacionadas
- Integridad referencial
- Timestamps en todos los registros

## Estructura de Base de Datos

```
mascotas_clinicos.db
├── mascotas
│   ├── id (PK)
│   ├── nombre (UNIQUE)
│   ├── tipo
│   ├── raza
│   ├── edad_años
│   ├── peso_kg
│   ├── propietario
│   └── fecha_registro

├── informacion_mascotas
│   ├── id (PK)
│   ├── tipo_mascota (UNIQUE)
│   ├── descripcion
│   ├── cuidados_basicos
│   ├── alimentacion
│   ├── vacunas
│   └── edad_promedio_vida

├── casos_clinicos
│   ├── id (PK)
│   ├── mascota_id (FK)
│   ├── fecha
│   ├── sintomas
│   ├── diagnostico
│   ├── tratamiento
│   ├── medicamentos
│   ├── veterinario
│   └── notas

├── enfermedades
│   ├── id (PK)
│   ├── nombre (UNIQUE)
│   ├── tipo_mascota
│   ├── sintomas
│   ├── prevención
│   └── tratamiento

└── recomendaciones
    ├── id (PK)
    ├── tema
    ├── contenido
    └── tipo_mascota (nullable)
```

## Uso

### Iniciar el Sistema

```bash
cd /workspaces/SistemasExpertos/01_Parcial/02_Chatbot_Conocimiento
source ../../.venv/bin/activate
python3 chatbot_mascotas.py
```

### Menú Principal

```
🐾 CHATBOT DE CUIDADO DE MASCOTAS - CASOS CLÍNICOS
======================================================================

Opciones disponibles:
  1. Registrar nueva mascota
  2. Listar mascotas
  3. Ver información de mascota (tipo)
  4. Registrar caso clínico
  5. Ver historial clínico
  6. Generar reporte de mascota
  7. Ver enfermedades comunes
  8. Ver recomendaciones de cuidado
  9. Ayuda
  0. Salir
```

## Ejemplos de Uso

### 1. Registrar una Mascota

```
👤 Elige una opción: 1

📝 REGISTRO DE NUEVA MASCOTA
============================================================

¿Nombre de la mascota?: Max
¿Tipo de mascota?: Perro
¿Raza (opcional)?: Golden Retriever
¿Edad en años?: 5
¿Peso en kg (opcional)?: 32.5
¿Nombre del propietario (opcional)?: Juan Pérez

✅ Mascota 'Max' registrada exitosamente.
```

### 2. Listar Mascotas

```
👤 Elige una opción: 2

🐾 MASCOTAS REGISTRADAS
======================================================================

🐶 Max (ID: 1)
   Tipo: Perro | Raza: Golden Retriever
   Edad: 5 años | Propietario: Juan Pérez

🐱 Luna (ID: 2)
   Tipo: Gato | Raza: Siamés
   Edad: 3 años | Propietario: María García

======================================================================
```

### 3. Ver Información de Cuidados

```
👤 Elige una opción: 3

¿Tipo de mascota?: Perro

📋 INFORMACIÓN: PERRO
======================================================================

📝 Descripción:
Animal leal y sociable, requiere atención regular

🏥 Cuidados Básicos:
Paseos diarios, juegos, adiestramiento, socialización

🍽️ Alimentación:
Alimento balanceado de calidad, agua fresca siempre disponible

💉 Vacunaciones:
Rabia, DHPP (moquillo, hepatitis, parvovirosis, parainfluenza), antiparasitarios

📅 Esperanza de vida: 10-15 años

======================================================================
```

### 4. Registrar Caso Clínico

```
👤 Elige una opción: 4
¿Nombre de la mascota?: Max

🏥 NUEVO CASO CLÍNICO
============================================================

¿Síntomas observados?: Tos persistente, letargo
¿Diagnóstico (si disponible)?: Posible traqueobronquitis
¿Tratamiento recomendado?: Reposo, antitusígenos
¿Medicamentos prescritos?: Doxiciclina 250mg cada 12 horas
¿Veterinario que atiende?: Dr. González
¿Notas adicionales?: Seguimiento en 5 días

✅ Caso clínico registrado exitosamente.
```

### 5. Ver Historial Clínico

```
👤 Elige una opción: 5
¿Nombre de la mascota?: Max

🏥 HISTORIAL CLÍNICO: MAX
======================================================================

📅 Fecha: 2026-03-08 15:30:00
🔍 Síntomas: Tos persistente, letargo
📋 Diagnóstico: Posible traqueobronquitis
💊 Tratamiento: Reposo, antitusígenos
💉 Medicamentos: Doxiciclina 250mg cada 12 horas
👨‍⚕️ Veterinario: Dr. González
📝 Notas: Seguimiento en 5 días
----------------------------------------------------------------------

======================================================================
```

### 6. Generar Reporte

```
👤 Elige una opción: 6
¿Nombre de la mascota?: Max

✅ Reporte generado: reporte_Max_20260308_153045.txt
```

**Contenido del reporte (reporte_Max_20260308_153045.txt):**

```
======================================================================
REPORTE DE MASCOTA
======================================================================

Fecha de generación: 2026-03-08 15:45:30

INFORMACIÓN GENERAL
----------------------------------------------------------------------
Nombre: Max
Tipo: Perro
Raza: Golden Retriever
Edad: 5 años
Peso: 32.5 kg
Propietario: Juan Pérez
Fecha de registro: 2026-03-08 15:30:00

INFORMACIÓN DE CUIDADOS
----------------------------------------------------------------------
Descripción: Animal leal y sociable, requiere atención regular
Cuidados básicos: Paseos diarios, juegos, adiestramiento, socialización
Alimentación: Alimento balanceado de calidad, agua fresca siempre disponible
Vacunaciones recomendadas: Rabia, DHPP...
Esperanza de vida: 10-15 años

HISTORIAL CLÍNICO
----------------------------------------------------------------------
Total de casos registrados: 1

Caso #1
Fecha: 2026-03-08 15:30:00
Síntomas: Tos persistente, letargo
Diagnóstico: Posible traqueobronquitis
Tratamiento: Reposo, antitusígenos
Medicamentos: Doxiciclina 250mg cada 12 horas
Veterinario: Dr. González
Notas: Seguimiento en 5 días

======================================================================
FIN DEL REPORTE
======================================================================
```

### 7. Ver Enfermedades Comunes

```
👤 Elige una opción: 7

Tipos disponibles: Perro, Gato

¿Tipo de mascota?: Perro

🦠 ENFERMEDADES COMUNES EN PERRO
======================================================================

🔴 Parvovirosis
   Síntomas: Diarrea con sangre, vómitos, letargo, deshidratación
   Prevención: Vacunación DHPP, evitar contacto con animales infectados
   Tratamiento: Tratamiento de síntomas, fluidoterapia, antibióticos si hay infección secundaria

🔴 Otitis
   Síntomas: Sacudir orejas, rascado, mal olor, secreción
   Prevención: Limpiar orejas regularmente, evitar agua en los oídos
   Tratamiento: Limpieza de oído, gotas medicadas, antibióticos si es bacteriana

🔴 Obesidad
   Síntomas: Sobrepeso excesivo, dificultad para caminar, respiración pesada
   Prevención: Control de peso, ejercicio regular, dieta balanceada
   Tratamiento: Dieta especial, aumento gradual de ejercicio, control veterinario

======================================================================
```

### 8. Ver Recomendaciones

```
👤 Elige una opción: 8

Opciones: Perro, Gato, Conejo, Ave, Pez, Todas

¿Tipo de mascota (o Todas)?: Perro

💡 RECOMENDACIONES DE CUIDADO
======================================================================

✅ Higiene
   Baños regulares, cepillado, limpieza de orejas y dientes

✅ Ejercicio
   Al menos 30 minutos diarios de actividad física

✅ Identificación
   Microchip o collar con datos de contacto

✅ Revisión Veterinaria
   Al menos una vez por año, dos veces en animales mayores

======================================================================
```

## Datos Iniciales Preargados

### Mascotas (5 tipos)
1. **Perro**: Cuidados, alimentación, vacunas
2. **Gato**: Información específica de felinos
3. **Conejo**: Guía de cuidados herbívoros
4. **Ave**: Loros y canarios
5. **Pez**: Peces de acuario

### Enfermedades (5+ por mascota)
- Parvovirosis (Perro)
- Panleucopenia Felina (Gato)
- Otitis (Perro)
- Obesidad (Perro)
- Insuficiencia Renal (Gato)

### Recomendaciones Generales
- Higiene
- Ejercicio
- Revisión Veterinaria
- Desparasitación
- Identificación

## Características Técnicas

✅ **Clase ChatbotMascotas** con métodos especializados
✅ **BD SQLite** con 6 tablas relacionadas
✅ **Manejo robusto de excepciones**
✅ **Timestamps automáticos** en todos los registros
✅ **Generación de reportes** en archivos TXT
✅ **Interfaz amigable** con menú de opciones
✅ **Validación de entrada** en registros
✅ **Código bien documentado** y profesional

## Mejoras Futuras

- [ ] Exportar reportes a PDF
- [ ] Alertas de citas veterinarias
- [ ] Seguimiento de vacunas
- [ ] Grráficos de peso
- [ ] Integración con veterinarios
- [ ] Recordatorios de medicamentos
- [ ] Sistema de fotografías
- [ ] Búsqueda de casos similares

## Requisitos

```
thefuzz==0.22.1
python-Levenshtein==0.27.3
Python 3.6+
```

## Notas

- Los reportes se generan automáticamente con timestamp
- Todos los datos se guardan en SQLite
- Puedes eliminar `mascotas_clinicos.db` para reiniciar desde cero
- La BD se crea automáticamente al iniciar

---

**Sistema desarrollado para veterinarias, clínicas y cuidadores de mascotas**

**Versión: 2.0 - Orientada a Casos Clínicos**
