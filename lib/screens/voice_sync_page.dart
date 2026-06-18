import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../services/voice_sync_service.dart';

class VoiceSyncPage extends StatefulWidget {
  const VoiceSyncPage({super.key});

  @override
  State<VoiceSyncPage> createState() => _VoiceSyncPageState();
}

class _VoiceSyncPageState extends State<VoiceSyncPage> {
  final _service = VoiceSyncService();
  String? _selectedVideo;
  String? _selectedAudio;
  double _pitch = 0;
  double _speed = 1.0;
  String _status = 'Listo';
  double _progress = 0;

  Future<void> _pickFile(String type) async {
    final allowedExtensions = type == 'video'
        ? ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv']
        : ['mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a'];
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: allowedExtensions,
    );
    if (result != null && result.paths.isNotEmpty && result.paths[0] != null) {
      setState(() {
        if (type == 'video') {
          _selectedVideo = result.paths[0];
        } else {
          _selectedAudio = result.paths[0];
        }
        _status = '${type == 'video' ? "Video" : "Audio"} seleccionado';
      });
    }
  }

  Future<void> _syncAudio() async {
    if (_selectedVideo == null || _selectedAudio == null) {
      setState(() => _status = 'Selecciona video y audio primero');
      return;
    }
    setState(() { _status = 'Sincronizando audio...'; _progress = 0.2; });

    final output = await _service.syncAudioToVideo(
      videoPath: _selectedVideo!,
      audioPath: _selectedAudio!,
    );
    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Sincronizado: $output');
      if (mounted) _showSuccess('Video sincronizado:\n$output');
    } else {
      setState(() { _status = 'Error en sincronización'; _progress = 0; });
    }
  }

  Future<void> _extractAudio() async {
    if (_selectedVideo == null) {
      setState(() => _status = 'Selecciona un video primero');
      return;
    }
    setState(() { _status = 'Extrayendo audio...'; _progress = 0.3; });

    final output = await _service.extractAudioFromVideo(_selectedVideo!);
    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Audio extraído: $output');
      if (mounted) _showSuccess('Audio extraído:\n$output');
    } else {
      setState(() { _status = 'Error extrayendo audio'; _progress = 0; });
    }
  }

  Future<void> _adjustPitch() async {
    if (_selectedAudio == null) {
      setState(() => _status = 'Selecciona un audio primero');
      return;
    }
    setState(() { _status = 'Ajustando tono...'; _progress = 0.3; });
    final output = await _service.adjustVoicePitch(_selectedAudio!, semitones: _pitch.round());
    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Tono ajustado: $output');
      if (mounted) _showSuccess('Audio con tono ajustado:\n$output');
    } else {
      setState(() { _status = 'Error ajustando tono'; _progress = 0; });
    }
  }

  Future<void> _changeSpeed() async {
    if (_selectedAudio == null) {
      setState(() => _status = 'Selecciona un audio primero');
      return;
    }
    setState(() { _status = 'Cambiando velocidad...'; _progress = 0.3; });
    final output = await _service.changeVoiceSpeed(_selectedAudio!, speed: _speed);
    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Velocidad cambiada: $output');
      if (mounted) _showSuccess('Audio con velocidad cambiada:\n$output');
    } else {
      setState(() { _status = 'Error cambiando velocidad'; _progress = 0; });
    }
  }

  void _showSuccess(String msg) {
    showDialog(context: context, builder: (c) => AlertDialog(
      title: const Text('Éxito'),
      content: Text(msg),
      actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Cerrar'))],
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sincronizar Voz')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ListTile(title: Text('Video: ${_selectedVideo != null ? _selectedVideo!.split('/').last : 'Ninguno'}'),
              trailing: ElevatedButton(onPressed: () => _pickFile('video'), child: const Text('Buscar'))),
            ListTile(title: Text('Audio: ${_selectedAudio != null ? _selectedAudio!.split('/').last : 'Ninguno'}'),
              trailing: ElevatedButton(onPressed: () => _pickFile('audio'), child: const Text('Buscar'))),
            const Divider(),
            Row(children: [
              const Text('Tono:'),
              Expanded(child: Slider(value: _pitch, min: -12, max: 12, divisions: 24, label: '${_pitch.round()}', onChanged: (v) => setState(() => _pitch = v))),
              Text('${_pitch.round()}'),
            ]),
            Row(children: [
              const Text('Velocidad:'),
              Expanded(child: Slider(value: _speed, min: 0.5, max: 2.0, divisions: 15, label: '${_speed.toStringAsFixed(1)}x', onChanged: (v) => setState(() => _speed = v))),
              Text('${_speed.toStringAsFixed(1)}x'),
            ]),
            const SizedBox(height: 16),
            Wrap(spacing: 8, children: [
              ElevatedButton(onPressed: _syncAudio, child: const Text('Sincronizar Audio con Video')),
              ElevatedButton(onPressed: _extractAudio, child: const Text('Extraer Audio del Video')),
              ElevatedButton(onPressed: _adjustPitch, child: const Text('Ajustar Tono')),
              ElevatedButton(onPressed: _changeSpeed, child: const Text('Cambiar Velocidad')),
            ]),
            const SizedBox(height: 16),
            LinearProgressIndicator(value: _progress),
            Text(_status),
          ],
        ),
      ),
    );
  }
}
