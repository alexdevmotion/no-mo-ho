import pickle

from deoffensate_similarity import deoffensate_word_similarity_approach, is_still_offensive


STORAGE_PATH = 'storage/graph.pkl'


def pad_deoffensated(deoffensated_words, num_options):
    if deoffensated_words is None:
        return [''] * num_options
    if len(deoffensated_words) >= num_options:
        return deoffensated_words + ['']
    return deoffensated_words + ((num_options - len(deoffensated_words)) * [''])


def sort_deoffensated(deoffensated_words, tone_analyzer):
    if len(deoffensated_words) == 0 or deoffensated_words == ['']:
        return deoffensated_words
    deoffensated_word_tones = [(word, tone_analyzer.get_tone_score(word)) for word in deoffensated_words]
    sorted_deoffensated_word_tones = sorted(deoffensated_word_tones, key=lambda tup: tup[1], reverse=True)
    return [tup[0] for tup in sorted_deoffensated_word_tones]


def noho_resolve(text, offensive_tokens, graph_storage, token_parser, nlp, num_options):
    result = [text] * num_options
    while len(offensive_tokens) > 0:
        offensive_token = offensive_tokens[0]
        deoffensated_words = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        if deoffensated_words is None:
            print('Offensive token', offensive_token.text, 'not found, training ad hoc..')
            noho_train(text, offensive_tokens, token_parser, graph_storage, nlp)
            print('Persisting...')
            persist(graph_storage)
            deoffensated_words = graph_storage.get_non_offensive_alternatives(offensive_token.text)
        sorted_deoffensated = sort_deoffensated(deoffensated_words, token_parser.tone_analyzer)
        padded_deoffensated = pad_deoffensated(sorted_deoffensated, num_options)

        for i in range(0, num_options):
            for j in range(0, len(padded_deoffensated)):
                deoffensated_word = padded_deoffensated[j]
                if len(deoffensated_word) == 0:
                    result[i] = result[i].replace(offensive_token.text + ' ', '')
                    result[i] = result[i].replace(' ' + offensive_token.text, '')
                    if offensive_token in offensive_tokens:
                        offensive_tokens.remove(offensive_token)
                    break
                is_still, _remaining_offensive_tokens = is_still_offensive(result[i], offensive_token.text, deoffensated_word, token_parser)
                if not is_still:
                    offensive_tokens = _remaining_offensive_tokens
                    result[i] = result[i].replace(offensive_token.text, deoffensated_word)
                    padded_deoffensated.remove(deoffensated_word)
                    break
    return result


def noho_train(text, offensive_tokens, token_parser, graph_storage, nlp):
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


def persist(graph_storage):
    out_file = open(STORAGE_PATH, 'wb')
    pickle.dump(graph_storage, out_file)


def paraphrase(text, graph_storage, token_parser, nlp, num_options=4):
    offensive_tokens = token_parser.get_offensive_tokens(text)
    if len(offensive_tokens) == 0:
        return []
    result = noho_resolve(text, offensive_tokens, graph_storage, token_parser, nlp, num_options)
    return list(set(result))


def train_praphraser(texts, token_parser, graph_storage, nlp):
    for text in texts:
        print('Processing:', text)
        offensive_tokens = token_parser.get_offensive_tokens(text)
        if noho_train(text, offensive_tokens, token_parser, graph_storage, nlp):
            print('Persisting...')
            persist(graph_storage)
        else:
            print('Nothing to persist...')
