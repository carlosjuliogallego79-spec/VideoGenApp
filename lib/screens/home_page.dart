import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('VideoGenApp')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const Spacer(flex: 2),
              Icon(Icons.video_library, size: 80, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 16),
              Text(
                'VideoGenApp',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(
                'Generación de Video y Sincronización de Voz',
                style: Theme.of(context).textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),
              const Spacer(flex: 3),
              _MenuButton(
                icon: Icons.movie_creation,
                label: 'Generar Video',
                subtitle: 'Crear video desde imágenes con transiciones',
                onTap: () => Navigator.pushNamed(context, '/video'),
              ),
              _MenuButton(
                icon: Icons.record_voice_over,
                label: 'Texto a Voz',
                subtitle: 'Convertir texto a voz narrada',
                onTap: () => Navigator.pushNamed(context, '/tts'),
              ),
              _MenuButton(
                icon: Icons.slideshow,
                label: 'Presentaciones',
                subtitle: 'Crear slideshows animados',
                onTap: () => Navigator.pushNamed(context, '/presentation'),
              ),
              _MenuButton(
                icon: Icons.sync,
                label: 'Sincronizar Voz',
                subtitle: 'Sincronizar y clonar voces',
                onTap: () => Navigator.pushNamed(context, '/voice_sync'),
              ),
              _MenuButton(
                icon: Icons.settings,
                label: 'Configuración',
                subtitle: 'Ajustes de la aplicación',
                onTap: () => Navigator.pushNamed(context, '/settings'),
              ),
              const Spacer(flex: 2),
              Text('Hecho con Flutter | Dart para Android',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.grey)),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class _MenuButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final String subtitle;
  final VoidCallback onTap;

  const _MenuButton({
    required this.icon,
    required this.label,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        leading: Icon(icon, size: 32, color: Theme.of(context).colorScheme.primary),
        title: Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
