import 'dart:io';
import 'package:flutter_tts/flutter_tts.dart';
import '../models/voice.dart';

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
    String? voiceId,
  }) async {
    try {
      if (voiceId != null) {
        await _tts.setVoice({'name': voiceId, 'locale': voice});
      } else {
        await _tts.setLanguage(voice);
      }
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
      await _tts.speak(text);

      return outPath;
    } catch (e) {
      return null;
    }
  }

  Future<List<Voice>> getAvailableVoices() async {
    try {
      final raw = await _tts.getVoices;
      if (raw is List) {
        return raw
            .whereType<Map<dynamic, dynamic>>()
            .map((m) => Voice.fromEngineVoice(
                m.map((k, v) => MapEntry(k.toString(), v.toString()))))
            .toList();
      }
    } catch (_) {}
    return Voice.availableVoices;
  }

  Future<void> stop() async {
    await _tts.stop();
  }
}
