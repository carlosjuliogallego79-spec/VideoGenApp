import 'package:flutter/material.dart';
import '../models/slide.dart';
import '../services/presentation_service.dart';

class PresentationPage extends StatefulWidget {
  const PresentationPage({super.key});

  @override
  State<PresentationPage> createState() => _PresentationPageState();
}

class _PresentationPageState extends State<PresentationPage> {
  final _service = PresentationService();
  final _titleController = TextEditingController(text: 'Título del Slide');
  final _contentController = TextEditingController(text: 'Contenido del slide aquí...');
  final _durationController = TextEditingController(text: '5');
  final _animController = TextEditingController(text: 'fade_in');
  String _status = 'Listo';
  double _progress = 0;

  @override
  void dispose() {
    _titleController.dispose();
    _contentController.dispose();
    _durationController.dispose();
    _animController.dispose();
    super.dispose();
  }

  void _addSlide() {
    _service.addSlide(Slide(
      title: _titleController.text,
      content: _contentController.text,
      animation: _animController.text,
      duration: double.tryParse(_durationController.text) ?? 5.0,
    ));
    setState(() {});
  }

  void _clearSlides() {
    _service.clearSlides();
    setState(() {});
  }

  void _deleteSlide(int index) {
    if (index >= 0 && index < _service.slides.length) {
      _service.slides.removeAt(index);
      setState(() {});
    }
  }

  Future<void> _generate() async {
    if (_service.slides.isEmpty) {
      setState(() => _status = 'Añade al menos un slide');
      return;
    }
    setState(() { _status = 'Generando presentación...'; _progress = 0.1; });

    final output = await _service.generatePresentation();
    setState(() => _progress = 1.0);
    if (output != null) {
      setState(() => _status = 'Presentación generada');
      if (mounted) _showSuccess('Presentación guardada en:\n$output');
    } else {
      setState(() { _status = 'Error generando presentación'; _progress = 0; });
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
      appBar: AppBar(title: const Text('Presentaciones')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text('Nuevo Slide:', style: Theme.of(context).textTheme.titleSmall),
            TextField(controller: _titleController, decoration: const InputDecoration(labelText: 'Título')),
            TextField(controller: _contentController, decoration: const InputDecoration(labelText: 'Contenido'), maxLines: 2),
            TextField(controller: _durationController, decoration: const InputDecoration(labelText: 'Duración (s)')),
            TextField(controller: _animController, decoration: const InputDecoration(labelText: 'Animación')),
            const SizedBox(height: 8),
            Row(children: [
              ElevatedButton(onPressed: _addSlide, child: const Text('Añadir Slide')),
              const SizedBox(width: 8),
              OutlinedButton(onPressed: _clearSlides, child: const Text('Limpiar Todo')),
            ]),
            const SizedBox(height: 16),
            Text('Slides (${_service.slides.length}):', style: Theme.of(context).textTheme.titleSmall),
            Expanded(
              child: ListView.builder(
                itemCount: _service.slides.length,
                itemBuilder: (context, i) => ListTile(
                  title: Text('${i + 1}. ${_service.slides[i].title}'),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete, color: Colors.red),
                    onPressed: () => _deleteSlide(i),
                  ),
                ),
              ),
            ),
            ElevatedButton(onPressed: _generate, style: ElevatedButton.styleFrom(backgroundColor: Colors.green), child: const Text('Generar Presentación')),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: _progress),
            Text(_status),
          ],
        ),
      ),
    );
  }
}
