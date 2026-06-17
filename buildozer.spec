[app]

# Nombre de la aplicación
title = VideoGenApp

# Nombre del paquete
package.name = videogenapp

# Nombre de dominio del paquete (invertido)
package.domain = org.videogenapp

# Versión
version = 1.0.0

# Código de versión para Google Play
version.code = 1

# Archivo principal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# Requisitos para python-for-android (ffmpeg removido para velocidad)
requirements = python3,kivy,Pillow,requests,android

# Permisos de Android
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO

# API level de Android
android.api = 33
android.minapi = 24
android.sdk = 33

# NDK version (recomendado por p4a)
android.ndk = 28c

# Bootstrap (sdl2 es el predeterminado para Kivy)
p4a.bootstrap = sdl2

# Aceptar licencia de Android SDK automáticamente
android.accept_sdk_license = True

# Preset de compilación
android.presplash_color = #1a1a2e

# Icono de la aplicación (opcional)
# android.icon = assets/icons/icon.png

# Orientación
android.orientation = portrait

# Si la app debe ser fullscreen
android.fullscreen = 0

# Argumentos para python-for-android
android.add_src =

# Bibliotecas nativas adicionales
android.libraries_repository =

# Recursos adicionales para copiar
android.extra_files =

# Ganchos pre/post build
# android.gradle_dependencies =

# Meta-datos
osx.codesign =

# Configuración de compilación (optimizada)
log_level = 1
debug = 0
archs = arm64-v8a

# Almacenamiento local en Android
android.copy_libs = 1
android.wakelock = 1

# Habilitar almacenamiento externo
android.storage_path = /sdcard/VideoGenApp
