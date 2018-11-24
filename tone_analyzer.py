import yaml

from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


class ToneAnalyzer:
    
    def __init__(self):
        self._setup_tone_analyzer()
        self._setup_nlu()

    def _setup_tone_analyzer(self):
        config = yaml.load(open('config.yaml', 'r'))
        tone_analyzer_config = config['IBM_TONE_ANALYZER']

        tone_analyzer = ToneAnalyzerV3(
            version=tone_analyzer_config['version'],
            url=tone_analyzer_config['url'],
            username=tone_analyzer_config['username'],
            password=tone_analyzer_config['password']
        )
        self.analyzer = tone_analyzer

    def _setup_nlu(self):
        config = yaml.load(open('config.yaml', 'r'))
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

    def get_emotions(self, text):
        nlu_analysis = self.understander.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(
                    emotion=True,
                    sentiment=True),
                keywords=KeywordsOptions(
                    emotion=True,
                    sentiment=True))).get_result()
        return nlu_analysis

    def is_good_emotion(self, emotion):
        emotion_type = emotion[0]
        emotion_value = emotion[1]
        if emotion_type == 'disgust' and emotion_value < .3:
            return False
        if emotion_type == 'anger' and emotion_value < .25:
            return False
        if emotion_type == 'sadness' and emotion_value < .5:
            return False
        return True
    
    def get_bad_words(self, text):
        emotions = self.get_emotions(text)
        emotions = emotions["keywords"]
        for token in emotions:
            token["emotion"] = sorted(token["emotion"].items(), key=lambda x: x[1], reverse=True)[0]
        
        return [(w["text"], w["emotion"][0], w["emotion"][1]) for w in emotions if self.is_good_emotion(w['emotion'])]


if __name__ == "__main__":
    text = "Yo nigga, what's up, get your nigga together, you whiny bitch."
    analyzer = ToneAnalyzer()
    
    print(analyzer.get_bad_words(text))
