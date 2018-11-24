import spacy


blob = 'Ariana is a stupid bitch'
nlp = spacy.load('en_core_web_sm')
doc = nlp(blob)

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)