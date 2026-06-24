class VideoService {
  final String baseDir;

  VideoService({this.baseDir = ''});

  Future<String?> imagesToVideo({
    required List<String> imagePaths,
    String outputName = 'output.mp4',
    int fps = 24,
    double durationPerImage = 3,
    String transition = 'fade',
    (int, int) resolution = (1920, 1080),
  }) async {
    return '$baseDir/videos/$outputName';
  }

  Future<String?> addTextOverlay(String videoPath, String text) async {
    return videoPath;
  }

  Future<String?> addMusic(String videoPath, String audioPath) async {
    return videoPath;
  }
}
