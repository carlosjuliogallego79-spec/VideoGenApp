class Voice {
  final String name;
  final String lang;
  final String? voiceId;

  const Voice({
    required this.name,
    required this.lang,
    this.voiceId,
  });

  Voice.fromEngineVoice(Map<String, String> v)
      : name = v['name'] ?? v['locale'] ?? 'Unknown',
        lang = v['locale'] ?? 'en-US',
        voiceId = v['name'];

  static const List<Voice> availableVoices = [
    Voice(name: 'Español - México', lang: 'es-MX'),
    Voice(name: 'Español - Colombia', lang: 'es-CO'),
  ];
}
