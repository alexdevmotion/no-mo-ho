import json
import yaml
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions, EntitiesOptions

config = yaml.load(open('config.yaml', 'r'))
nlu_config = config['IBM_NLU']

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-24',
    iam_apikey=nlu_config['apikey'],
    url=nlu_config['url']
)

response = natural_language_understanding.analyze(
    text='Drangea is a motherfucking corrupt motherfucker. Fuck him.',
    features=Features(entities=EntitiesOptions(sentiment=True, limit=1))).get_result()

print(json.dumps(response, indent=2))
