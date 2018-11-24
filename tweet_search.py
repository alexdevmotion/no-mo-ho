from selenium import webdriver
from time import sleep

driver = webdriver.Chrome("./chromedriver")

search_terms = ["fuck+bitch", "shit+piece", "fag+stupid", "fuck+ass", "dick+head+face"]

with open("tweets_v2.txt", "w") as f:
    for search_term in search_terms:
        
        url = "https://twitter.com/search?q={}".format(search_term)
        driver.get(url)
        elems = driver.find_elements_by_css_selector(".tweet-text")
        for elem in elems:
            f.write(elem.text + "\n\n\n")

driver.close()
    