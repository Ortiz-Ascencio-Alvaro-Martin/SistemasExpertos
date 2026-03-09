#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot con Módulo de Adquisición de Conocimiento
Desarrollado como desarrollador senior de Python
Características:
- BD SQLite para persistencia
- Búsqueda difusa (fuzzy matching)
- Módulo de aprendizaje automático de nuevas Q&A
- Normalización de texto
"""

import sqlite3
import unicodedata
import string
import os
import sys
from typing import Tuple, Optional, List
from thefuzz import fuzz


class ChatbotKnowledgeModule:
    """Módulo de chatbot con adquisición de conocimiento."""
    
    DB_FILE = "chatbot_conocimiento.db"
    SIMILARITY_HIGH = 85  # > 85% -> respuesta automática
    SIMILARITY_MEDIUM = 60  # 60-85% -> preguntar confirmación
    
    def __init__(self):
        """Inicializa el chatbot y la base de datos."""
        self.conexion = None
        self._conectar_bd()
        self._crear_tabla()
        self._cargar_datos_iniciales()
    
    def _conectar_bd(self) -> None:
        """Conecta a la base de datos SQLite."""
        try:
            self.conexion = sqlite3.connect(self.DB_FILE)
            self.conexion.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"❌ Error al conectar a la BD: {e}")
            sys.exit(1)
    
    def _crear_tabla(self) -> None:
        """Crea la tabla de conocimiento si no existe."""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conocimiento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pregunta TEXT UNIQUE NOT NULL,
                    respuesta TEXT NOT NULL,
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al crear tabla: {e}")
            sys.exit(1)
    
    def _cargar_datos_iniciales(self) -> None:
        """Carga datos iniciales si la BD está vacía."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM conocimiento")
        count = cursor.fetchone()['count']
        
        if count == 0:
            datos_iniciales = [
                ("Hola", "¡Hola! ¿Cómo estás?"),
                ("¿Cómo estás?", "Muy bien, gracias por preguntar. ¿Y tú?"),
                ("¿De qué te gustaría hablar?", "Podemos hablar de robótica, programación o lo que quieras.")
            ]
            try:
                cursor.executemany(
                    "INSERT INTO conocimiento (pregunta, respuesta) VALUES (?, ?)",
                    datos_iniciales
                )
                self.conexion.commit()
                print("✅ Datos iniciales cargados correctamente.\n")
            except sqlite3.Error as e:
                print(f"❌ Error al cargar datos iniciales: {e}")
    
    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """
        Normaliza el texto del usuario.
        - Convierte a minúsculas
        - Elimina acentos
        - Quita signos de puntuación
        """
        # Convertir a minúsculas
        texto = texto.lower().strip()
        
        # Eliminar acentos
        texto_nfd = unicodedata.normalize('NFD', texto)
        texto_sin_acentos = ''.join(
            char for char in texto_nfd 
            if unicodedata.category(char) != 'Mn'
        )
        
        # Quitar signos de puntuación
        texto_limpio = texto_sin_acentos.translate(
            str.maketrans('', '', string.punctuation)
        )
        
        return texto_limpio.strip()
    
    def obtener_todas_preguntas(self) -> List[Tuple[str, str, int]]:
        """Obtiene todas las preguntas de la BD con sus respuestas e IDs."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, pregunta, respuesta FROM conocimiento")
        return cursor.fetchall()
    
    def buscar_respuesta_fuzzy(self, pregunta_usuario: str) -> Optional[Tuple[str, int]]:
        """
        Busca la mejor coincidencia para la pregunta del usuario.
        Retorna: (respuesta, similitud) o None
        """
        pregunta_normalizada = self.normalizar_texto(pregunta_usuario)
        todas_preguntas = self.obtener_todas_preguntas()
        
        mejores_coincidencias = []
        
        for id_preg, pregunta_bd, respuesta in todas_preguntas:
            pregunta_bd_normalizada = self.normalizar_texto(pregunta_bd)
            
            # Usar token_set_ratio para mejor comparación
            similitud = fuzz.token_set_ratio(
                pregunta_normalizada,
                pregunta_bd_normalizada
            )
            
            mejores_coincidencias.append({
                'pregunta_original': pregunta_bd,
                'respuesta': respuesta,
                'similitud': similitud,
                'id': id_preg
            })
        
        # Ordenar por similitud descendente
        mejores_coincidencias.sort(key=lambda x: x['similitud'], reverse=True)
        
        if mejores_coincidencias:
            return mejores_coincidencias
        return None
    
    def guardar_par_pregunta_respuesta(self, pregunta: str, respuesta: str) -> bool:
        """Guarda un nuevo par pregunta-respuesta en la BD."""
        try:
            cursor = self.conexion.cursor()
            pregunta_normalizada = self.normalizar_texto(pregunta)
            
            # Evitar duplicados normalizados
            cursor.execute(
                "SELECT COUNT(*) as count FROM conocimiento WHERE LOWER(pregunta) = ?",
                (pregunta_normalizada,)
            )
            if cursor.fetchone()['count'] > 0:
                print("⚠️ Esta pregunta ya existe en la base de datos.")
                return False
            
            cursor.execute(
                "INSERT INTO conocimiento (pregunta, respuesta) VALUES (?, ?)",
                (pregunta, respuesta)
            )
            self.conexion.commit()
            print("✅ Nuevo conocimiento adquirido y guardado.\n")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error al guardar: {e}")
            return False
    
    def procesar_entrada(self, pregunta_usuario: str) -> None:
        """Procesa la entrada del usuario y genera la respuesta."""
        if not pregunta_usuario.strip():
            return
        
        coincidencias = self.buscar_respuesta_fuzzy(pregunta_usuario)
        
        if not coincidencias:
            print("❌ No encontré información sobre eso.\n")
            return
        
        mejor_coincidencia = coincidencias[0]
        similitud = mejor_coincidencia['similitud']
        
        # Caso 1: Similitud > 85% -> Responder automáticamente
        if similitud > self.SIMILARITY_HIGH:
            print(f"\n🤖 Bot: {mejor_coincidencia['respuesta']}\n")
        
        # Caso 2: Similitud 60-85% -> Preguntar confirmación
        elif self.SIMILARITY_MEDIUM <= similitud <= self.SIMILARITY_HIGH:
            pregunta_similar = mejor_coincidencia['pregunta_original']
            print(f"\n❓ ¿Quisiste decir: '{pregunta_similar}'? (s/n): ", end="")
            
            respuesta_usuario = input().lower().strip()
            
            if respuesta_usuario in ['s', 'si', 'yes', 'sí']:
                print(f"\n🤖 Bot: {mejor_coincidencia['respuesta']}\n")
            else:
                # Si dice que no, ofrecemos guardar nuevo conocimiento
                print("\n❌ Entendido. No tengo respuesta para eso.")
                self._adquirir_nuevo_conocimiento(pregunta_usuario)
        
        # Caso 3: Similitud < 60% -> No sabe, adquirir conocimiento
        else:
            print("\n❌ No sé cómo responder a eso.")
            self._adquirir_nuevo_conocimiento(pregunta_usuario)
    
    def _adquirir_nuevo_conocimiento(self, pregunta: str) -> None:
        """Adquiere nuevo conocimiento del usuario."""
        print(f"📚 ¿Qué debería responder a '{pregunta}'?: ", end="")
        respuesta = input().strip()
        
        if respuesta:
            if self.guardar_par_pregunta_respuesta(pregunta, respuesta):
                pass  # El mensaje de éxito ya se imprime en guardar_par_pregunta_respuesta
        else:
            print("⚠️ No se registró la respuesta (vacía).\n")
    
    def listar_conocimiento(self) -> None:
        """Lista todo el conocimiento almacenado."""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM conocimiento")
        count = cursor.fetchone()['count']
        
        if count == 0:
            print("\n📚 No hay conocimiento almacenado aún.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"📚 Base de Conocimiento ({count} entradas)")
        print(f"{'='*60}")
        
        cursor.execute("SELECT id, pregunta, respuesta FROM conocimiento ORDER BY id")
        
        for idx, (id_row, pregunta, respuesta) in enumerate(cursor.fetchall(), 1):
            print(f"\n{idx}. P: {pregunta}")
            print(f"   R: {respuesta}")
        
        print(f"\n{'='*60}\n")
    
    def mostrar_menu(self) -> None:
        """Muestra el menú de ayuda."""
        print("\n" + "="*60)
        print("🤖 CHATBOT - MÓDULO DE ADQUISICIÓN DE CONOCIMIENTO")
        print("="*60)
        print("\nComandos disponibles:")
        print("  • Escribe cualquier pregunta para chatear")
        print("  • ':lista' - Ver toda la base de conocimiento")
        print("  • ':limpiar' - Limpiar pantalla")
        print("  • ':ayuda' - Mostrar este menú")
        print("  • ':salir' - Terminar el programa")
        print("="*60 + "\n")
    
    def limpiar_pantalla(self) -> None:
        """Limpia la pantalla."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def ejecutar(self) -> None:
        """Ejecuta el bucle principal del chatbot."""
        self.limpiar_pantalla()
        self.mostrar_menu()
        
        print("💬 Escribe tu pregunta (o ':ayuda' para ver comandos):\n")
        
        while True:
            try:
                entrada_usuario = input("👤 Tú: ").strip()
                
                if not entrada_usuario:
                    continue
                
                # Procesar comandos especiales
                if entrada_usuario.lower() == ':salir':
                    print("\n👋 ¡Hasta luego!\n")
                    break
                elif entrada_usuario.lower() == ':ayuda':
                    self.mostrar_menu()
                elif entrada_usuario.lower() == ':lista':
                    self.listar_conocimiento()
                elif entrada_usuario.lower() == ':limpiar':
                    self.limpiar_pantalla()
                    print("💬 Escribe tu pregunta:\n")
                else:
                    # Procesar pregunta normal
                    self.procesar_entrada(entrada_usuario)
            
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido. ¡Hasta luego!\n")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}\n")
    
    def cerrar(self) -> None:
        """Cierra la conexión a la BD."""
        if self.conexion:
            self.conexion.close()


def main():
    """Función principal."""
    chatbot = ChatbotKnowledgeModule()
    
    try:
        chatbot.ejecutar()
    finally:
        chatbot.cerrar()


if __name__ == "__main__":
    main()
