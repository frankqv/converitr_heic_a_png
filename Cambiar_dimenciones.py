# Redimensionador de Imágenes al 25% - Versión Mejorada
# Julio 2025 - Versión que funciona en cualquier computadora
# 
# INSTRUCCIONES DE INSTALACIÓN: 
# 1. Asegúrate de tener Python instalado en tu sistema.
# 2. Instala las librerías necesarias ejecutando en la terminal:
#    >>> pip install pillow
# 3. Ejecuta el script:
#    >>> python redimensionar_imagenes.py
# 4. Selecciona la carpeta donde están tus imágenes o usa la carpeta por defecto
# 5. El programa recorrerá todas las subcarpetas y redimensionará todas las imágenes al 25%
# 6. Una vez finalizado, verás un resumen del total de imágenes procesadas

import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def verificar_dependencias():
    """Verifica que las librerías necesarias estén instaladas"""
    try:
        from PIL import Image
        return True
    except ImportError as e:
        print(f"❌ Error: Falta instalar Pillow.")
        print(f"Ejecuta: pip install pillow")
        return False

def obtener_ruta_base():
    """Obtiene la ruta base donde buscar imágenes"""
    # Opción 1: Carpeta por defecto en Descargas
    ruta_por_defecto = os.path.join(os.path.expanduser("~"), "Downloads", "IMAGENES")
    
    print("🔍 Opciones para seleccionar carpeta:")
    print("1. Usar carpeta por defecto (Descargas/IMAGENES)")
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

def obtener_factor_escala():
    """Permite al usuario elegir el factor de escala"""
    print("\n📏 Opciones de redimensionamiento:")
    print("1. 25% del tamaño original (recomendado) ")
    print("2. 50% del tamaño original")
    print("3. 75% del tamaño original")
    print("4. Personalizado")
    print("Recomendado Ejemplo: 3024×4032 A 756×1008 ")
    
    while True:
        opcion = input("\nElige una opción (1-4): ").strip()
        
        if opcion == "1":
            return 0.25
        elif opcion == "2":
            return 0.50
        elif opcion == "3":
            return 0.75
        elif opcion == "4":
            while True:
                try:
                    factor = float(input("Ingresa el factor de escala (ejemplo: 0.25 para 25%): "))
                    if 0.1 <= factor <= 1.0:
                        return factor
                    else:
                        print("❌ El factor debe estar entre 0.1 y 1.0")
                except ValueError:
                    print("❌ Ingresa un número válido")
        else:
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")

def redimensionar_imagenes(ruta_base, factor_escala=0.25):
    """Redimensiona todas las imágenes en la ruta especificada"""
    
    # Extensiones de imagen soportadas
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    # Contadores para estadísticas
    contador_procesadas = 0
    contador_errores = 0
    contador_omitidas = 0
    errores_detallados = []
    
    # Calcular porcentaje para mostrar
    porcentaje = int(factor_escala * 100)
    
    print(f"\n🔄 Iniciando redimensionamiento al {porcentaje}% en: {ruta_base}")
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
            ruta_completa = os.path.join(carpeta_actual, archivo)
            nombre_base, extension = os.path.splitext(archivo)
            salida_redimensionada = os.path.join(carpeta_actual, f"{nombre_base}_{porcentaje}percent{extension}")
            
            # Verificar si ya existe el archivo redimensionado
            if os.path.exists(salida_redimensionada):
                print(f"⚠️  Ya existe: {nombre_base}_{porcentaje}percent{extension} (omitiendo)")
                contador_omitidas += 1
                continue
            
            try:
                # Abrir imagen
                with Image.open(ruta_completa) as img:
                    # Obtener dimensiones originales
                    ancho_original, alto_original = img.size
                    
                    # Calcular nuevas dimensiones
                    nuevo_ancho = int(ancho_original * factor_escala)
                    nuevo_alto = int(alto_original * factor_escala)
                    
                    # Redimensionar la imagen
                    img_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                    
                    # Guardar la imagen redimensionada
                    img_redimensionada.save(salida_redimensionada, optimize=True, quality=95)
                    
                    contador_procesadas += 1
                    print(f"✅ {archivo} → {nombre_base}_{porcentaje}percent{extension}")
                    print(f"   Tamaño: {ancho_original}x{alto_original} → {nuevo_ancho}x{nuevo_alto}")
                    
            except Exception as e:
                contador_errores += 1
                error_msg = f"❌ Error con {archivo}: {str(e)}"
                print(error_msg)
                errores_detallados.append(error_msg)
    
    # Mostrar resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE REDIMENSIONAMIENTO")
    print("=" * 60)
    print(f"✅ Imágenes procesadas exitosamente: {contador_procesadas}")
    print(f"⚠️  Imágenes omitidas (ya existían): {contador_omitidas}")
    print(f"❌ Errores encontrados: {contador_errores}")
    print(f"📁 Carpeta procesada: {ruta_base}")
    print(f"📏 Factor de escala usado: {porcentaje}%")
    
    if errores_detallados:
        print("\n📋 DETALLES DE ERRORES:")
        for error in errores_detallados:
            print(f"   {error}")
    
    if contador_procesadas > 0:
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        
        # Preguntar si eliminar archivos originales
        eliminar = input("\n¿Deseas eliminar las imágenes originales? (s/n): ").strip().lower()
        if eliminar in ['s', 'sí', 'si', 'SI', 'Si', 'Sí', 'yes', 'y']:
            eliminar_imagenes_originales(ruta_base, factor_escala)
    else:
        print("\n🤷 No se encontraron imágenes para procesar.")

def eliminar_imagenes_originales(ruta_base, factor_escala):
    """Elimina todas las imágenes originales después del redimensionamiento"""
    contador_eliminadas = 0
    porcentaje = int(factor_escala * 100)
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    print(f"\n🗑️  Eliminando imágenes originales...")
    
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if os.path.splitext(archivo.lower())[1] in extensiones_validas:
                # Verificar que NO sea una imagen ya redimensionada
                if f"_{porcentaje}percent" not in archivo:
                    ruta_completa = os.path.join(carpeta_actual, archivo)
                    try:
                        os.remove(ruta_completa)
                        contador_eliminadas += 1
                        print(f"🗑️  Eliminado: {archivo}")
                    except Exception as e:
                        print(f"❌ Error al eliminar {archivo}: {e}")
    
    print(f"\n✅ Imágenes originales eliminadas: {contador_eliminadas}")

def main():
    """Función principal"""
    print("🖼️  REDIMENSIONADOR DE IMÁGENES")
    print("=" * 40)
    
    # Verificar dependencias
    if not verificar_dependencias():
        input("\nPresiona Enter para salir...")
        return
    
    try:
        # Obtener ruta base
        ruta_base = obtener_ruta_base()
        
        # Verificar que la ruta existe
        if not os.path.exists(ruta_base):
            print(f"❌ La ruta especificada no existe: {ruta_base}")
            return
        
        # Obtener factor de escala
        factor_escala = obtener_factor_escala()
        
        # Iniciar redimensionamiento
        redimensionar_imagenes(ruta_base, factor_escala)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()