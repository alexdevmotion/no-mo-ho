import spacy
from tone_analyzer import ToneAnalyzer
from deoffensate_similarity import eliminate_lemma_clones

class TokenParser:

    def __init__(self, tone_analyzer = ToneAnalyzer()):
        self.nlp = spacy.load('en_core_web_lg')
        self.tone_analyzer = tone_analyzer

    def get_offensive_tokens(self, text):
        bad_words = self.tone_analyzer.get_bad_words(text)
        split_words = []
        for word in bad_words:
            split_words += word[0].split(" ")    
        return  self._tokenize(text, split_words)

    def _tokenize(self, text, word_list):
        doc = self.nlp(text)
        return [token for token in doc if token.text in word_list]

if __name__ == "__main__":
    
    text = "Yo nigga, what's up, get your shit, shits together, you whiny bitch."

    parser = TokenParser()    
    tokens = parser.get_offensive_tokens(text)
    print(tokens)
    print(eliminate_lemma_clones(tokens))