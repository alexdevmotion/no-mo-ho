from polyglot.text import Text


blob = 'Ariana is a stupid bitch'
text = Text(blob, hint_language_code='en')

print(text.pos_tags)
