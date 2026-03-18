import os
import subprocess
import shutil
import sys

def build():
    print("Iniciando compilacion de Vocally para Windows...")
    
    # Asegurarse de que las carpetas de salida esten limpias
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(f"Advertencia: No se pudo limpiar {folder}: {e}")
                print("Asegurate de que Vocally.exe no este abierto.")

    # Identificar la ruta de customtkinter para incluir sus assets
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)
    
    # Comando de PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name=Vocally',
        # Incluir JSON de diccionarios
        f'--add-data=backend/processing/diccionarios.py;backend/processing',
        # Incluir assets de customtkinter
        f'--add-data={ctk_path};customtkinter',
        # Script principal
        'vocally.py'
    ]

    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Compilacion exitosa! El archivo esta en la carpeta 'dist/Vocally.exe'")
    else:
        print("Error en la compilacion:")
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    try:
        import pyinstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    build()
