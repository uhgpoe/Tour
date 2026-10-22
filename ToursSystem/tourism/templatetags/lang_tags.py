from django import template
from django.utils.translation import gettext as _gettext, get_language
from tourism.translations import translate_text, TRANSLATIONS_KM

register = template.Library()


@register.filter(name='t')
def translate_filter(value, lang=None):
    """
    Template filter: {{ "Home"|t }}
    Translates English string to active language (e.g. Khmer).
    """
    if not value:
        return value
    if lang is None:
        lang = get_language() or 'en'
    
    val_str = str(value)
    # Check dictionary first
    translated = translate_text(val_str, lang=lang)
    if translated != val_str:
        return translated
    
    # Check Django gettext
    django_trans = _gettext(val_str)
    if django_trans != val_str:
        return django_trans

    return val_str


@register.simple_tag(takes_context=True, name='t')
def translate_tag(context, text):
    """
    Simple tag: {% t "Explore Packages" %}
    """
    if not text:
        return ''
    
    request = context.get('request')
    lang = None
    if request:
        lang = request.session.get('django_language') or getattr(request, 'LANGUAGE_CODE', None)
    if not lang:
        lang = get_language() or 'en'

    return translate_filter(text, lang=lang)


@register.simple_tag(takes_context=True)
def is_khmer_active(context):
    """Helper to check if current language is Khmer."""
    request = context.get('request')
    lang = None
    if request:
        lang = request.session.get('django_language') or getattr(request, 'LANGUAGE_CODE', None)
    if not lang:
        lang = get_language() or 'en'
    return lang.lower().startswith('km')
