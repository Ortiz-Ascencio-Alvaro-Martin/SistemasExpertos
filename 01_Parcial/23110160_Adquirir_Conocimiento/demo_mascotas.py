#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración del Chatbot de Mascotas
Ejemplo de: Registro, casos, historial, reporte
"""

from chatbot_mascotas import ChatbotMascotas


def demo_registros_y_casos():
    """Demostración de registro de mascotas y casos clínicos."""
    print("\n" + "="*70)
    print("📊 DEMOSTRACIÓN: SISTEMA DE GESTIÓN DE MASCOTAS")
    print("="*70 + "\n")
    
    bot = ChatbotMascotas()
    
    # Mostrar tipos disponibles
    print("✅ Sistema inicializado correctamente.\n")
    
    # Mostrar información de mascotas
    print("📋 TIPOS DE MASCOTAS DISPONIBLES:\n")
    import sqlite3
    cursor = bot.conexion.cursor()
    cursor.execute("SELECT tipo_mascota, descripcion FROM informacion_mascotas")
    
    for mascota in cursor.fetchall():
        print(f"  • {mascota[0]}: {mascota[1]}")
    
    print("\n" + "="*70)
    print("📚 INFORMACIÓN PRECARGADA:")
    print("="*70)
    
    # Enfermedades
    cursor.execute("SELECT COUNT(*) as count FROM enfermedades")
    enferm_count = cursor.fetchone()['count']
    print(f"\n🦠 Enfermedades comunes: {enferm_count} registradas")
    
    cursor.execute("SELECT DISTINCT tipo_mascota FROM enfermedades ORDER BY tipo_mascota")
    tipos_enf = [row[0] for row in cursor.fetchall()]
    for tipo in tipos_enf:
        cursor.execute("SELECT COUNT(*) as count FROM enfermedades WHERE tipo_mascota = ?", (tipo,))
        count = cursor.fetchone()['count']
        print(f"   - {tipo}: {count} enfermedades")
    
    # Recomendaciones
    cursor.execute("SELECT COUNT(*) as count FROM recomendaciones")
    rec_count = cursor.fetchone()['count']
    print(f"\n💡 Recomendaciones de cuidado: {rec_count} registradas")
    
    cursor.execute("SELECT DISTINCT tema FROM recomendaciones")
    temas = [row[0] for row in cursor.fetchall()]
    print(f"   Temas: {', '.join(temas)}")
    
    print("\n" + "="*70)
    print("🐾 EJEMPLO: REGISTRO DE MASCOTA")
    print("="*70)
    
    print("""
    ENTRADA DEL USUARIO:
    → Elige opción: 1 (Registrar nueva mascota)
    → Nombre: Max
    → Tipo: Perro
    → Raza: Golden Retriever
    → Edad: 5 años
    → Peso: 32.5 kg
    → Propietario: Juan Pérez
    
    RESULTADO:
    ✅ Mascota 'Max' registrada exitosamente.
    """)
    
    # Intentar registrar una mascota de prueba
    print("📝 Registrando mascota de demostración...\n")
    
    try:
        cursor.execute(
            """INSERT INTO mascotas 
               (nombre, tipo, raza, edad_años, peso_kg, propietario)
               VALUES (?, ?, ?, ?, ?, ?)""",
            ("Max_Demo", "Perro", "Golden Retriever", 5, 32.5, "Juan Pérez")
        )
        bot.conexion.commit()
        mascota_id = cursor.lastrowid
        print(f"✅ Mascota registrada con ID: {mascota_id}\n")
        
        # Registrar caso clínico
        print("="*70)
        print("🏥 EJEMPLO: REGISTRO DE CASO CLÍNICO")
        print("="*70)
        
        print("""
        ENTRADA DEL USUARIO:
        → Elige opción: 4 (Registrar caso clínico)
        → Mascota: Max_Demo
        → Síntomas: Tos persistente, letargo
        → Diagnóstico: Posible traqueobronquitis
        → Tratamiento: Reposo, antitusígenos
        → Medicamentos: Doxiciclina 250mg
        → Veterinario: Dr. González
        → Notas: Seguimiento en 5 días
        
        RESULTADO:
        ✅ Caso clínico registrado exitosamente.
        """)
        
        cursor.execute(
            """INSERT INTO casos_clinicos 
               (mascota_id, sintomas, diagnostico, tratamiento, medicamentos, veterinario, notas)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (mascota_id, "Tos persistente, letargo", "Posible traqueobronquitis", 
             "Reposo, antitusígenos", "Doxiciclina 250mg cada 12 horas", 
             "Dr. González", "Seguimiento en 5 días")
        )
        bot.conexion.commit()
        print("✅ Caso clínico registrado.\n")
        
        # Mostrar historial
        print("="*70)
        print("🏥 HISTORIAL CLÍNICO DE MAX_DEMO")
        print("="*70 + "\n")
        
        cursor.execute(
            "SELECT * FROM casos_clinicos WHERE mascota_id = ? ORDER BY fecha DESC",
            (mascota_id,)
        )
        casos = cursor.fetchall()
        
        for caso in casos:
            print(f"📅 Fecha: {caso['fecha']}")
            print(f"🔍 Síntomas: {caso['sintomas']}")
            print(f"📋 Diagnóstico: {caso['diagnostico']}")
            print(f"💊 Tratamiento: {caso['tratamiento']}")
            print(f"💉 Medicamentos: {caso['medicamentos']}")
            print(f"👨‍⚕️ Veterinario: {caso['veterinario']}")
            print(f"📝 Notas: {caso['notas']}\n")
        
        # Mostrar información de cuidados
        print("="*70)
        print("📋 INFORMACIÓN DE CUIDADOS: PERRO")
        print("="*70 + "\n")
        
        cursor.execute("SELECT * FROM informacion_mascotas WHERE tipo_mascota = 'Perro'")
        info = cursor.fetchone()
        
        print(f"📝 Descripción:\n{info['descripcion']}\n")
        print(f"🏥 Cuidados básicos:\n{info['cuidados_basicos']}\n")
        print(f"🍽️ Alimentación:\n{info['alimentacion']}\n")
        print(f"💉 Vacunaciones:\n{info['vacunas']}\n")
        print(f"📅 Esperanza de vida: {info['edad_promedio_vida']}\n")
        
        # Mostrar enfermedades
        print("="*70)
        print("🦠 ENFERMEDADES COMUNES EN PERROS")
        print("="*70 + "\n")
        
        cursor.execute("SELECT * FROM enfermedades WHERE tipo_mascota = 'Perro' LIMIT 2")
        enferms = cursor.fetchall()
        
        for enferm in enferms:
            print(f"🔴 {enferm['nombre']}")
            print(f"   Síntomas: {enferm['sintomas']}")
            print(f"   Prevención: {enferm['prevención']}")
            print(f"   Tratamiento: {enferm['tratamiento']}\n")
        
        # Generar reporte
        print("="*70)
        print("📄 GENERACIÓN DE REPORTE")
        print("="*70 + "\n")
        
        print("Generando reporte para Max_Demo...\n")
        bot.generar_reporte_mascota(mascota_id)
        
        # Listar archivos generados
        import os
        archivos_reporte = [f for f in os.listdir('.') if f.startswith('reporte_Max_Demo')]
        if archivos_reporte:
            print(f"📁 Archivos generados:")
            for archivo in archivos_reporte:
                print(f"   • {archivo}")
        
    except Exception as e:
        print(f"Nota: {e}")
    
    finally:
        bot.cerrar()
    
    print("\n" + "="*70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("="*70)
    print("""
Para usar el sistema completo de forma interactiva:

    python3 chatbot_mascotas.py

O desde la raíz del proyecto:

    cd 01_Parcial/02_Chatbot_Conocimiento
    source ../../.venv/bin/activate
    python3 chatbot_mascotas.py
    """)


if __name__ == "__main__":
    demo_registros_y_casos()
