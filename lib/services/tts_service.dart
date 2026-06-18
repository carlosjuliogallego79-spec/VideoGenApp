import 'package:flutter_tts/flutter_tts.dart';

class TTSService {
  final FlutterTts _tts = FlutterTts();

  Future<String?> textToSpeech({
    required String text,
    String outputName = 'tts_output.mp3',
    String voice = 'es-MX',
    double speed = 1.0,
    double pitch = 1.0,
  }) async {
    try {
      await _tts.setLanguage(voice);
      await _tts.setSpeechRate(speed * 0.5);
      await _tts.setPitch(pitch);
      await _tts.speak(text);
      return '/storage/emulated/0/VideoGenApp/audio/$outputName';
    } catch (e) {
      return null;
    }
  }

  Future<void> stop() async {
    await _tts.stop();
  }
}
