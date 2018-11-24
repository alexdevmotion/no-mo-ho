from deoffensate_antonym import most_similar_spacy, filter_tokens_by_pos


def deoffensate_word_similarity_approach(text, token, nlp, token_parser):
    most_similar_words = most_similar_spacy(token.text, nlp, num_items=150)
    tokens = [nlp(word)[0] for word in most_similar_words]
    tokens_filtered_by_pos = filter_tokens_by_pos(tokens, [token.pos_])

    deoffensated_words = []
    for replacement_token in tokens_filtered_by_pos:
        new_text = text.replace(token.text, replacement_token.text)
        new_offensive_tokens = token_parser.get_offensive_tokens(new_text)
        new_offesive_token_texts = [token.text for token in new_offensive_tokens]
        if replacement_token.text not in new_offesive_token_texts:
            deoffensated_words.append(replacement_token.text)
            print(replacement_token.text, 'REPLACES', token.text)
    return deoffensated_words
