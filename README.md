# VideoGenApp

Aplicación Android para generar videos con sincronización de voces, desarrollada con **Kivy** y compilada con **Buildozer**.

## Características

- 📹 Generación de videos
- 🎙️ Sincronización de voces
- 🎨 Interfaz gráfica con Kivy
- 🔊 Síntesis de texto a voz (TTS)
- 🎤 Reconocimiento de voz
- 📱 Optimizado para Android (API 24+)

## Estructura del Proyecto

```
VideoGenApp/
├── main.py                    # Punto de entrada de la aplicación
├── VideoGenApp.kv            # Interfaz gráfica (Kivy Language)
├── buildozer.spec            # Configuración de compilación para Android
├── requirements.txt          # Dependencias de Python
├── screens/                  # Módulos de pantallas (UI)
│   ├── main_screen.py
│   ├── video_screen.py
│   ├── tts_screen.py
│   ├── presentation_screen.py
│   ├── voice_sync_screen.py
│   └── settings_screen.py
├── modules/                  # Lógica de negocio
├── utils/                    # Utilidades y funciones auxiliares
└── .github/workflows/        # CI/CD con GitHub Actions
```

## Requisitos

### Para desarrollo local:
- Python 3.9+
- Kivy 2.1.0+
- pip

### Para compilar APK:
- Buildozer
- Java Development Kit (JDK)
- Android SDK/NDK (se descarga automáticamente)

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/carlosjuliogallego79-spec/VideoGenApp.git
cd VideoGenApp
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar en desarrollo
```bash
python main.py
```

## Compilación para Android

### Opción 1: Con GitHub Actions (Recomendado)
El proyecto incluye un workflow automático que compila y genera el APK al hacer push a `main`.

**Pasos:**
1. Haz push a la rama `main`
2. Ve a la sección "Actions" del repositorio
3. El workflow "Build Android APK" se ejecutará automáticamente
4. Descarga el APK desde los artifacts una vez completado

### Opción 2: Compilación Local
```bash
# Instalar buildozer
pip install buildozer

# Compilar APK
buildozer android debug

# El APK estará en: bin/videogenapp-1.0.0-debug.apk
```

## Configuración

### buildozer.spec
Archivo de configuración principal para la compilación:
- **Versión:** 1.0.0
- **API Level:** 33 (API mínima: 24)
- **Arquitectura:** arm64-v8a (optimizada para dispositivos modernos)
- **Permisos:** INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, etc.

### main.py
Puntos de entrada:
- **Desktop:** Ejecuta la UI de Kivy
- **Android:** Solicita permisos necesarios (almacenamiento, audio)

## Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|----------|
| kivy | ≥2.1.0 | Framework de UI |
| kivymd | ≥1.1.1 | Componentes Material Design |
| Pillow | ≥9.0.0 | Procesamiento de imágenes |
| pyttsx3 | ≥2.90 | Síntesis de voz |
| SpeechRecognition | ≥3.8.1 | Reconocimiento de voz |
| requests | ≥2.28.0 | Peticiones HTTP |

## Desarrollo

### Agregar una nueva pantalla

1. Crea un archivo en `screens/` (ej: `new_screen.py`)
2. Hereda de `Screen` de Kivy
3. Agrega el widget en `main.py`

### Agregar un módulo

1. Crea un archivo en `modules/` con tu lógica
2. Importa en las pantallas que lo necesiten

## CI/CD con GitHub Actions

El archivo `.github/workflows/build.yml` automatiza:
- ✅ Compilación de APK en cada push
- ✅ Carga de artifacts para descarga
- ✅ Caching de dependencias para builds más rápidos

## Troubleshooting

### Error: "sdkmanager path does not exist"
- El workflow usa Docker container con todo pre-instalado
- Asegúrate de hacer push a `main` para triggear el build

### APK no se genera
- Verifica que `buildozer.spec` esté correctamente configurado
- Revisa los logs del workflow en GitHub Actions

### Problemas de permisos
- En `main.py` se solicitan permisos automáticamente en Android
- En settings.gradle puedes ajustar los permisos según necesites

## Versiones

**v1.0.0** - Versión inicial con:
- UI completa con 6 pantallas principales
- Sincronización de video y voz
- Síntesis de texto a voz
- Reconocimiento de voz
- Soporte para Android 7.0+

## Autor

**carlosjuliogallego79**

## Licencia

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

## Recursos

- [Documentación de Kivy](https://kivy.org/doc/stable/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [Buildozer](https://buildozer.readthedocs.io/)
- [Python-for-Android](https://python-for-android.readthedocs.io/)

---

**Última actualización:** 2026-06-17
**Estado:** ✅ Completado - v1.0.0
