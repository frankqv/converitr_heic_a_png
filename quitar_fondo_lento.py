# Eliminador de Fondos de Imágenes - Versión Automática
# Julio 2025 - Versión que funciona en cualquier computadora
# 
# INSTRUCCIONES DE INSTALACIÓN: 
# 1. Asegúrate de tener Python instalado en tu sistema.
# 2. Instala las librerías necesarias ejecutando en la terminal:
#    >>> pip install rembg pillow
#    >>> pip install onnxruntime
#    >>> pip list | findstr -i "rembg onnxruntime pillow"
#    >>> pip install rembg[gpu] pillow onnxruntime

# Ejecuta powershell como administrador, 
#    >>> pip install --user onnxruntime-gpu
# 3. Ejecuta el script:
#    >>> python quitar_fondo.py
# 4. Selecciona la carpeta donde están tus imágenes o usa la carpeta por defecto
# 5. El programa procesará todas las imágenes y les quitará el fondo
# 6. Una vez finalizado, verás un resumen del total de imágenes procesadas

import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove

def verificar_dependencias():
    """Verifica que las librerías necesarias estén instaladas"""
    try:
        import rembg
        from PIL import Image
        print("✅ Dependencias verificadas correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error: Faltan dependencias.")
        print(f"Ejecuta: pip install rembg pillow")
        print(f"Detalle del error: {e}")
        return False

def obtener_ruta_base():
    """Obtiene la ruta base donde buscar imágenes"""
    # Opción 1: Carpeta por defecto en Descargas
    ruta_por_defecto = os.path.join(os.path.expanduser("~"), "Downloads", "IMAGENES_FONDO")
    
    print("🔍 Opciones para seleccionar carpeta:")
    print("1. Usar carpeta por defecto (Descargas/IMAGENES_FONDO)")
    print("2. Seleccionar carpeta manualmente")
    print("3. Usar carpeta actual")
    print("4. Salir")
    
    while True:
        opcion = input("\nElige una opción (1-4): ").strip()
        
        if opcion == "1":
            if os.path.exists(ruta_por_defecto):
                return ruta_por_defecto
            else:
                print(f"❌ La carpeta por defecto no existe: {ruta_por_defecto}")
                crear = input("¿Deseas crearla? (s/n): ").strip().lower()
                if crear in ['s', 'sí', 'si', 'SI', 'Si', 'Sí', 'yes', 'y']:
                    try:
                        os.makedirs(ruta_por_defecto, exist_ok=True)
                        print(f"✅ Carpeta creada: {ruta_por_defecto}")
                        return ruta_por_defecto
                    except Exception as e:
                        print(f"❌ Error al crear carpeta: {e}")
                        continue
                else:
                    continue
        
        elif opcion == "2":
            try:
                # Crear ventana de diálogo para seleccionar carpeta
                root = tk.Tk()
                root.withdraw()  # Ocultar ventana principal
                
                ruta_seleccionada = filedialog.askdirectory(
                    title="Selecciona la carpeta raíz con imágenes"
                )
                
                root.destroy()
                
                if ruta_seleccionada:
                    return ruta_seleccionada
                else:
                    print("❌ No se seleccionó ninguna carpeta.")
                    continue
            except Exception as e:
                print(f"❌ Error al abrir diálogo: {e}")
                continue
        
        elif opcion == "3":
            return os.getcwd()  # Carpeta actual
        
        elif opcion == "4":
            print("👋 Saliendo...")
            sys.exit()
        
        else:
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")

def seleccionar_modelo():
    """Permite al usuario elegir el modelo de eliminación de fondo"""
    print("\n🤖 Modelos disponibles para eliminar fondo:")
    print("1. u2net - General, bueno para la mayoría de casos")
    print("2. u2net_human_seg - Optimizado para personas")
    print("3. u2net_cloth_seg - Optimizado para ropa")
    print("4. isnet-general-use - Modelo mejorado (más lento pero mejor calidad)")
    print("5. silueta - Para crear siluetas")
    
    modelos = {
        "1": "u2net",
        "2": "u2net_human_seg", 
        "3": "u2net_cloth_seg",
        "4": "isnet-general-use",
        "5": "silueta"
    }
    
    while True:
        opcion = input("\nElige un modelo (1-5, recomendado: 1): ").strip()
        
        if opcion in modelos:
            return modelos[opcion]
        else:
            print("❌ Opción inválida. Elige 1, 2, 3, 4 o 5.")

