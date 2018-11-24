from paraphraser import train_praphraser
from tweet_search import TweetGenerator

# generator = TweetGenerator()
# tweets = generator.load_file()
# train_praphraser(tweets)
text = "Yo nigga, what's up, get your shit together, you whiny bitch."

train_praphraser([text])
