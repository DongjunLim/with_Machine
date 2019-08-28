import os
import six
from google.cloud import translate

credential_path = "/home/ubuntu/google_translate_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

translate_client = translate.Client()

'''text = u'Hello world!'
target = 'ko'

translation = translate_client.translate(text,
		target_language=target)

print(u'TextL {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))


text = "Hi I'm Dongjun Nice to meet you"
target = 'ja'
if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(
    text, target_language=target)

print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
print(u'Detected source language: {}'.format(
    result['detectedSourceLanguage']))
'''

def translate_language(text,language):
    if isinstance(text,six.binary_type):
        text = text.decode('utf-8')
    result = translate_client.translate(text,target_language=language)

    return result['translatedText']