def quitar_fondo_imagenes(ruta_base, modelo="u2net"):
    """Quita el fondo de todas las imágenes en la ruta especificada"""
    
    # Extensiones de imagen soportadas
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Contadores para estadísticas
    contador_procesadas = 0
    contador_errores = 0
    contador_omitidas = 0
    errores_detallados = []
    
    print(f"\n🔄 Iniciando eliminación de fondos con modelo '{modelo}' en: {ruta_base}")
    print("⏳ Nota: La primera vez puede tardar más porque descarga el modelo...")
    print("=" * 60)
    
    # Recorrer todas las carpetas y subcarpetas
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        
        # Filtrar solo archivos de imagen
        archivos_imagen = [archivo for archivo in archivos 
            if os.path.splitext(archivo.lower())[1] in extensiones_validas]
        
        if archivos_imagen:
            print(f"\n📁 Procesando carpeta: {carpeta_actual}")
            print(f"   Imágenes encontradas: {len(archivos_imagen)}")
        
        for archivo in archivos_imagen:
            # Omitir archivos que ya tienen el fondo removido
            if "_sin_fondo" in archivo:
                continue
                
            ruta_completa = os.path.join(carpeta_actual, archivo)
            nombre_base, extension = os.path.splitext(archivo)
            
            # Siempre guardar como PNG para mantener transparencia
            salida_sin_fondo = os.path.join(carpeta_actual, f"{nombre_base}_sin_fondo.png")
            
            # Verificar si ya existe el archivo sin fondo
            if os.path.exists(salida_sin_fondo):
                print(f"⚠️  Ya existe: {nombre_base}_sin_fondo.png (omitiendo)")
                contador_omitidas += 1
                continue
            
            try:
                print(f"🔄 Procesando: {archivo}...")
                
                # Leer imagen
                with open(ruta_completa, 'rb') as input_file:
                    input_data = input_file.read()
                
                # Quitar fondo usando rembg
                output_data = remove(input_data)
                
                # Guardar imagen sin fondo
                with open(salida_sin_fondo, 'wb') as output_file:
                    output_file.write(output_data)
                
                contador_procesadas += 1
                print(f"✅ {archivo} → {nombre_base}_sin_fondo.png")
                
            except Exception as e:
                contador_errores += 1
                error_msg = f"❌ Error con {archivo}: {str(e)}"
                print(error_msg)
                errores_detallados.append(error_msg)
    
    # Mostrar resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE ELIMINACIÓN DE FONDOS")
    print("=" * 60)
    print(f"✅ Imágenes procesadas exitosamente: {contador_procesadas}")
    print(f"⚠️  Imágenes omitidas (ya existían): {contador_omitidas}")
    print(f"❌ Errores encontrados: {contador_errores}")
    print(f"📁 Carpeta procesada: {ruta_base}")
    print(f"🤖 Modelo usado: {modelo}")
    
    if errores_detallados:
        print("\n📋 DETALLES DE ERRORES:")
        for error in errores_detallados:
            print(f"   {error}")
    
    if contador_procesadas > 0:
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        print(f"💡 Las imágenes sin fondo se guardaron en formato PNG para mantener la transparencia")
        
        # Preguntar si eliminar archivos originales
        eliminar = input("\n¿Deseas eliminar las imágenes originales? (s/n): ").strip().lower()
        if eliminar in ['s', 'sí', 'si', 'SI', 'Si', 'Sí', 'yes', 'y']:
            eliminar_imagenes_originales(ruta_base)
    else:
        print("\n🤷 No se encontraron imágenes para procesar.")

def eliminar_imagenes_originales(ruta_base):
    """Elimina todas las imágenes originales después de quitar el fondo"""
    contador_eliminadas = 0
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    print(f"\n🗑️  Eliminando imágenes originales...")
    
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if os.path.splitext(archivo.lower())[1] in extensiones_validas:
                # Verificar que NO sea una imagen sin fondo
                if "_sin_fondo" not in archivo:
                    ruta_completa = os.path.join(carpeta_actual, archivo)
                    try:
                        os.remove(ruta_completa)
                        contador_eliminadas += 1
                        print(f"🗑️  Eliminado: {archivo}")
                    except Exception as e:
                        print(f"❌ Error al eliminar {archivo}: {e}")
    
    print(f"\n✅ Imágenes originales eliminadas: {contador_eliminadas}")

def crear_imagen_prueba():
    """Crea una imagen de prueba para verificar que funciona"""
    print("\n🧪 ¿Deseas crear una imagen de prueba primero?")
    print("Esto te permitirá ver cómo funciona antes de procesar todas tus imágenes.")
    
    crear = input("¿Crear imagen de prueba? (s/n): ").strip().lower()
    if crear in ['s', 'sí', 'si', 'SI', 'Si', 'Sí', 'yes', 'y']:
        try:
            root = tk.Tk()
            root.withdraw()
            
            archivo_prueba = filedialog.askopenfilename(
                title="Selecciona UNA imagen para prueba",
                filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp")]
            )
            
            root.destroy()
            
            if archivo_prueba:
                print(f"🔄 Procesando imagen de prueba: {os.path.basename(archivo_prueba)}")
                
                with open(archivo_prueba, 'rb') as input_file:
                    input_data = input_file.read()
                
                output_data = remove(input_data)
                
                carpeta_original = os.path.dirname(archivo_prueba)
                nombre_base = os.path.splitext(os.path.basename(archivo_prueba))[0]
                salida_prueba = os.path.join(carpeta_original, f"{nombre_base}_PRUEBA_sin_fondo.png")
                
                with open(salida_prueba, 'wb') as output_file:
                    output_file.write(output_data)
                
                print(f"✅ Imagen de prueba creada: {salida_prueba}")
                print(f"💡 Abre el archivo para ver el resultado antes de continuar")
                
                continuar = input("\n¿Continuar con el procesamiento masivo? (s/n): ").strip().lower()
                return continuar in ['s', 'sí', 'si', 'SI', 'Si', 'Sí', 'yes', 'y']
            else:
                print("❌ No se seleccionó archivo de prueba")
                return True
                
        except Exception as e:
            print(f"❌ Error creando imagen de prueba: {e}")
            return True
    
    return True

def main():
    """Función principal"""
    print("🎨 ELIMINADOR DE FONDOS DE IMÁGENES")
    print("=" * 45)
    
    # Verificar dependencias
    if not verificar_dependencias():
        input("\nPresiona Enter para salir...")
        return
    
    try:
        # Crear imagen de prueba opcional
        if not crear_imagen_prueba():
            print("👋 Proceso cancelado por el usuario.")
            return
        
        # Obtener ruta base
        ruta_base = obtener_ruta_base()
        
        # Verificar que la ruta existe
        if not os.path.exists(ruta_base):
            print(f"❌ La ruta especificada no existe: {ruta_base}")
            return
        
        # Seleccionar modelo
        modelo = seleccionar_modelo()
        
        # Iniciar eliminación de fondos
        quitar_fondo_imagenes(ruta_base, modelo)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()