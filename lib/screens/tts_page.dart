import 'package:flutter/material.dart';
import '../services/tts_service.dart';
import '../models/voice.dart';

class TTSPage extends StatefulWidget {
  const TTSPage({super.key});

  @override
  State<TTSPage> createState() => _TTSPageState();
}

class _TTSPageState extends State<TTSPage> {
  final _ttsService = TTSService();
  final _textController = TextEditingController(
    text: 'Hola, bienvenido a VideoGenApp. Esta es una prueba de texto a voz.',
  );
  Voice _selectedVoice = Voice.availableVoices[0];
  double _speed = 1.0;
  double _pitch = 1.0;
  String _status = 'Listo';
  double _progress = 0;

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  Future<void> _generate({bool preview = false}) async {
    if (_textController.text.trim().isEmpty) {
      setState(() => _status = 'Escribe algún texto primero');
      return;
    }
    setState(() { _status = 'Generando audio...'; _progress = preview ? 0.3 : 0.2; });

    final output = await _ttsService.textToSpeech(
      text: _textController.text.trim(),
      outputName: preview ? 'preview.mp3' : 'tts_output.mp3',
      voice: _selectedVoice.lang,
      speed: _speed,
      pitch: _pitch,
    );

    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = preview ? 'Vista previa lista' : 'Audio generado');
      if (mounted) _showSuccess('Audio guardado en:\n$output');
    } else {
      setState(() { _status = 'Error generando audio'; _progress = 0; });
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
      appBar: AppBar(title: const Text('Texto a Voz')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _textController,
              decoration: const InputDecoration(labelText: 'Texto a convertir'),
              maxLines: 4,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<Voice>(
              initialValue: _selectedVoice,
              decoration: const InputDecoration(labelText: 'Voz'),
              items: Voice.availableVoices.map((v) => DropdownMenuItem(value: v, child: Text(v.name))).toList(),
              onChanged: (v) => setState(() => _selectedVoice = v!),
            ),
            Row(children: [
              const Text('Velocidad:'),
              Expanded(child: Slider(value: _speed, min: 0.5, max: 2.0, divisions: 15, label: '${_speed.toStringAsFixed(1)}x', onChanged: (v) => setState(() => _speed = v))),
              Text('${_speed.toStringAsFixed(1)}x'),
            ]),
            Row(children: [
              const Text('Tono:'),
              Expanded(child: Slider(value: _pitch, min: 0.5, max: 2.0, divisions: 15, label: '${_pitch.toStringAsFixed(1)}x', onChanged: (v) => setState(() => _pitch = v))),
              Text('${_pitch.toStringAsFixed(1)}x'),
            ]),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(child: ElevatedButton(onPressed: () => _generate(preview: true), child: const Text('Vista Previa'))),
              const SizedBox(width: 8),
              Expanded(child: ElevatedButton(onPressed: () => _generate(), style: ElevatedButton.styleFrom(backgroundColor: Colors.green), child: const Text('Generar Audio'))),
            ]),
            const SizedBox(height: 16),
            LinearProgressIndicator(value: _progress),
            const SizedBox(height: 8),
            Text(_status),
          ],
        ),
      ),
    );
  }
}
