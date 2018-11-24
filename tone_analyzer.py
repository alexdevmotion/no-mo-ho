import json
import yaml

from watson_developer_cloud import ToneAnalyzerV3

config = yaml.load(open('config.yaml', 'r'))
tone_analyzer_config = config['IBM_TONE_ANALYZER']

tone_analyzer = ToneAnalyzerV3(
    version=tone_analyzer_config['version'],
    url=tone_analyzer_config['url'],
    username=tone_analyzer_config['username'],
    password=tone_analyzer_config['password']
)

text = 'You are a stupid bitch'

tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json'
).get_result()
print(json.dumps(tone_analysis, indent=2))
