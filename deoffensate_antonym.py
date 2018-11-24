from nltk.corpus import wordnet


def get_synonyms_anytonyms_based_on_similarity(word, nlp):
    most_similar_words = most_similar_spacy(word, nlp)
    all_synonyms = []
    all_antonyms = []
    for similar_word in most_similar_words:
        synonyms, antonyms = get_synonyms_antonyms(similar_word)
        all_synonyms.extend(synonyms)
        all_antonyms.extend(antonyms)
    return set(all_synonyms), set(all_antonyms)


def most_similar_spacy(word, nlp, num_items=10):
    word = nlp.vocab[word]
    if not word:
        return []
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return [w.lower_ for w in by_similarity[:num_items]]


def get_synonyms_antonyms(word):
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            cur_antonyms = l.antonyms()
            if cur_antonyms:
                antonyms.extend([antonym.name() for antonym in cur_antonyms])
    return set(synonyms), set(antonyms)


def filter_tokens_by_pos(tokens, pos_arr):
    return [token for token in tokens if token.pos_ in pos_arr]


def deoffensate_word_antonym_approach(token, nlp):
    synonyms, antonyms = get_synonyms_anytonyms_based_on_similarity(token.text, nlp)
    if antonyms is None or len(antonyms) == 0:
        return None

    return filter_tokens_by_pos([nlp(doc)[0] for doc in antonyms], [token.pos_])
