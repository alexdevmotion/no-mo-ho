from deoffensate_antonym import most_similar_spacy, filter_tokens_by_pos


def deoffensate_word_similarity_approach(text, token, nlp, token_parser):
    most_similar_words = most_similar_spacy(token.text, nlp, num_items=150)
    tokens = [nlp(word)[0] for word in most_similar_words]
    tokens_filtered_by_pos = filter_tokens_by_pos(tokens, [token.pos_])

    deoffensated_tokens = []
    remaining_offensive_tokens = None
    for replacement_token in tokens_filtered_by_pos:
        is_still, _remaining_offensive_tokens = is_still_offensive(text, token.text, replacement_token.text, token_parser)
        if not is_still:
            remaining_offensive_tokens = _remaining_offensive_tokens
            deoffensated_tokens.append(replacement_token)
            print(replacement_token.text, 'REPLACES', token.text)
            if len(deoffensated_tokens) > 15:
                break
    eliminated_lemma_clones = eliminate_lemma_clones(deoffensated_tokens)
    return [token.text for token in eliminated_lemma_clones], remaining_offensive_tokens


def is_still_offensive(original_text, token_text, replacement_text, token_parser):
    new_text = original_text.replace(token_text, replacement_text)
    new_offensive_tokens = token_parser.get_offensive_tokens(new_text)
    new_offesive_token_texts = [token.text for token in new_offensive_tokens]
    return replacement_text in new_offesive_token_texts, new_offensive_tokens


def eliminate_lemma_clones(token_list):
    unique_tokens = []
    unique_lemmas = []
    for token in token_list:
        if token.lemma_ in unique_lemmas:
            continue
        unique_lemmas.append(token.lemma_)
        unique_tokens.append(token)
    return unique_tokens
