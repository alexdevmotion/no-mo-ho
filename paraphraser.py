import spacy

from deoffensate_antonym import deoffensate_word_antonym_approach

nlp = spacy.load('en_core_web_lg')


def noho_tokens(spacy_tokens):
    for spacy_token in spacy_tokens:
        deoffensated_word = deoffensate_word_antonym_approach(spacy_token, nlp)
        print(spacy_token.text, '<=>', deoffensated_word)
    return None


if __name__ == '__main__':
    blob = 'stupid bitch dickhead motherfucker imbecile retarded'
    tokens = nlp(blob)
    noho_tokens(tokens)
