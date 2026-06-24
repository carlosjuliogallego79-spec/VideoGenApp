import 'dart:io';
import 'package:path_provider/path_provider.dart';

class FileManager {
  late final String baseDir;
  late final String importDir;
  late final String exportDir;
  late final String tempDir;

  static const Map<String, List<String>> mediaExtensions = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'],
    'audio': ['.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a'],
  };

  FileManager._();

  static Future<FileManager> create() async {
    final fm = FileManager._();
    await fm._init();
    return fm;
  }

  Future<void> _init() async {
    try {
      final appsDir = await getExternalStorageDirectory();
      baseDir = appsDir!.path;
      importDir = '$baseDir/imports';
      exportDir = '$baseDir/exports';
      tempDir = '$baseDir/temp';
      for (final d in [importDir, exportDir, tempDir]) {
        await Directory(d).create(recursive: true);
      }
    } catch (e) {
      try {
        final appDir = await getApplicationDocumentsDirectory();
        baseDir = appDir.path;
        importDir = '$baseDir/imports';
        exportDir = '$baseDir/exports';
        tempDir = '$baseDir/temp';
        for (final d in [importDir, exportDir, tempDir]) {
          await Directory(d).create(recursive: true);
        }
      } catch (e2) {
        baseDir = '/tmp/VideoGenApp';
        importDir = '$baseDir/imports';
        exportDir = '$baseDir/exports';
        tempDir = '$baseDir/temp';
      }
    }
  }

  String getStorageInfo() {
    try {
      final dir = Directory(baseDir);
      if (!dir.existsSync()) return '0 B';
      int totalSize = 0;
      for (var entity in dir.listSync(recursive: true)) {
        if (entity is File) {
          totalSize += entity.lengthSync();
        }
      }
      if (totalSize < 1024) return '$totalSize B';
      if (totalSize < 1024 * 1024) return '${(totalSize / 1024).toStringAsFixed(1)} KB';
      if (totalSize < 1024 * 1024 * 1024) return '${(totalSize / (1024 * 1024)).toStringAsFixed(1)} MB';
      return '${(totalSize / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
    } catch (e) {
      return 'Error';
    }
  }

  void clearTemp() {
    try {
      final dir = Directory(tempDir);
      if (dir.existsSync()) {
        for (var entity in dir.listSync()) {
          if (entity is File) entity.deleteSync();
        }
      }
    } catch (e) {
      // Silently fail
    }
  }
}
