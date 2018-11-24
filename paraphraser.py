import pickle
import random
import spacy

from deoffensate_similarity import deoffensate_word_similarity_approach
from graph_mapping_storage import GraphMappingStorage
from tokens_to_replace_detector import TokenParser
from tone_analyzer import ToneAnalyzer

nlp = spacy.load('en_core_web_lg')

STORAGE_PATH = 'storage/graph.pkl'


def noho_resolve(text, offensive_tokens, graph_storage, num_options=5):
    result = [text] * num_options
    for offensive_token in offensive_tokens:
        deoffensated_words = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        if len(deoffensated_words) < num_options:
            num_options = len(deoffensated_words)
            result = result[:num_options]
        ranomized_deoffensated = random.sample(deoffensated_words, num_options)
        for i in range(0, num_options):
            result[i] = result[i].replace(offensive_token.text, ranomized_deoffensated[i])
    return result


def noho_train(text, offensive_tokens, token_parser, graph_storage):
    for offensive_token in offensive_tokens:
        deoffensated_words_in_graph = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        if deoffensated_words_in_graph is None:
            deoffensated_words = deoffensate_word_similarity_approach(text, offensive_token, nlp, token_parser)
            graph_storage.add_non_offensive_mapping(offensive_token.text, deoffensated_words)


def load():
    try:
        storage_file = open(STORAGE_PATH, 'rb')
        return pickle.load(storage_file)
    except:
        return GraphMappingStorage()


def persist(graph_storage):
    out_file = open(STORAGE_PATH, 'wb')
    pickle.dump(graph_storage, out_file)


def paraphrase(text):
    graph_storage = load()
    tone_analyzer = ToneAnalyzer()
    parser = TokenParser(tone_analyzer)
    offensive_tokens = parser.get_offensive_tokens(text)

    return noho_resolve(text, offensive_tokens, graph_storage)


def train_praphraser(texts):
    graph_storage = load()
    tone_analyzer = ToneAnalyzer()
    parser = TokenParser(tone_analyzer)

    for text in texts:
        print('Processing', text)
        offensive_tokens = parser.get_offensive_tokens(text)
        noho_train(text, offensive_tokens, parser, graph_storage)

    print('Persisting...')
    persist(graph_storage)


if __name__ == '__main__':
    text = "Yo nigga, what's up, get your shit together, you whiny bitch."
    # paraphrase(text)

    train_praphraser([text])
