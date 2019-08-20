import os

from google.cloud import translate

credential_path = "/home/ubuntu/google_translate_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

translate_client = translate.Client()

text = u'Hello world!'
target = 'ko'

translation = translate_client.translate(text,
		target_language=target)

print(u'TextL {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))

