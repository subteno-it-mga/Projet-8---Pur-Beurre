import polib
from django.core import management
from django.conf import settings
from google.cloud import translate_v2 as translate

def create_local_path_po(language):
    management.call_command('makemessages', '-l'+ language, '-igoogle-cloud-sdk')

def translate_po(language_to):
    ts = translate.Client()
    if not language_to == 'en':
        if language_to in settings.SUPPORTED_LANGUAGES:
            if language_to == 'zh-hans':
                language_to = 'zh'
            create_local_path_po(language_to)
            path = 'locale/'+ language_to +'/LC_MESSAGES/django.po'
            po = polib.pofile(path)
            for entry in po:
                trans = ts.translate(entry.msgid, target_language=language_to)
                entry.msgstr = trans.get('translatedText')
                print(entry.msgid)
                print(trans)
            po.save(path)
            management.call_command('compilemessages')
