class Slide {
  String title;
  String content;
  String? imagePath;
  String animation;
  double duration;
  String notes;

  Slide({
    this.title = '',
    this.content = '',
    this.imagePath,
    this.animation = 'fade_in',
    this.duration = 5.0,
    this.notes = '',
  });

  Map<String, dynamic> toJson() => {
        'title': title,
        'content': content,
        'image_path': imagePath,
        'animation': animation,
        'duration': duration,
        'notes': notes,
      };

  factory Slide.fromJson(Map<String, dynamic> json) => Slide(
        title: json['title'] ?? '',
        content: json['content'] ?? '',
        imagePath: json['image_path'],
        animation: json['animation'] ?? 'fade_in',
        duration: (json['duration'] ?? 5.0).toDouble(),
        notes: json['notes'] ?? '',
      );
}
