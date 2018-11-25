import json
import pickle
import spacy
from flask import Flask, request

from graph_mapping_storage import GraphMappingStorage
from paraphraser import paraphrase
from tokens_to_replace_detector import TokenParser
from tone_analyzer import ToneAnalyzer


app = Flask(__name__)
STORAGE_PATH = 'storage/graph.pkl'


def load_storage():
    try:
        storage_file = open(STORAGE_PATH, 'rb')
        return pickle.load(storage_file)
    except:
        return GraphMappingStorage()


nlp = spacy.load('en_core_web_lg')
tone_analyzer = ToneAnalyzer()
token_parser = TokenParser(tone_analyzer, nlp)
graph_storage = load_storage()


@app.route('/noho')
def noho():
    text = request.args.get('q')
    paraphrases = paraphrase(text, graph_storage, token_parser, nlp)
    return json.dumps(paraphrases)


if __name__ == "__main__":
    app.run(port='5000', host='0.0.0.0')
