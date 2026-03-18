# 🎙 Vocally — Transcriptor Offline para Android

Vocally es una aplicación Android desarrollada en Python que permite grabar, transcribir y clasificar automáticamente clases o conferencias. Utiliza un motor de reconocimiento de voz **100% offline** (Vosk) directamente en tu teléfono, garantizando privacidad total sin necesidad de internet.

## ✨ Características

- **Grabación de audio**: Graba audio directamente desde el micrófono del teléfono
- **Transcripción 100% Offline**: Convierte audio a texto localmente en tu dispositivo Android, sin enviar datos a ningún servidor
- **Modelo de IA incluido**: El modelo de reconocimiento de voz en español (~40MB) viene integrado en la app
- **Interfaz táctil**: Interfaz diseñada para pantallas móviles con Kivy
- **Sin internet requerido**: Una vez instalada, funciona completamente sin conexión

## 📋 Requisitos para Compilar

| Requisito | Detalles |
|---|---|
| **Sistema operativo** | Ubuntu / Debian / Linux Mint (o WSL2 en Windows) |
| **Python** | 3.8 – 3.12 (Buildozer NO soporta 3.13+) |
| **Espacio en disco** | Mínimo **10 GB** libres (Android SDK/NDK son grandes) |
| **Internet** | Solo durante la compilación para descargar herramientas |
| **Teléfono Android** | Android 5.0+ (API 21+) |

## 🚀 Tutorial Completo: De Código a APK

### Paso 1 — Instalar dependencias del sistema

Abrí una terminal y ejecutá:

```bash
sudo apt update
sudo apt install -y \
  git \
  zip \
  unzip \
  openjdk-17-jdk \
  python3-pip \
  python3-venv \
  autoconf \
  libtool \
  pkg-config \
  zlib1g-dev \
  libncurses5-dev \
  libncursesw5-dev \
  cmake \
  libffi-dev \
  libssl-dev \
  lld
```

> **¿Por qué?** Buildozer necesita Java (JDK 17), un compilador C y varias bibliotecas del sistema para compilar Python y librerías nativas (como Vosk) para la arquitectura ARM de Android.

---

### Paso 2 — Instalar Buildozer y Cython

```bash
pip install --user --upgrade buildozer cython virtualenv
```

Asegurate de que `~/.local/bin` esté en tu PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verificá que funcione:

```bash
buildozer --version
```

Deberías ver algo como `Buildozer 1.5.0` o superior.

---

### Paso 3 — Ir a la carpeta del proyecto Android

```bash
cd vocally_android
```

---

### Paso 4 — Verificar que el modelo Vosk esté presente

El modelo de reconocimiento de voz offline ya debería estar descargado. Verificalo:

```bash
ls model/
```

Deberías ver carpetas como `am/`, `conf/`, `graph/`, `ivector/`.

**Si la carpeta `model/` está vacía o no existe**, descargalo manualmente:

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
mv vosk-model-small-es-0.42 model
rm vosk-model-small-es-0.42.zip
```

---

### Paso 5 — Compilar el APK

Este es el paso principal. Ejecutá:

```bash
buildozer android debug
```

> ⏳ **La primera compilación tarda 15–30 minutos** porque descarga:
> - Android SDK (~500MB)
> - Android NDK (~1.5GB)
> - Cadena de herramientas Python-for-Android
> - Todas las dependencias de Python compiladas para ARM
>
> **Las compilaciones siguientes son MUCHO más rápidas (1–3 minutos).**

Si la compilación es exitosa, verás un mensaje como:

```
# APK build successful!
# APK located at: bin/vocally-1.0-arm64-v8a-debug.apk
```

---

### Paso 6 — Transferir el APK a tu teléfono

El archivo `.apk` generado está dentro de la carpeta `bin/`:

```bash
ls bin/*.apk
```

**Opción A — Cable USB con ADB:**

```bash
adb install bin/vocally-1.0-arm64-v8a-debug.apk
```

**Opción B — Transferencia de archivos:**
1. Copiá el archivo `.apk` a tu teléfono por cable USB, Google Drive, WhatsApp, email o cualquier app para compartir archivos.
2. En tu teléfono, abrí el archivo y tocá "Instalar".
3. Si te lo pide, andá a **Ajustes → Seguridad → Instalar apps de fuentes desconocidas** y permitilo.

---

### Paso 7 — Otorgar permisos en tu teléfono

Cuando abras la app por primera vez:
1. **Permitir acceso al micrófono** — Necesario para grabar audio.
2. **Permitir acceso a archivos** — Necesario para guardar el audio temporalmente.

¡Después de eso, la app funciona **100% offline** para siempre!

---

## 📱 Cómo Usar la App

1. Abrí **Vocally** en tu teléfono Android.
2. Tocá el botón verde **"🎙 Start Recording"**.
3. Hablá por el micrófono del teléfono.
4. Tocá **"⏹ Stop & Transcribe"** cuando termines.
5. Esperá unos segundos — tu voz se transcribirá a texto directamente en el dispositivo.
6. El texto transcrito aparece en el área de texto.

---

## 📁 Estructura del Proyecto

```
vocally_android/
├── main.py              # Interfaz Kivy — punto de entrada de la app
├── audio_recorder.py    # Acceso al micrófono Android via pyjnius
├── transcriber.py       # Motor de transcripción offline Vosk
├── buildozer.spec       # Configuración de compilación para el APK
├── model/               # Modelo Vosk de español pre-descargado (~40MB)
│   ├── am/
│   ├── conf/
│   ├── graph/
│   └── ivector/
├── bin/                 # (Generado) Contiene el .apk compilado
└── README.md            # Este archivo
```

---

## 🔧 Solución de Problemas

### La compilación falla con errores de Java
Asegurate de tener JDK 17:
```bash
java -version
# Debería mostrar: openjdk version "17.x.x"
```

### La app crashea al abrir
Conectá tu teléfono por USB y revisá los logs:
```bash
adb logcat | grep python
```

### El audio no se transcribe correctamente
El `MediaRecorder` de Android exporta AAC/MP4 por defecto. Vosk requiere WAV (PCM 16-bit, 16kHz, mono). Si la transcripción falla, puede ser necesario agregar conversión de formato en `audio_recorder.py`.

### Error: "pip no se reconoce"
Usá `python3 -m pip` en lugar de `pip`.

---

## 🔄 Recompilar Después de Cambios

Después de modificar cualquier archivo `.py`, simplemente ejecutá:

```bash
buildozer android debug
```

Para una recompilación limpia completa:

```bash
buildozer android clean
buildozer android debug
```

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**🎉 ¡Disfrutá usando Vocally offline en tu Android!**
