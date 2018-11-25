import spacy

from paraphraser import paraphrase
from server import load_storage
from tokens_to_replace_detector import TokenParser
from tone_analyzer import ToneAnalyzer

nlp = spacy.load('en_core_web_lg')
tone_analyzer = ToneAnalyzer()
token_parser = TokenParser(tone_analyzer, nlp)
graph_storage = load_storage()

text = "Codette is the worst organization the Earth has ever seen!"
print(paraphrase(text, graph_storage, token_parser, nlp))
