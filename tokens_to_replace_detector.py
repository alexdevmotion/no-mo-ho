import spacy
from tone_analyzer import ToneAnalyzer

class TokenParser:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        # self.nlp = spacy.load('en')

    def get_tokens(self, text, word_list):
        doc = self.nlp(text)
        return [token for token in doc if token.text in word_list]

if __name__ == "__main__":
    
    text = "Yo nigga, what's up, get your shit together, you whiny bitch."
    
    analyzer = ToneAnalyzer()
    bad_words = analyzer.get_bad_words(text)
    split_words = []
    for word in bad_words:
        split_words += word[0].split(" ")

    parser = TokenParser()    
    tokens = parser.get_tokens(text, split_words)
    print(tokens)