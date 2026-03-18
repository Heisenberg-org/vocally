import sounddevice as sd
import numpy as np
import time
import speech_recognition as sr
import os

def check_devices():
    print("Listando dispositivos de audio disponibles:")
    print(sd.query_devices())
    
    try:
        default_input = sd.default.device[0]
        print(f"\nDispositivo de entrada por defecto: {default_input}")
        
        device_info = sd.query_devices(default_input, 'input')
        print(f"   Nombre: {device_info['name']}")
        print(f"   Canales: {device_info['max_input_channels']}")
        print(f"   Sample Rate por defecto: {device_info['default_samplerate']}")
    except Exception as e:
        print(f"Error al obtener dispositivo por defecto: {e}")

def test_recording(duration=3):
    print(f"\nProbando grabacion por {duration} segundos...")
    print("   Hable fuerte y claro ahora...")
    
    try:
        recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        
        max_amp = np.max(np.abs(recording))
        mean_amp = np.mean(np.abs(recording))
        
        print(f"Grabacion finalizada.")
        print(f"Estadisticas de audio:")
        print(f"   Amplitud Maxima: {max_amp:.6f}")
        print(f"   Amplitud Promedio: {mean_amp:.6f}")
        
        if max_amp < 0.01:
            print("ADVERTENCIA: La senal es MUY BAJA. Posiblemente silencio (microfono incorrecto o muteado).")
        else:
            print("Se detecto senal de audio.")
            
        # Intentar transcripción rápida si hay señal
        if max_amp > 0.01:
            import soundfile as sf
            wav_path = "test_audio.wav"
            sf.write(wav_path, recording, 16000)
            print(f"\nIntentando transcribir {wav_path} con Google...")
            
            r = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio = r.record(source)
                try:
                    text = r.recognize_google(audio, language="es-ES")
                    print(f"Transcripcion exitosa: '{text}'")
                except sr.UnknownValueError:
                    print("Google no entendio el audio (UnknownValueError)")
                except sr.RequestError as e:
                    print(f"Error de conexion con Google: {e}")
            
            # Limpiar
            try:
                os.remove(wav_path)
            except:
                pass
                
    except Exception as e:
        print(f"Error al grabar: {e}")

if __name__ == "__main__":
    check_devices()
    test_recording()
