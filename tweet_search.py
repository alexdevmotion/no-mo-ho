from selenium import webdriver


class TweetGenerator:
    
    def __init__(self):
        self.default_search_terms = ["fuck+bitch", "shit+piece", "fag+stupid", "fuck+ass", "dick+head+face"]
        self.separator = "\n\n\n"

    def scrap_tweets(self, search_terms=None, file_name="tweets_v2.txt"):
        if search_terms is None:
            search_terms = self.default_search_terms

        driver = webdriver.Chrome("./chromedriver")

        with open(file_name, "w") as f:
            for search_term in search_terms:
                
                url = "https://twitter.com/search?q={}".format(search_term)
                driver.get(url)
                elems = driver.find_elements_by_css_selector(".tweet-text")
                for elem in elems:
                    f.write(elem.text + self.separator)

        driver.close()

    def load_file(self, file_name="tweets_v2.txt"):
        with open(file_name, 'r', encoding='utf-8') as f:
            all_tweets = f.read()
        all_tweets = all_tweets.split(self.separator)
        return [x for x in all_tweets if len(x.strip()) > 0]


if __name__ == "__main__":
    generator = TweetGenerator()
    tweets = generator.load_file()
    print(len(tweets))
