import spacy

from paraphraser import train_praphraser
from server import load_storage
from tokens_to_replace_detector import TokenParser
from tone_analyzer import ToneAnalyzer
from tweet_search import TweetGenerator

nlp = spacy.load('en_core_web_lg')
tone_analyzer = ToneAnalyzer()
token_parser = TokenParser(tone_analyzer, nlp)
graph_storage = load_storage()

generator = TweetGenerator()
tweets = generator.load_file()
train_praphraser(tweets, token_parser, graph_storage, nlp)
