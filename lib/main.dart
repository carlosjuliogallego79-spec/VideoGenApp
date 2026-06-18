import 'package:flutter/material.dart';
import 'screens/home_page.dart';
import 'screens/video_generator_page.dart';
import 'screens/tts_page.dart';
import 'screens/presentation_page.dart';
import 'screens/voice_sync_page.dart';
import 'screens/settings_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const VideoGenApp());
}

class VideoGenApp extends StatelessWidget {
  const VideoGenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'VideoGenApp',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: Colors.blue,
        useMaterial3: true,
        brightness: Brightness.dark,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(),
        '/video': (context) => const VideoGeneratorPage(),
        '/tts': (context) => const TTSPage(),
        '/presentation': (context) => const PresentationPage(),
        '/voice_sync': (context) => const VoiceSyncPage(),
        '/settings': (context) => const SettingsPage(),
      },
    );
  }
}
