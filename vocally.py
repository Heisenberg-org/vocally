 #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vocally - Transcriptor inteligente de clases
Aplicación para grabar, transcribir y clasificar clases automáticamente.
"""

import sys
import os
from pathlib import Path
import customtkinter as ctk
import time

# Agregar el directorio raíz al path para importaciones
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def verificar_dependencias():
    """Verifica que las dependencias principales estén instaladas."""
    dependencias_faltantes = []
    
    try:
        import customtkinter
    except ImportError:
        dependencias_faltantes.append("customtkinter")
    
    try:
        import numpy
    except ImportError:
        dependencias_faltantes.append("numpy")
    
    try:
        import sounddevice
    except ImportError:
        dependencias_faltantes.append("sounddevice")
    
    try:
        import vosk
    except ImportError:
        dependencias_faltantes.append("vosk")
    
    if dependencias_faltantes:
        print("ERROR: Faltan las siguientes dependencias:")
        for dep in dependencias_faltantes:
            print(f"   - {dep}")
        print("\nPara instalarlas, ejecuta:")
        print("   python -m pip install -r requirements.txt")
        return False
    
    return True

def inicializar_nltk():
    """Inicializa los recursos de NLTK si están disponibles de forma segura."""
    try:
        import nltk
        resources = ['tokenizers/punkt', 'corpora/stopwords']
        for res in resources:
            try:
                # Usar quiet=True y un timeout implícito (NLTK no tiene timeout directo pero podemos capturar excepciones)
                nltk.data.find(res)
            except (LookupError, Exception):
                res_name = res.split('/')[-1]
                print(f"Descargando recurso de NLTK: {res_name}...")
                nltk.download(res_name, quiet=True)
    except ImportError:
        print("Advertencia: NLTK no está instalado. El clasificador tendrá menor precisión.")
    except Exception as e:
        print(f"Advertencia: Error al inicializar NLTK: {e}")
        print("   La aplicación continuará sin recursos adicionales de NLTK.")

def main():
    """Función principal de la aplicación."""
    # Configurar codificación UTF-8 para Windows
    if sys.platform == 'win32':
        import io
        if sys.stdout is not None:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if sys.stderr is not None:
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    print("Iniciando Vocally...")
    
    # Verificar dependencias críticas
    if not verificar_dependencias():
        sys.exit(1)
    
    # Inicializar NLTK (opcional)
    inicializar_nltk()
    
    # Splash y arranque de UI
    try:
        def splash_screen(callback):
            splash = ctk.CTk()
            width = 500
            height = 400
            screen_width = splash.winfo_screenwidth()
            screen_height = splash.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            splash.geometry(f"{width}x{height}+{x}+{y}")
            splash.overrideredirect(True)

            frame = ctk.CTkFrame(splash, fg_color="#111111")
            frame.pack(fill="both", expand=True)

            fallback_label = ctk.CTkLabel(
                frame,
                text="VOCALLY",
                font=ctk.CTkFont(size=40, weight="bold")
            )
            logo_label = None
            if (ROOT_DIR / "backend/assets/vocally_logo_verde.png").exists():
                try:
                    from PIL import Image
                    img = Image.open(ROOT_DIR / "backend/assets/vocally_logo_verde.png")
                    logo = ctk.CTkImage(img, size=(320, 105))
                    logo_label = ctk.CTkLabel(frame, text="", image=logo)
                except Exception:
                    pass
            
            # Mostrar logo centrado inmediato
            label_to_use = logo_label if logo_label else fallback_label
            label_to_use.place(relx=0.5, rely=0.5, anchor="center")
            splash.attributes("-alpha", 1.0)
            
            # Fade-out usando .after para no bloquear
            fade_steps = 90
            fade_duration = 2.5 # Un poco más rápido
            delay_ms = int((fade_duration * 1000) / fade_steps)

            def fade_step(step):
                if step <= fade_steps:
                    alpha = 1 - (step / fade_steps)
                    splash.attributes("-alpha", alpha)
                    splash.after(delay_ms, lambda: fade_step(step + 1))
                else:
                    splash.destroy()
                    callback()

            # Iniciar el fade-out después de un breve momento de visibilidad total
            splash.after(1000, lambda: fade_step(0))
            splash.mainloop()

        from frontend.ui_vocally import run_app
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        print("Aplicacion iniciada correctamente")
        splash_screen(run_app)
    except ImportError as e:
        print(f"ERROR: Error al importar modulos: {e}")
        print("Asegurate de estar en el directorio raiz del proyecto")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()