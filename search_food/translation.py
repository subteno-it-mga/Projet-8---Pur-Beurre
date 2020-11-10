import translators as ts
import polib
from django.core import management
from django.conf import settings

def create_local_path_po(language):
    management.call_command('makemessages', '-l'+ language)

def translate_po(language_to):
    if not language_to == 'en':
        if language_to in settings.SUPPORTED_LANGUAGES:
            create_local_path_po(language_to)
            path = 'locale/'+ language_to +'/LC_MESSAGES/django.po'
            po = polib.pofile(path)
            for entry in po:
                trans = ts.alibaba(entry.msgid, from_language='en', to_language=language_to)
                entry.msgstr = trans
            po.save(path)
            management.call_command('compilemessages')
