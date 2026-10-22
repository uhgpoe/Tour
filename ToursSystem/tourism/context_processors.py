"""
Context processors for language switching and localization in Wanderlust Tours.
"""

from django.utils.translation import get_language


def language_context(request):
    """
    Exposes current language state and switcher options to all templates.
    """
    # Prefer explicit session value, fallback to get_language()
    current_lang = request.session.get('django_language') or get_language() or 'en'
    current_lang = current_lang.lower().split('-')[0]
    if current_lang not in ['en', 'km']:
        current_lang = 'en'

    languages = [
        {
            'code': 'en',
            'name': 'English',
            'native': 'English',
            'flag': '🇬🇧',
            'active': current_lang == 'en',
        },
        {
            'code': 'km',
            'name': 'Khmer',
            'native': 'ភាសាខ្មែរ',
            'flag': '🇰🇭',
            'active': current_lang == 'km',
        },
    ]

    current_item = next((item for item in languages if item['code'] == current_lang), languages[0])

    return {
        'CURRENT_LANGUAGE': current_lang,
        'IS_KHMER': current_lang == 'km',
        'IS_ENGLISH': current_lang == 'en',
        'AVAILABLE_LANGUAGES': languages,
        'CURRENT_LANG_NAME': current_item['native'],
        'CURRENT_LANG_FLAG': current_item['flag'],
    }
