import 'package:flutter/material.dart';
import '../services/ffmpeg_helper.dart';
import '../services/file_manager.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final _ffmpeg = FFmpegHelper();
  FileManager? _fileManager;
  String _status = 'Listo';

  @override
  void initState() {
    super.initState();
    FileManager.create().then((fm) {
      if (mounted) setState(() => _fileManager = fm);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Configuración')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Información del Sistema', style: Theme.of(context).textTheme.titleMedium),
          ListTile(title: Text('FFmpeg: ${_ffmpeg.isAvailable() ? "Disponible" : "No instalado"}')),
          const ListTile(title: Text('Plataforma: Android')),
          const Divider(),
          Text('Almacenamiento', style: Theme.of(context).textTheme.titleMedium),
          ListTile(
            title: Text('Espacio usado: ${_fileManager?.getStorageInfo() ?? "Calculando..."}'),
          ),
          const Divider(),
          Text('Acciones', style: Theme.of(context).textTheme.titleMedium),
          ListTile(
            leading: const Icon(Icons.cleaning_services),
            title: const Text('Limpiar Archivos Temporales'),
            onTap: () {
              _fileManager?.clearTemp();
              setState(() => _status = 'Archivos temporales limpiados');
            },
          ),
          const Divider(),
          Text('Acerca de', style: Theme.of(context).textTheme.titleMedium),
          const ListTile(title: Text('VideoGenApp v1.0.0')),
          const ListTile(title: Text('Hecho con Flutter + Dart')),
          ListTile(title: Text('© 2026 VideoGenApp', style: TextStyle(color: Colors.grey[600]))),
          const SizedBox(height: 16),
          Text(_status, style: TextStyle(color: Colors.grey[600])),
        ],
      ),
    );
  }
}
