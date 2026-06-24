import 'dart:io';
import 'package:flutter_tts/flutter_tts.dart';

class TTSService {
  final FlutterTts _tts = FlutterTts();
  final String baseDir;

  TTSService({this.baseDir = ''});

  Future<String?> textToSpeech({
    required String text,
    String outputName = 'tts_output.wav',
    String voice = 'es-MX',
    double speed = 1.0,
    double pitch = 1.0,
    bool preview = false,
  }) async {
    try {
      await _tts.setLanguage(voice);
      await _tts.setSpeechRate(speed * 0.5);
      await _tts.setPitch(pitch);

      if (preview) {
        await _tts.speak(text);
        return 'preview_played';
      }

      final outDir = Directory('$baseDir/audio');
      if (!await outDir.exists()) {
        await outDir.create(recursive: true);
      }
      final outPath = '${outDir.path}/$outputName';

      await _tts.synthesizeToFile(text, outPath, true);

      return outPath;
    } catch (e) {
      return null;
    }
  }

  Future<void> stop() async {
    await _tts.stop();
  }
}
