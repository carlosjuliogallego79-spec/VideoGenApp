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
    Voice(name: 'Español - México', lang: 'es-MX', gender: 'female'),
    Voice(name: 'Español - España', lang: 'es-ES', gender: 'female'),
    Voice(name: 'English - US', lang: 'en-US', gender: 'female'),
    Voice(name: 'English - UK', lang: 'en-GB', gender: 'male'),
    Voice(name: 'Português - Brasil', lang: 'pt-BR', gender: 'female'),
    Voice(name: 'Français - France', lang: 'fr-FR', gender: 'female'),
  ];
}
