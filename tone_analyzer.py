import yaml

from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions

CONFIG_PATH = 'config_eugeniu.yaml'


class ToneAnalyzer:
    
    def __init__(self):
        self._setup_tone_analyzer()
        self._setup_nlu()

    def _setup_tone_analyzer(self):
        config = yaml.load(open(CONFIG_PATH, 'r'))
        tone_analyzer_config = config['IBM_TONE_ANALYZER']

        tone_analyzer = ToneAnalyzerV3(
            version=tone_analyzer_config['version'],
            url=tone_analyzer_config['url'],
            username=tone_analyzer_config['username'],
            password=tone_analyzer_config['password']
        )
        self.analyzer = tone_analyzer

    def _setup_nlu(self):
        config = yaml.load(open(CONFIG_PATH, 'r'))
        nlu_config = config['IBM_NLU']

        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=nlu_config['version'],
            iam_apikey=nlu_config['apikey'],
            url=nlu_config['url']
        )
        self.understander = natural_language_understanding

    def get_tone(self, text):
        return self.analyzer.tone(
            {'text': text},
            'application/json', content_language="en"
        ).get_result()

    def get_tone_score(self, text):
        main_tone = self.get_tone(text)
        if 'document_tone' not in main_tone:
            return .2
        document_tone = main_tone['document_tone']
        score = 0
        for tone in document_tone['tones']:
            if tone['tone_id'] in ['joy']:
                score += tone['score']
            elif tone['tone_id'] in ['fear', 'anger', 'disgust']:
                score += .1 * tone['score']
        return score

    def get_emotions(self, text):
        nlu_analysis = self.understander.analyze(
            text=text,
            features=Features(
                keywords=KeywordsOptions(
                    emotion=True,
                    sentiment=True))).get_result()
        return nlu_analysis

    def is_good_emotion(self, w):
        if w['emotion'] is not None:
            emotion_type, emotion_value = w['emotion']
            if emotion_type == 'disgust' and emotion_value > .3:
                return False
            if emotion_type == 'anger' and emotion_value > .3:
                return False
            if emotion_type == 'sadness' and emotion_value > .3:
                return False
        if w['sentiment'] is not None:
            sentiment_score, sentiment_type = w['sentiment']['score'], w['sentiment']['label']
            if sentiment_type == 'negative' and sentiment_score < -.7:
                return False
        return True
    
    def get_bad_words(self, text):
        emotions = self.get_emotions(text)
        emotions = emotions["keywords"]
        for token in emotions:
            token["emotion"] = sorted(token["emotion"].items(), key=lambda x: x[1], reverse=True)[0]
        
        return [(w["text"], w["emotion"], w['sentiment']) for w in emotions if not self.is_good_emotion(w)]


if __name__ == "__main__":
    text = "idiotic"
    analyzer = ToneAnalyzer()
    
    # print(analyzer.get_bad_words(text))
    print(analyzer.get_tone(text))
    print(analyzer.get_tone_score(text))
