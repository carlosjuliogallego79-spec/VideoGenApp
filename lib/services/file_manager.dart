import 'dart:io';

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

  FileManager() {
    baseDir = '/storage/emulated/0/VideoGenApp';
    importDir = '$baseDir/imports';
    exportDir = '$baseDir/exports';
    tempDir = '$baseDir/temp';
    for (final d in [importDir, exportDir, tempDir]) {
      Directory(d).createSync(recursive: true);
    }
  }

  String getStorageInfo() {
    int totalSize = 0;
    final dir = Directory(baseDir);
    if (dir.existsSync()) {
      for (var entity in dir.listSync(recursive: true)) {
        if (entity is File) {
          totalSize += entity.lengthSync();
        }
      }
    }
    if (totalSize < 1024) return '$totalSize B';
    if (totalSize < 1024 * 1024) return '${(totalSize / 1024).toStringAsFixed(1)} KB';
    if (totalSize < 1024 * 1024 * 1024) return '${(totalSize / (1024 * 1024)).toStringAsFixed(1)} MB';
    return '${(totalSize / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
  }

  void clearTemp() {
    final dir = Directory(tempDir);
    if (dir.existsSync()) {
      for (var entity in dir.listSync()) {
        if (entity is File) entity.deleteSync();
      }
    }
  }
}
