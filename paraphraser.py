import pickle
import spacy

from deoffensate_similarity import deoffensate_word_similarity_approach, is_still_offensive
from graph_mapping_storage import GraphMappingStorage
from tokens_to_replace_detector import TokenParser
from tone_analyzer import ToneAnalyzer

nlp = spacy.load('en_core_web_lg')

STORAGE_PATH = 'storage/graph.pkl'


def pad_deoffensated(deoffensated_words, num_options):
    if deoffensated_words is None:
        return [''] * num_options
    if len(deoffensated_words) >= num_options:
        return deoffensated_words + ['']
    return deoffensated_words + ((num_options - len(deoffensated_words)) * [''])


def noho_resolve(text, offensive_tokens, graph_storage, token_parser, num_options):
    result = [text] * num_options
    while len(offensive_tokens) > 0:
        offensive_token = offensive_tokens[0]
        # TODO implement ad hoc train if you don't find alternatives for the token
        deoffensated_words = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        padded_deoffensated = pad_deoffensated(deoffensated_words, num_options)

        for i in range(0, num_options):
            for j in range(0, len(padded_deoffensated)):
                deoffensated_word = padded_deoffensated[j]
                if len(deoffensated_word) == 0:
                    result[i] = result[i].replace(offensive_token.text + ' ', '')
                    result[i] = result[i].replace(' ' + offensive_token.text, '')
                    break
                # TODO instead of settling with the first acceptable variant, rank them all after how positive they are
                # call get_tone on each token and rank them by how positive they are, then take them in that order
                # order_deoffensated_by_positiveness(deoffensated_words)
                is_still, _remaining_offensive_tokens = is_still_offensive(result[i], offensive_token.text, deoffensated_word, token_parser)
                if not is_still:
                    offensive_tokens = _remaining_offensive_tokens
                    result[i] = result[i].replace(offensive_token.text, deoffensated_word)
                    padded_deoffensated.remove(deoffensated_word)
                    break
    return result


def noho_train(text, offensive_tokens, token_parser, graph_storage):
    found_something = False
    while len(offensive_tokens) > 0:
        offensive_token = offensive_tokens[0]
        deoffensated_words_in_graph = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        if deoffensated_words_in_graph is None:
            found_something = True
            deoffensated_words, new_offensive_tokens = deoffensate_word_similarity_approach(text, offensive_token, nlp, token_parser)
            graph_storage.add_non_offensive_mapping(offensive_token.text, deoffensated_words)
            if new_offensive_tokens is None:
                offensive_tokens.remove(offensive_token)
            else:
                offensive_tokens = new_offensive_tokens
        else:
            break
    return found_something


def load():
    try:
        storage_file = open(STORAGE_PATH, 'rb')
        return pickle.load(storage_file)
    except:
        return GraphMappingStorage()


def persist(graph_storage):
    out_file = open(STORAGE_PATH, 'wb')
    pickle.dump(graph_storage, out_file)


def paraphrase(text, num_options=4):
    graph_storage = load()
    tone_analyzer = ToneAnalyzer()
    parser = TokenParser(tone_analyzer, nlp)
    offensive_tokens = parser.get_offensive_tokens(text)

    return noho_resolve(text, offensive_tokens, graph_storage, parser, num_options)


def train_praphraser(texts):
    graph_storage = load()
    tone_analyzer = ToneAnalyzer()
    parser = TokenParser(tone_analyzer, nlp)

    for text in texts:
        print('Processing:', text)
        offensive_tokens = parser.get_offensive_tokens(text)
        if noho_train(text, offensive_tokens, parser, graph_storage):
            print('Persisting...')
            persist(graph_storage)
        else:
            print('Nothing to persist...')
