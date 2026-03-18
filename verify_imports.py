import sys
from pathlib import Path
import os

# Add root to path
ROOT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(ROOT_DIR))

print(f"Checking imports from {ROOT_DIR}...")

try:
    print("Importing config...")
    import customtkinter
    
    print("Importing components...")
    from frontend.components.boton_grabacion import BotonGrabacion
    from frontend.components.cronometro import Cronometro
    
    print("Importing backend modules...")
    from backend.processing import library_viewer
    from backend.processing.lector_texto import get_tts_reader
    from backend.processing.diccionarios import DICCIONARIOS_MATERIA
    from backend.processing.clasificador import CLASIFICADOR_MATERIAS
    from backend.processing.grabacion_audio import grabar_audio
    
    print("Importing UI...")
    # This might fail if it tries to init TKinter but we just want to check ImportError
    try:
        from frontend.ui_vocally import VocallyApp
    except Exception as e:
        # Ignore TclError/RuntimeError if no display, but catch ImportErrors
        if "Import" in str(e) or "Module" in str(e):
            raise e
        print(f"UI import triggered non-import error (expected in headless): {e}")

    print("✅ All imports successful!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    sys.exit(1)
