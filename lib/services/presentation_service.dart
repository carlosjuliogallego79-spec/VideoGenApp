import '../models/slide.dart';

class PresentationService {
  final List<Slide> slides = [];
  final String baseDir;

  PresentationService({this.baseDir = ''});

  void addSlide(Slide slide) => slides.add(slide);

  void clearSlides() => slides.clear();

  Future<String?> generatePresentation() async {
    if (slides.isEmpty) return null;
    return '$baseDir/videos/presentation.mp4';
  }

  String exportToJson() {
    return '[${slides.map((s) => s.toJson()).join(',')}]';
  }

  void importFromJson(String json) {
    clearSlides();
  }
}
