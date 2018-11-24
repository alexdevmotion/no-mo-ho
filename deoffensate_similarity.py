from deoffensate_antonym import most_similar_spacy, filter_tokens_by_pos


def deoffensate_word_similarity_approach(token, nlp):
    most_similar_words = most_similar_spacy(token.text, nlp, num_items=500)
    tokens = [nlp(word)[0] for word in most_similar_words]
    filtered_by_pos = filter_tokens_by_pos(tokens, [token.pos_])
    pass