import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../services/video_service.dart';

class VideoGeneratorPage extends StatefulWidget {
  const VideoGeneratorPage({super.key});

  @override
  State<VideoGeneratorPage> createState() => _VideoGeneratorPageState();
}

class _VideoGeneratorPageState extends State<VideoGeneratorPage> {
  final _videoService = VideoService();
  final _fpsController = TextEditingController(text: '24');
  final _durationController = TextEditingController(text: '3');
  final _widthController = TextEditingController(text: '1920');
  final _heightController = TextEditingController(text: '1080');
  List<String> _selectedImages = [];
  String _transition = 'fade';
  String _status = 'Listo';
  double _progress = 0;

  @override
  void dispose() {
    _fpsController.dispose();
    _durationController.dispose();
    _widthController.dispose();
    _heightController.dispose();
    super.dispose();
  }

  Future<void> _pickImages() async {
    final result = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
      allowMultiple: true,
    );
    if (result != null) {
      setState(() {
        _selectedImages = result.paths.where((p) => p != null).cast<String>().toList();
        _status = 'Imágenes seleccionadas: ${_selectedImages.length}';
      });
    }
  }

  Future<void> _generate() async {
    if (_selectedImages.isEmpty) {
      setState(() => _status = 'Selecciona al menos una imagen');
      return;
    }
    setState(() { _status = 'Generando video...'; _progress = 0.2; });

    final fps = int.tryParse(_fpsController.text) ?? 24;
    final duration = double.tryParse(_durationController.text) ?? 3;
    final width = int.tryParse(_widthController.text) ?? 1920;
    final height = int.tryParse(_heightController.text) ?? 1080;

    final output = await _videoService.imagesToVideo(
      imagePaths: _selectedImages,
      fps: fps,
      durationPerImage: duration,
      transition: _transition,
      resolution: (width, height),
    );

    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Video generado');
      if (mounted) _showSuccess('Video guardado en:\n$output');
    } else {
      setState(() { _status = 'Error generando video'; _progress = 0; });
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
      appBar: AppBar(title: const Text('Generar Video')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _fpsController, decoration: const InputDecoration(labelText: 'FPS')),
            TextField(controller: _durationController, decoration: const InputDecoration(labelText: 'Duración por imagen (s)')),
            DropdownButtonFormField<String>(
              value: _transition,
              decoration: const InputDecoration(labelText: 'Transición'),
              items: ['fade', 'slide', 'zoom'].map((t) => DropdownMenuItem(value: t, child: Text(t))).toList(),
              onChanged: (v) => setState(() => _transition = v!),
            ),
            Row(children: [
              Expanded(child: TextField(controller: _widthController, decoration: const InputDecoration(labelText: 'Ancho'))),
              const Padding(padding: EdgeInsets.symmetric(horizontal: 8), child: Text('x')),
              Expanded(child: TextField(controller: _heightController, decoration: const InputDecoration(labelText: 'Alto'))),
            ]),
            const SizedBox(height: 16),
            Text('Imágenes seleccionadas: ${_selectedImages.length}'),
            const SizedBox(height: 8),
            Row(children: [
              Expanded(child: ElevatedButton(onPressed: _pickImages, child: const Text('Seleccionar Imágenes'))),
              const SizedBox(width: 8),
              Expanded(child: ElevatedButton(onPressed: _generate, style: ElevatedButton.styleFrom(backgroundColor: Colors.green), child: const Text('Generar Video'))),
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
