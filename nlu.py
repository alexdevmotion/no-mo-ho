import yaml

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

config = yaml.load(open('config.yaml', 'r'))
nlu_config = config['IBM_NLU']

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-24',
    iam_apikey=nlu_config['apikey'],
    url=nlu_config['url']
)


def do_nlu(text):
    nlu_analysis = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                emotion=True,
                sentiment=True,
                limit=2),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True,
                limit=2))).get_result()
    return nlu_analysis


do_nlu('Ariana is a stupid bitch')
