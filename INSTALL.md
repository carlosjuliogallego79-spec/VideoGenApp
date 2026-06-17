# 📱 Guía de Instalación - VideoGenApp

## Paso 1: Descargar el APK

### Opción A: Desde GitHub Actions (Recomendado)
1. Ve a: https://github.com/carlosjuliogallego79-spec/VideoGenApp/actions
2. Haz clic en el workflow más reciente "Build Android APK"
3. Descarga el archivo `VideoGenApp-APK.zip` desde la sección "Artifacts"
4. Extrae el archivo para obtener `videogenapp-*.apk`

### Opción B: Compilar localmente
```bash
git clone https://github.com/carlosjuliogallego79-spec/VideoGenApp.git
cd VideoGenApp
pip install buildozer
buildozer android debug
# El APK estará en: bin/videogenapp-*.apk
```

## Paso 2: Transferir APK a Android

### Por USB
```bash
# Conecta tu dispositivo Android
adb push bin/videogenapp-*.apk /sdcard/Download/
```

### Por Email/Descarga
1. Descarga el APK en tu dispositivo Android
2. El archivo estará en `Descargas/` o `Downloads/`

## Paso 3: Instalar en Android

### Método 1: Desde Archivos (Recomendado)
1. Abre la app **Archivos** en tu Android
2. Navega a `Descargas/` o `Downloads/`
3. Toca el archivo `videogenapp-*.apk`
4. Si aparece un popup: **Instalar de todas formas** (o similar)
5. Espera a que termine la instalación
6. Toca **Abrir** para ejecutar la app

### Método 2: Desde Settings
1. Ve a **Configuración → Seguridad**
2. Activa **"Orígenes desconocidos"** (permitir instalación desde APK)
3. Abre Archivos y toca el APK
4. Sigue los pasos anteriores

### Método 3: Por ADB
```bash
adb install bin/videogenapp-*.apk
```

## Paso 4: Dar Permisos (Primera Ejecución)

Al abrir VideoGenApp por primera vez, pedirá:
- ✅ **Almacenamiento** (lectura/escritura)
- ✅ **Micrófono** (para reconocimiento de voz)
- ✅ **Cámara** (si se requiere)

**Acepta todos los permisos** para que funcione correctamente.

## Requisitos del Dispositivo

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **Android** | 7.0 (API 24) | 10.0+ (API 29+) |
| **RAM** | 2 GB | 4 GB+ |
| **Almacenamiento** | 100 MB libres | 500 MB+ |
| **Procesador** | ARM 64-bit | Snapdragon 600+ |
| **Internet** | Recomendado | Recomendado |

## Solución de Problemas

### ❌ "No se puede instalar desde origen desconocido"
**Solución:**
1. Ve a **Configuración → Aplicaciones → Administrador de aplicaciones**
2. Busca la app donde descargaste (Chrome, Navegador, etc.)
3. Toca el menú ⋮ y activa **"Instalar aplicaciones desconocidas"**
4. Intenta instalar nuevamente

### ❌ "Error de análisis"
**Solución:**
- Descarga nuevamente el APK (puede estar corrupto)
- Verifica que sea el archivo correcto: `videogenapp-*.apk`

### ❌ "Permisos no concedidos"
**Solución:**
1. Desinstala la app
2. Ve a **Configuración → Privacidad → Permisos de aplicaciones**
3. Reinicia el dispositivo
4. Reinstala la app

### ❌ "La app se cierra al abrir"
**Solución:**
- Actualiza a la última versión de Android
- Libera espacio en almacenamiento (mín. 100 MB)
- Borra caché: **Configuración → Aplicaciones → VideoGenApp → Almacenamiento → Borrar caché**

### ❌ "No se escucha el micrófono"
**Solución:**
1. Abre **Configuración → Privacidad → Permisos**
2. Ve a **Micrófono**
3. Verifica que VideoGenApp tenga permiso activado
4. Reinicia la app

## Actualizar la App

Cuando salga una nueva versión:
1. Descarga el nuevo APK
2. Instálalo igual que la primera vez
3. Automáticamente sobrescribe la versión anterior

## Desinstalar

1. Abre **Configuración → Aplicaciones**
2. Busca "VideoGenApp"
3. Toca **Desinstalar**
4. Confirma

## Primeros Pasos en la App

1. **Pantalla Principal**: Lee el tutorial
2. **Generador de Video**: Crea tu primer video
3. **TTS**: Prueba la síntesis de voz
4. **Voice Sync**: Sincroniza video con audio
5. **Settings**: Personaliza la experiencia

## Reportar Problemas

Si encuentras bugs:
1. Ve a: https://github.com/carlosjuliogallego79-spec/VideoGenApp/issues
2. Haz clic en **New Issue**
3. Describe el problema y adjunta screenshots

---

**¡Listo! Tu VideoGenApp está instalada y lista para usar.** 🎉
