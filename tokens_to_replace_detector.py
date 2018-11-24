import spacy

class TokenParser:

    def __init__(self):
        # nlp = spacy.load('en_core_web_lg')
        self.nlp = spacy.load('en')

    def get_tokens(self, str):
        doc = self.nlp(blob)
        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)


if __name__ == "__main__":
    blob = 'Ariana is a stupid bitch'
    parser = TokenParser()    
    parser.get_tokens(blob)