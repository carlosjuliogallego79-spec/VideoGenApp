class FFmpegHelper {
  bool isAvailable() {
    // TODO: Check ffmpeg availability
    return false;
  }

  Future<Map<String, dynamic>?> probe(String filepath) async {
    return null;
  }

  double getDuration(String filepath) {
    return 0.0;
  }

  (int, int)? getResolution(String videoPath) {
    return null;
  }

  Future<String?> convertFormat(String inputPath, String outputPath) async {
    return null;
  }
}
