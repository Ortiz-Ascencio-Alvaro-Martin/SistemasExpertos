#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot de Cuidado de Mascotas con Casos Clínicos
Características:
- Registro de mascotas
- Información de cuidados por tipo de mascota
- Casos clínicos y síntomas
- Generación de reportes personalizados
- BD SQLite con múltiples tablas
"""

import sqlite3
import unicodedata
import string
import os
import sys
from datetime import datetime
from typing import Tuple, Optional, List, Dict
from thefuzz import fuzz


class ChatbotMascotas:
    """Chatbot inteligente para cuidado de mascotas."""
    
    DB_FILE = "mascotas_clinicos.db"
    SIMILARITY_HIGH = 85
    SIMILARITY_MEDIUM = 60
    
    def __init__(self):
        """Inicializa el chatbot y la base de datos."""
        self.conexion = None
        self._conectar_bd()
        self._crear_tablas()
        self._cargar_datos_iniciales()
        self.mascota_actual = None
    
    def _conectar_bd(self) -> None:
        """Conecta a la base de datos SQLite."""
        try:
            self.conexion = sqlite3.connect(self.DB_FILE)
            self.conexion.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"❌ Error al conectar a la BD: {e}")
            sys.exit(1)
    
    def _crear_tablas(self) -> None:
        """Crea las tablas de la base de datos."""
        try:
            cursor = self.conexion.cursor()
            
            # Tabla de mascotas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mascotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    tipo TEXT NOT NULL,
                    raza TEXT,
                    edad_años INTEGER,
                    peso_kg REAL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    propietario TEXT
                )
            """)
            
            # Tabla de información por tipo de mascota
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS informacion_mascotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_mascota TEXT UNIQUE NOT NULL,
                    descripcion TEXT NOT NULL,
                    cuidados_basicos TEXT NOT NULL,
                    alimentacion TEXT NOT NULL,
                    vacunas TEXT NOT NULL,
                    edad_promedio_vida TEXT
                )
            """)
            
            # Tabla de casos clínicos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS casos_clinicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mascota_id INTEGER NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sintomas TEXT NOT NULL,
                    diagnostico TEXT,
                    tratamiento TEXT,
                    medicamentos TEXT,
                    veterinario TEXT,
                    notas TEXT,
                    FOREIGN KEY(mascota_id) REFERENCES mascotas(id)
                )
            """)
            
            # Tabla de enfermedades comunes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enfermedades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    tipo_mascota TEXT NOT NULL,
                    sintomas TEXT NOT NULL,
                    prevención TEXT NOT NULL,
                    tratamiento TEXT NOT NULL
                )
            """)
            
            # Tabla de recomendaciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recomendaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tema TEXT NOT NULL,
                    contenido TEXT NOT NULL,
                    tipo_mascota TEXT
                )
            """)
            
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al crear tablas: {e}")
            sys.exit(1)
    
    def _cargar_datos_iniciales(self) -> None:
        """Carga datos iniciales en la BD."""
        cursor = self.conexion.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) as count FROM informacion_mascotas")
        if cursor.fetchone()['count'] > 0:
            return
        
        try:
            # Información de mascotas
            info_mascotas = [
                (
                    "Perro",
                    "Animal leal y sociable, requiere atención regular",
                    "Paseos diarios, juegos, adiestramiento, socialización",
                    "Alimento balanceado de calidad, agua fresca siempre disponible",
                    "Rabia, DHPP (moquillo, hepatitis, parvovirosis, parainfluenza), antiparasitarios",
                    "10-15 años"
                ),
                (
                    "Gato",
                    "Animal independiente, cazador natural, requiere enriquecimiento ambiental",
                    "Rascadores, juguetes, espacios elevados, limpieza de arenero",
                    "Alimento balanceado, agua fresca, evitar alimentos tóxicos",
                    "Rabia, FVRCP (panleucopenia, rinotraqueítis, calicivirus), antiparasitarios",
                    "12-18 años"
                ),
                (
                    "Conejo",
                    "Animal herbívoro, requiere jaula espaciosa y ejercicio",
                    "Jaula limpia, ejercicio diario, espacio para saltar, revisiones de dientes",
                    "Heno de calidad, verduras frescas, pellets limitados",
                    "Mixomatosis, enfermedad hemorrágica vírica, desparasitante",
                    "8-12 años"
                ),
                (
                    "Ave (Loro/Canario)",
                    "Animal social, requiere estimulación mental y ambiental",
                    "Jaula espaciosa, juguetes variados, luz natural, interacción",
                    "Semillas variadas, frutas, verduras, minerales",
                    "Vacunación según análisis veterinario, antiparasitarios",
                    "5-80 años (según especie)"
                ),
                (
                    "Pez",
                    "Animal acuático, requiere acuario adecuado y mantenimiento",
                    "Acuario limpio, filtración adecuada, temperatura controlada",
                    "Alimento comercial en cantidad adecuada, cambios de agua",
                    "Depende de especie, tratamiento de agua químicos",
                    "3-10 años"
                )
            ]
            
            cursor.executemany(
                """INSERT INTO informacion_mascotas 
                   (tipo_mascota, descripcion, cuidados_basicos, alimentacion, vacunas, edad_promedio_vida)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                info_mascotas
            )
            
            # Enfermedades comunes
            enfermedades = [
                (
                    "Parvovirosis",
                    "Perro",
                    "Diarrea con sangre, vómitos, letargo, deshidratación",
                    "Vacunación DHPP, evitar contacto con animales infectados",
                    "Tratamiento de síntomas, fluidoterapia, antibióticos si hay infección secundaria"
                ),
                (
                    "Panleucopenia Felina",
                    "Gato",
                    "Vómitos, diarrea, letargo, fiebre, disminución de glóbulos blancos",
                    "Vacunación FVRCP, higiene, evitar contacto con gatos infectados",
                    "Tratamiento de síntomas, antibióticos, fluidoterapia"
                ),
                (
                    "Otitis",
                    "Perro",
                    "Sacudir orejas, rascado, mal olor, secreción",
                    "Limpiar orejas regularmente, evitar agua en los oídos",
                    "Limpieza de oído, gotas medicadas, antibióticos si es bacteriana"
                ),
                (
                    "Obesidad",
                    "Perro",
                    "Sobrepeso excesivo, dificultad para caminar, respiración pesada",
                    "Control de peso, ejercicio regular, dieta balanceada",
                    "Dieta especial, aumento gradual de ejercicio, control veterinario"
                ),
                (
                    "Insuficiencia Renal",
                    "Gato",
                    "Aumento de sed, orina frecuente, pérdida de peso, letargo",
                    "Controles periódicos en gatos mayores, hidratación adecuada",
                    "Dieta renal especial, fluidoterapia, medicamentos según caso"
                )
            ]
            
            cursor.executemany(
                """INSERT INTO enfermedades 
                   (nombre, tipo_mascota, sintomas, prevención, tratamiento)
                   VALUES (?, ?, ?, ?, ?)""",
                enfermedades
            )
            
            # Recomendaciones generales
            recomendaciones = [
                (
                    "Higiene",
                    "Baños regulares, cepillado, limpieza de orejas y dientes",
                    "Perro"
                ),
                (
                    "Ejercicio",
                    "Al menos 30 minutos diarios de actividad física",
                    "Perro"
                ),
                (
                    "Revisión Veterinaria",
                    "Al menos una vez por año, dos veces en animales mayores",
                    None
                ),
                (
                    "Desparasitación",
                    "Según recomendación veterinaria, usualmente cada 3-6 meses",
                    None
                ),
                (
                    "Identificación",
                    "Microchip o collar con datos de contacto",
                    "Perro"
                )
            ]
            
            cursor.executemany(
                """INSERT INTO recomendaciones 
                   (tema, contenido, tipo_mascota)
                   VALUES (?, ?, ?)""",
                recomendaciones
            )
            
            self.conexion.commit()
            print("✅ Base de datos inicializada correctamente.\n")
        except sqlite3.Error as e:
            print(f"❌ Error al cargar datos iniciales: {e}")
    
    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """Normaliza el texto del usuario."""
        texto = texto.lower().strip()
        texto_nfd = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = ''.join(
            char for char in texto_nfd 
            if unicodedata.category(char) != 'Mn'
        )
        texto_limpio = texto_sin_acentos.translate(
            str.maketrans('', '', string.punctuation)
        )
        return texto_limpio.strip()
    
    def registrar_mascota(self) -> bool:
        """Registra una nueva mascota en el sistema."""
        print("\n" + "="*60)
        print("📝 REGISTRO DE NUEVA MASCOTA")
        print("="*60)
        
        try:
            nombre = input("\n¿Nombre de la mascota?: ").strip()
            if not nombre:
                print("⚠️ El nombre es requerido.")
                return False
            
            print("\nTipos disponibles: Perro, Gato, Conejo, Ave, Pez")
            tipo = input("¿Tipo de mascota?: ").strip().capitalize()
            
            raza = input("¿Raza (opcional)?: ").strip() or "No especificada"
            
            try:
                edad = int(input("¿Edad en años?: ") or 0)
            except ValueError:
                edad = None
            
            try:
                peso = float(input("¿Peso en kg (opcional)?: ") or 0)
                peso = peso if peso > 0 else None
            except ValueError:
                peso = None
            
            propietario = input("¿Nombre del propietario (opcional)?: ").strip() or "No especificado"
            
            cursor = self.conexion.cursor()
            cursor.execute(
                """INSERT INTO mascotas 
                   (nombre, tipo, raza, edad_años, peso_kg, propietario)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (nombre, tipo, raza, edad, peso, propietario)
            )
            self.conexion.commit()
            
            self.mascota_actual = nombre
            print(f"\n✅ Mascota '{nombre}' registrada exitosamente.\n")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ La mascota '{nombre}' ya existe en el sistema.")
            return False
        except Exception as e:
            print(f"❌ Error al registrar mascota: {e}")
            return False
    
    def listar_mascotas(self) -> None:
        """Lista todas las mascotas registradas."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, nombre, tipo, raza, edad_años, propietario FROM mascotas ORDER BY nombre")
        mascotas = cursor.fetchall()
        
        if not mascotas:
            print("\n🐾 No hay mascotas registradas aún.\n")
            return
        
        print("\n" + "="*70)
        print("🐾 MASCOTAS REGISTRADAS")
        print("="*70)
        
        for mascota in mascotas:
            edad_info = f"{mascota['edad_años']} años" if mascota['edad_años'] else "No especificada"
            print(f"\n🐶 {mascota['nombre']} (ID: {mascota['id']})")
            print(f"   Tipo: {mascota['tipo']} | Raza: {mascota['raza']}")
            print(f"   Edad: {edad_info} | Propietario: {mascota['propietario']}")
        
        print("\n" + "="*70 + "\n")
    
    def seleccionar_mascota(self) -> Optional[int]:
        """Permite seleccionar una mascota por nombre."""
        nombre = input("\n🐾 ¿Nombre de la mascota?: ").strip()
        
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, nombre FROM mascotas WHERE LOWER(nombre) = LOWER(?)", (nombre,))
        resultado = cursor.fetchone()
        
        if resultado:
            self.mascota_actual = resultado['nombre']
            return resultado['id']
        
        print(f"⚠️ No se encontró mascota con el nombre '{nombre}'.")
        return None
    
    def registrar_caso_clinico(self, mascota_id: int) -> bool:
        """Registra un nuevo caso clínico para una mascota."""
        print("\n" + "="*60)
        print("🏥 NUEVO CASO CLÍNICO")
        print("="*60)
        
        try:
            sintomas = input("\n¿Síntomas observados?: ").strip()
            if not sintomas:
                print("⚠️ Los síntomas son requeridos.")
                return False
            
            diagnostico = input("¿Diagnóstico (si disponible)?: ").strip() or None
            tratamiento = input("¿Tratamiento recomendado?: ").strip() or None
            medicamentos = input("¿Medicamentos prescritos?: ").strip() or None
            veterinario = input("¿Veterinario que atiende?: ").strip() or None
            notas = input("¿Notas adicionales?: ").strip() or None
            
            cursor = self.conexion.cursor()
            cursor.execute(
                """INSERT INTO casos_clinicos 
                   (mascota_id, sintomas, diagnostico, tratamiento, medicamentos, veterinario, notas)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (mascota_id, sintomas, diagnostico, tratamiento, medicamentos, veterinario, notas)
            )
            self.conexion.commit()
            
            print("\n✅ Caso clínico registrado exitosamente.\n")
            return True
        except Exception as e:
            print(f"❌ Error al registrar caso clínico: {e}")
            return False
    
    def mostrar_informacion_mascota(self, tipo_mascota: str) -> None:
        """Muestra información sobre un tipo de mascota."""
        cursor = self.conexion.cursor()
        
        # Buscar información con fuzzy matching
        cursor.execute("SELECT * FROM informacion_mascotas")
        tipos = cursor.fetchall()
        
        mejor_match = None
        mejor_similitud = 0
        
        for tipo in tipos:
            similitud = fuzz.ratio(self.normalizar_texto(tipo_mascota), 
                                  self.normalizar_texto(tipo['tipo_mascota']))
            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_match = tipo
        
        if mejor_match and mejor_similitud > 50:
            print("\n" + "="*70)
            print(f"📋 INFORMACIÓN: {mejor_match['tipo_mascota'].upper()}")
            print("="*70)
            print(f"\n📝 Descripción:\n{mejor_match['descripcion']}")
            print(f"\n🏥 Cuidados Básicos:\n{mejor_match['cuidados_basicos']}")
            print(f"\n🍽️ Alimentación:\n{mejor_match['alimentacion']}")
            print(f"\n💉 Vacunaciones:\n{mejor_match['vacunas']}")
            print(f"\n📅 Esperanza de vida: {mejor_match['edad_promedio_vida']}")
            print("\n" + "="*70 + "\n")
        else:
            print(f"\n❌ No hay información disponible para '{tipo_mascota}'.")
            print("Tipos disponibles: Perro, Gato, Conejo, Ave, Pez\n")
    
    def mostrar_historial_clinico(self, mascota_id: int) -> None:
        """Muestra el historial clínico de una mascota."""
        cursor = self.conexion.cursor()
        
        # Obtener nombre de mascota
        cursor.execute("SELECT nombre FROM mascotas WHERE id = ?", (mascota_id,))
        mascota = cursor.fetchone()
        
        if not mascota:
            print("⚠️ Mascota no encontrada.")
            return
        
        # Obtener casos clínicos
        cursor.execute(
            """SELECT * FROM casos_clinicos 
               WHERE mascota_id = ? 
               ORDER BY fecha DESC""",
            (mascota_id,)
        )
        casos = cursor.fetchall()
        
        if not casos:
            print(f"\n📋 No hay casos clínicos registrados para {mascota['nombre']}.\n")
            return
        
        print("\n" + "="*70)
        print(f"🏥 HISTORIAL CLÍNICO: {mascota['nombre'].upper()}")
        print("="*70)
        
        for caso in casos:
            print(f"\n📅 Fecha: {caso['fecha']}")
            print(f"🔍 Síntomas: {caso['sintomas']}")
            if caso['diagnostico']:
                print(f"📋 Diagnóstico: {caso['diagnostico']}")
            if caso['tratamiento']:
                print(f"💊 Tratamiento: {caso['tratamiento']}")
            if caso['medicamentos']:
                print(f"💉 Medicamentos: {caso['medicamentos']}")
            if caso['veterinario']:
                print(f"👨‍⚕️ Veterinario: {caso['veterinario']}")
            if caso['notas']:
                print(f"📝 Notas: {caso['notas']}")
            print("-" * 70)
        
        print()
    
    def generar_reporte_mascota(self, mascota_id: int) -> None:
        """Genera un reporte detallado de una mascota."""
        cursor = self.conexion.cursor()
        
        # Obtener datos de mascota
        cursor.execute("SELECT * FROM mascotas WHERE id = ?", (mascota_id,))
        mascota = cursor.fetchone()
        
        if not mascota:
            print("⚠️ Mascota no encontrada.")
            return
        
        # Obtener casos clínicos
        cursor.execute(
            "SELECT * FROM casos_clinicos WHERE mascota_id = ? ORDER BY fecha DESC",
            (mascota_id,)
        )
        casos = cursor.fetchall()
        
        # Obtener información de tipo de mascota
        cursor.execute(
            "SELECT * FROM informacion_mascotas WHERE tipo_mascota = ?",
            (mascota['tipo'],)
        )
        info = cursor.fetchone()
        
        # Crear reporte
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre_archivo = f"reporte_{mascota['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("REPORTE DE MASCOTA\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Fecha de generación: {timestamp}\n\n")
                
                # Información general
                f.write("INFORMACIÓN GENERAL\n")
                f.write("-"*70 + "\n")
                f.write(f"Nombre: {mascota['nombre']}\n")
                f.write(f"Tipo: {mascota['tipo']}\n")
                f.write(f"Raza: {mascota['raza']}\n")
                f.write(f"Edad: {mascota['edad_años']} años\n")
                f.write(f"Peso: {mascota['peso_kg']} kg\n")
                f.write(f"Propietario: {mascota['propietario']}\n")
                f.write(f"Fecha de registro: {mascota['fecha_registro']}\n\n")
                
                # Información de cuidados
                if info:
                    f.write("INFORMACIÓN DE CUIDADOS\n")
                    f.write("-"*70 + "\n")
                    f.write(f"Descripción: {info['descripcion']}\n")
                    f.write(f"Cuidados básicos: {info['cuidados_basicos']}\n")
                    f.write(f"Alimentación: {info['alimentacion']}\n")
                    f.write(f"Vacunaciones recomendadas: {info['vacunas']}\n")
                    f.write(f"Esperanza de vida: {info['edad_promedio_vida']}\n\n")
                
                # Historial clínico
                f.write("HISTORIAL CLÍNICO\n")
                f.write("-"*70 + "\n")
                if casos:
                    f.write(f"Total de casos registrados: {len(casos)}\n\n")
                    for idx, caso in enumerate(casos, 1):
                        f.write(f"Caso #{idx}\n")
                        f.write(f"Fecha: {caso['fecha']}\n")
                        f.write(f"Síntomas: {caso['sintomas']}\n")
                        if caso['diagnostico']:
                            f.write(f"Diagnóstico: {caso['diagnostico']}\n")
                        if caso['tratamiento']:
                            f.write(f"Tratamiento: {caso['tratamiento']}\n")
                        if caso['medicamentos']:
                            f.write(f"Medicamentos: {caso['medicamentos']}\n")
                        if caso['veterinario']:
                            f.write(f"Veterinario: {caso['veterinario']}\n")
                        if caso['notas']:
                            f.write(f"Notas: {caso['notas']}\n")
                        f.write("\n")
                else:
                    f.write("No hay casos clínicos registrados.\n\n")
                
                f.write("="*70 + "\n")
                f.write("FIN DEL REPORTE\n")
                f.write("="*70 + "\n")
            
            print(f"\n✅ Reporte generado: {nombre_archivo}\n")
        except Exception as e:
            print(f"\n❌ Error al generar reporte: {e}\n")
    
    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal."""
        print("\n" + "="*70)
        print("🐾 CHATBOT DE CUIDADO DE MASCOTAS - CASOS CLÍNICOS")
        print("="*70)
        print("\nOpciones disponibles:")
        print("  1. Registrar nueva mascota")
        print("  2. Listar mascotas")
        print("  3. Ver información de mascota (tipo)")
        print("  4. Registrar caso clínico")
        print("  5. Ver historial clínico")
        print("  6. Generar reporte de mascota")
        print("  7. Ver enfermedades comunes")
        print("  8. Ver recomendaciones de cuidado")
        print("  9. Ayuda")
        print("  0. Salir")
        print("="*70 + "\n")
    
    def mostrar_enfermedades(self) -> None:
        """Muestra las enfermedades comunes."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT DISTINCT tipo_mascota FROM enfermedades")
        tipos = [row[0] for row in cursor.fetchall()]
        
        print(f"\nTipos disponibles: {', '.join(tipos)}")
        tipo = input("¿Tipo de mascota?: ").strip()
        
        cursor.execute(
            "SELECT * FROM enfermedades WHERE tipo_mascota = ? ORDER BY nombre",
            (tipo,)
        )
        enfermedades = cursor.fetchall()
        
        if not enfermedades:
            print(f"\n⚠️ No hay enfermedades registradas para {tipo}.\n")
            return
        
        print("\n" + "="*70)
        print(f"🦠 ENFERMEDADES COMUNES EN {tipo.upper()}")
        print("="*70)
        
        for enfermedad in enfermedades:
            print(f"\n🔴 {enfermedad['nombre']}")
            print(f"   Síntomas: {enfermedad['sintomas']}")
            print(f"   Prevención: {enfermedad['prevención']}")
            print(f"   Tratamiento: {enfermedad['tratamiento']}")
        
        print("\n" + "="*70 + "\n")
    
    def mostrar_recomendaciones(self) -> None:
        """Muestra recomendaciones de cuidado."""
        cursor = self.conexion.cursor()
        cursor.execute(
            """SELECT DISTINCT tipo_mascota FROM recomendaciones 
               WHERE tipo_mascota IS NOT NULL
               UNION ALL
               SELECT 'Todas' AS tipo_mascota"""
        )
        tipos = [row[0] for row in cursor.fetchall()]
        
        print(f"\nOpciones: {', '.join(tipos)}")
        tipo = input("¿Tipo de mascota (o Todas)?: ").strip().capitalize()
        
        if tipo.lower() == "todas":
            cursor.execute("SELECT * FROM recomendaciones ORDER BY tema")
        else:
            cursor.execute(
                """SELECT * FROM recomendaciones 
                   WHERE tipo_mascota = ? OR tipo_mascota IS NULL
                   ORDER BY tema""",
                (tipo,)
            )
        
        recomendaciones = cursor.fetchall()
        
        if not recomendaciones:
            print(f"\n⚠️ No hay recomendaciones para {tipo}.\n")
            return
        
        print("\n" + "="*70)
        print("💡 RECOMENDACIONES DE CUIDADO")
        print("="*70)
        
        for rec in recomendaciones:
            print(f"\n✅ {rec['tema']}")
            print(f"   {rec['contenido']}")
        
        print("\n" + "="*70 + "\n")
    
    def ejecutar(self) -> None:
        """Ejecuta el bucle principal del sistema."""
        self.limpiar_pantalla()
        
        while True:
            self.mostrar_menu_principal()
            opcion = input("👤 Elige una opción: ").strip()
            
            if opcion == "1":
                self.registrar_mascota()
            
            elif opcion == "2":
                self.listar_mascotas()
            
            elif opcion == "3":
                tipo = input("\n¿Tipo de mascota?: ").strip()
                self.mostrar_informacion_mascota(tipo)
            
            elif opcion == "4":
                mascota_id = self.seleccionar_mascota()
                if mascota_id:
                    self.registrar_caso_clinico(mascota_id)
            
            elif opcion == "5":
                mascota_id = self.seleccionar_mascota()
                if mascota_id:
                    self.mostrar_historial_clinico(mascota_id)
            
            elif opcion == "6":
                mascota_id = self.seleccionar_mascota()
                if mascota_id:
                    self.generar_reporte_mascota(mascota_id)
            
            elif opcion == "7":
                self.mostrar_enfermedades()
            
            elif opcion == "8":
                self.mostrar_recomendaciones()
            
            elif opcion == "9":
                self.mostrar_menu_principal()
            
            elif opcion == "0":
                print("\n👋 ¡Hasta luego!\n")
                break
            
            else:
                print("⚠️ Opción no válida. Intenta de nuevo.\n")
    
    @staticmethod
    def limpiar_pantalla() -> None:
        """Limpia la pantalla."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def cerrar(self) -> None:
        """Cierra la conexión a la BD."""
        if self.conexion:
            self.conexion.close()


def main():
    """Función principal."""
    chatbot = ChatbotMascotas()
    
    try:
        chatbot.ejecutar()
    finally:
        chatbot.cerrar()


if __name__ == "__main__":
    main()
