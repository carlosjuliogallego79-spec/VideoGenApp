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
    Voice(name: 'Español - Argentina', lang: 'es-AR'),
    Voice(name: 'Español - Chile', lang: 'es-CL'),
    Voice(name: 'Español - Perú', lang: 'es-PE'),
    Voice(name: 'Español - Venezuela', lang: 'es-VE'),
    Voice(name: 'Español - Estados Unidos', lang: 'es-US'),
  ];
}
