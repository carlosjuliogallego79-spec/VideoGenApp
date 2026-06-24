class Voice {
  final String name;
  final String lang;
  final String gender;

  const Voice({
    required this.name,
    required this.lang,
    required this.gender,
  });

  static const List<Voice> availableVoices = [
    // Español - variedad de países y géneros
    Voice(name: 'Español - México (Mujer)', lang: 'es-MX', gender: 'female'),
    Voice(name: 'Español - México (Hombre)', lang: 'es-MX', gender: 'male'),
    Voice(name: 'Español - España (Mujer)', lang: 'es-ES', gender: 'female'),
    Voice(name: 'Español - España (Hombre)', lang: 'es-ES', gender: 'male'),
    Voice(name: 'Español - Argentina', lang: 'es-AR', gender: 'female'),
    Voice(name: 'Español - Colombia', lang: 'es-CO', gender: 'female'),
    Voice(name: 'Español - Chile', lang: 'es-CL', gender: 'female'),
    Voice(name: 'Español - Perú', lang: 'es-PE', gender: 'female'),
    Voice(name: 'Español - Venezuela', lang: 'es-VE', gender: 'female'),
    Voice(name: 'Español - Estados Unidos', lang: 'es-US', gender: 'male'),
    // English - variety of regions and genders
    Voice(name: 'English - US (Female)', lang: 'en-US', gender: 'female'),
    Voice(name: 'English - US (Male)', lang: 'en-US', gender: 'male'),
    Voice(name: 'English - UK (Female)', lang: 'en-GB', gender: 'female'),
    Voice(name: 'English - UK (Male)', lang: 'en-GB', gender: 'male'),
    Voice(name: 'English - Australia', lang: 'en-AU', gender: 'female'),
    Voice(name: 'English - Canada', lang: 'en-CA', gender: 'female'),
    Voice(name: 'English - India', lang: 'en-IN', gender: 'female'),
    Voice(name: 'English - Ireland', lang: 'en-IE', gender: 'male'),
    Voice(name: 'English - New Zealand', lang: 'en-NZ', gender: 'female'),
    Voice(name: 'English - South Africa', lang: 'en-ZA', gender: 'female'),
    // Otros idiomas
    Voice(name: 'Português - Brasil', lang: 'pt-BR', gender: 'female'),
    Voice(name: 'Português - Portugal', lang: 'pt-PT', gender: 'male'),
    Voice(name: 'Français - France', lang: 'fr-FR', gender: 'female'),
    Voice(name: 'Français - Canada', lang: 'fr-CA', gender: 'male'),
    Voice(name: 'Deutsch - Deutschland', lang: 'de-DE', gender: 'female'),
    Voice(name: 'Italiano - Italia', lang: 'it-IT', gender: 'female'),
    Voice(name: '日本語 - 日本', lang: 'ja-JP', gender: 'female'),
    Voice(name: '中文 - 中国', lang: 'zh-CN', gender: 'female'),
    Voice(name: '한국어 - 대한민국', lang: 'ko-KR', gender: 'female'),
  ];
}
