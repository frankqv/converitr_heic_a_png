# Convertidor HEIC a PNG - Versión Portable
# Julio 2025 - Versión mejorada que funciona en cualquier computadora
#
# INSTRUCCIONES DE INSTALACIÓN:
# 1. Asegúrate de tener Python instalado en tu sistema.
# 2. Instala las librerías necesarias ejecutando en la terminal:
#    >>> pip install pillow pillow-heif
# 3. Ejecuta el script:
#    >>> python convertir_a_png.py
# 4. Selecciona la carpeta donde están tus archivos HEIC o usa la carpeta por defecto
# 5. El programa recorrerá todas las subcarpetas y convertirá todas las imágenes .HEIC a .PNG
# 6. Una vez finalizado, verás un resumen del total de imágenes convertidas
import os
import sys
from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog, messagebox

def verificar_dependencias():
    """Verifica que las librerías necesarias estén instaladas"""
    try:
        import pillow_heif
        from PIL import Image
        return True
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias.")
        print(f"Ejecuta: pip install pillow pillow-heif")
        return False

def obtener_ruta_base():
    """Obtiene la ruta base donde buscar archivos HEIC"""
    # Opción 1: Carpeta por defecto en Descargas
    ruta_por_defecto = os.path.join(os.path.expanduser("~"), "Downloads", "BATERIAS")
    print("🔍 Opciones para seleccionar carpeta:")
    print("1. Seleccionar carpeta manualmente")
    print("2. Usar carpeta por defecto (Descargas/BATERIAS)")
    print("3. Salir")
    while True:
        opcion = input("\nElige una opción (1-3): ").strip()
        if opcion == "1":
            try:
                # Crear ventana de diálogo para seleccionar carpeta
                root = tk.Tk()
                root.withdraw()  # Ocultar ventana principal
                ruta_seleccionada = filedialog.askdirectory(
                    title="Selecciona la carpeta raíz con archivos HEIC"
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
        if opcion == "2":
            if os.path.exists(ruta_por_defecto):
                return ruta_por_defecto
            else:
                print(f"❌ La carpeta por defecto no existe: {ruta_por_defecto}")
                crear = input("¿Deseas crearla? (s/n): ").strip().lower()
                if crear in ["s", "sí", "si", "SI", "Si", "Sí", "yes", "y", "YES", "Yes", "1"]:
                    try:
                        os.makedirs(ruta_por_defecto, exist_ok=True)
                        print(f"✅ Carpeta creada: {ruta_por_defecto}")
                        return ruta_por_defecto
                    except Exception as e:
                        print(f"❌ Error al crear carpeta: {e}")
                        continue
                else:
                    continue
        elif opcion == "3":
            print("👋 Saliendo...")
            sys.exit()
        else:
            print("❌ Opción inválida. Elige 1, 2 o 3.")

def convertir_heic_a_png(ruta_base):
    """Convierte todos los archivos HEIC a PNG en la ruta especificada"""
    # Registrar soporte HEIC
    pillow_heif.register_heif_opener()
    # Contadores para estadísticas
    contador_convertidos = 0
    contador_errores = 0
    errores_detallados = []
    print(f"\n🔄 Iniciando conversión en: {ruta_base}")
    print("=" * 60)
    # Recorrer todas las carpetas y subcarpetas
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        # Filtrar solo archivos HEIC
        archivos_heic = [
            archivo
            for archivo in archivos
            if archivo.lower().endswith((".heic", ".heif"))
        ]
        if archivos_heic:
            print(f"\n📁 Procesando carpeta: {carpeta_actual}")
            print(f"   Archivos HEIC encontrados: {len(archivos_heic)}")
        for archivo in archivos_heic:
            ruta_completa = os.path.join(carpeta_actual, archivo)
            nombre_base = os.path.splitext(archivo)[0]
            salida_png = os.path.join(carpeta_actual, nombre_base + ".png")
            # Verificar si ya existe el archivo PNG
            if os.path.exists(salida_png):
                print(f"⚠️  Ya existe: {nombre_base}.png (omitiendo)")
                continue
            try:
                # Abrir y convertir imagen
                img = Image.open(ruta_completa).convert("RGB")
                img.save(salida_png, "PNG")
                contador_convertidos += 1
                print(f"✅ Convertido: {archivo} → {nombre_base}.png")
            except Exception as e:
                contador_errores += 1
                error_msg = f"❌ Error con {archivo}: {str(e)}"
                print(error_msg)
                errores_detallados.append(error_msg)
    # Mostrar resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CONVERSIÓN")
    print("=" * 60)
    print(f"✅ Imágenes convertidas exitosamente: {contador_convertidos}")
    print(f"❌ Errores encontrados: {contador_errores}")
    print(f"📁 Carpeta procesada: {ruta_base}")
    if errores_detallados:
        print("\n📋 DETALLES DE ERRORES:")
        for error in errores_detallados:
            print(f"   {error}")
    if contador_convertidos > 0:
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        # Preguntar si eliminar archivos HEIC originales
        eliminar = (
            input("\n¿Deseas eliminar los archivos HEIC originales? (s/n): ")
            .strip()
            .lower()
        )
        if eliminar in ["s", "sí", "si", "SI", "Si", "Sí", "yes", "y", "YES", "Yes", "1"]:
            eliminar_archivos_heic(ruta_base)
    else:
        print("\n🤷 No se encontraron archivos HEIC para convertir.")

def eliminar_archivos_heic(ruta_base):
    """Elimina todos los archivos HEIC después de la conversión"""
    contador_eliminados = 0
    print(f"\n🗑️  Eliminando archivos HEIC originales...")
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.lower().endswith((".heic", ".heif")):
                ruta_completa = os.path.join(carpeta_actual, archivo)
                try:
                    os.remove(ruta_completa)
                    contador_eliminados += 1
                    print(f"🗑️  Eliminado: {archivo}")
                except Exception as e:
                    print(f"❌ Error al eliminar {archivo}: {e}")
    print(f"\n✅ Archivos HEIC eliminados: {contador_eliminados}")

def main():
    """Función principal"""
    print("🖼️  CONVERTIDOR HEIC A PNG")
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
        # Iniciar conversión
        convertir_heic_a_png(ruta_base)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        input("\nPresiona Enter para salir...")


if __name__ == "__main__":
    main()
