import '../models/slide.dart';

class PresentationService {
  final List<Slide> slides = [];

  void addSlide(Slide slide) => slides.add(slide);

  void clearSlides() => slides.clear();

  Future<String?> generatePresentation() async {
    if (slides.isEmpty) return null;
    return '/storage/emulated/0/VideoGenApp/videos/presentation.mp4';
  }

  String exportToJson() {
    return '[${slides.map((s) => s.toJson()).join(',')}]';
  }

  void importFromJson(String json) {
    clearSlides();
    // Parse JSON and add slides
  }
}
