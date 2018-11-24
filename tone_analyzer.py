import yaml

from watson_developer_cloud import ToneAnalyzerV3

class ToneAnalyzer:
    
    def __init__(self):
        config = yaml.load(open('config.yaml', 'r'))
        tone_analyzer_config = config['IBM_TONE_ANALYZER']

        tone_analyzer = ToneAnalyzerV3(
            version=tone_analyzer_config['version'],
            url=tone_analyzer_config['url'],
            username=tone_analyzer_config['username'],
            password=tone_analyzer_config['password']
        )
        self.analyzer = tone_analyzer



    def analyze_tone(self, text):
        return self.analyzer.tone(
            {'text': text},
            'application/json'
        ).get_result()

if __name__ == "__main__":    
    analyzer = ToneAnalyzer()
    tone = analyzer.analyze_tone("Yo nigga, what's up, get your shit together bitch.")
    print(tone)
