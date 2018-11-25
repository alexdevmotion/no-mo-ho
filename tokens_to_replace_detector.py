import spacy
from tone_analyzer import ToneAnalyzer
from deoffensate_similarity import eliminate_lemma_clones


class TokenParser:
    def __init__(self, tone_analyzer=ToneAnalyzer(), nlp=spacy.load('en_core_web_lg')):
        self.nlp = nlp
        self.tone_analyzer = tone_analyzer

    def get_offensive_tokens(self, text):
        try:
            bad_words = self.tone_analyzer.get_bad_words(text)
        except:
            print('Failed to make request for NLU')
            return []
        tokens = []
        for word in bad_words:
            tokens += self.nlp(word[0])
        return [token for token in tokens if token.pos_ in ['VERB', 'ADJ', 'ADV', 'NOUN', 'INTJ']]


if __name__ == "__main__":
    text = "Codette is the worst organization the Earth has seen!"

    parser = TokenParser()    
    tokens = parser.get_offensive_tokens(text)
    print(tokens)
    print(eliminate_lemma_clones(tokens))
