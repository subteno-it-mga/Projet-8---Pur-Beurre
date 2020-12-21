from django import template
from..models import PBLanguage


register = template.Library()

@register.simple_tag
def get_translated_languages():
    all_languages = PBLanguage.objects.all()
    lang_array = []
    for lang in all_languages:
        lang_array.append(lang.language_code)

    return lang_array