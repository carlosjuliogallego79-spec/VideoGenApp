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
    // Español
    Voice(name: 'Español - México', lang: 'es-MX'),
    Voice(name: 'Español - España', lang: 'es-ES'),
    Voice(name: 'Español - Argentina', lang: 'es-AR'),
    Voice(name: 'Español - Colombia', lang: 'es-CO'),
    Voice(name: 'Español - Chile', lang: 'es-CL'),
    Voice(name: 'Español - Perú', lang: 'es-PE'),
    Voice(name: 'Español - Venezuela', lang: 'es-VE'),
    Voice(name: 'Español - Estados Unidos', lang: 'es-US'),
    // English
    Voice(name: 'English - US', lang: 'en-US'),
    Voice(name: 'English - UK', lang: 'en-GB'),
    Voice(name: 'English - Australia', lang: 'en-AU'),
    Voice(name: 'English - Canada', lang: 'en-CA'),
    Voice(name: 'English - India', lang: 'en-IN'),
    Voice(name: 'English - Ireland', lang: 'en-IE'),
    Voice(name: 'English - New Zealand', lang: 'en-NZ'),
    Voice(name: 'English - South Africa', lang: 'en-ZA'),
    // Otros idiomas
    Voice(name: 'Português - Brasil', lang: 'pt-BR'),
    Voice(name: 'Português - Portugal', lang: 'pt-PT'),
    Voice(name: 'Français - France', lang: 'fr-FR'),
    Voice(name: 'Français - Canada', lang: 'fr-CA'),
    Voice(name: 'Deutsch - Deutschland', lang: 'de-DE'),
    Voice(name: 'Italiano - Italia', lang: 'it-IT'),
    Voice(name: '日本語 - 日本', lang: 'ja-JP'),
    Voice(name: '中文 - 中国', lang: 'zh-CN'),
    Voice(name: '한국어 - 대한민국', lang: 'ko-KR'),
  ];
}
