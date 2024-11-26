import requests
import os
from newspaper import Article
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

default = 'https://arquivo.pt/textsearch?q='
election_time = '&from=20200203000000&to=20201103000000'
non_election_time = '&from=20180203000000&to=20181103000000'
pretty_print = "&prettyPrint=true&maxItems=500"

top_words = {}
top_trigrams = {}

forbidden_words = ['facebook', 'advertisement', 'said', 'told', 'asked', 'added', 'noted', 'explained', 
                   'stated', 'commented', 'wrote', 'tweeted', 'posted', 'announced', 'claimed', 'reported', 
                   'mentioned', 'argued', 'discussed', 'replied', 'suggested', 'warned', 'urged', 'emphasized', 
                   'pointed', 'expressed', 'noted', 'noting', 'may', 'one', 'would', 'also']


news_sites = ['&siteSearch=www.cbs.com', 
              '&siteSearch=www.nbc.com', 
              '&siteSearch=www.washingtonpost.com', 
              '&siteSearch=www.bbc.com',
              '&siteSearch=www.forbes.com',
              '&siteSearch=www.nytimes.com', 
              '&siteSearch=www.foxnews.com', 
              '&siteSearch=www.cnn.com']

def request_api(query, is_election, site):

    if query:

        if is_election == 1:
            response = requests.get(default + query + election_time + site +pretty_print)
            return response
        elif is_election == 0:
            response = requests.get(default + query + non_election_time + site + pretty_print)
            return response
    else:
        print("No query provided")
        return
    
input_query = input("Enter a query: ")
is_election = int(input("Is it election time? (1 for yes, 0 for no): "))

# if output.txt exists, delete it
if os.path.exists('output_election.txt'):
    os.remove('output_election.txt')
if os.path.exists('output_non_election.txt'):
    os.remove('output_non_election.txt')

for site in news_sites:
    response = request_api(input_query, is_election, site)
    response = response.json()
    
    for item in response['response_items']:
        html_link = item['originalURL']
        try:
            article = Article(html_link)
            article.download()
            article.parse()
        except:
            continue

        # Clean the article text
        # remove all non-alpabetical characters
        cleaned_text = ' '.join([word for word in article.text.split() if word.isalpha() and word.lower() not in stop_words])

        for word in cleaned_text.split():
            if word.lower() in forbidden_words:
                continue
            elif word.lower() in top_words:
                top_words[word.lower()] += 1
            else:
                top_words[word.lower()] = 1
        
        trigrams = [cleaned_text.split()[i:i+3] for i in range(len(cleaned_text.split())-2)]
        for trigram in trigrams:
            trigram = ' '.join(trigram)
            if trigram in top_trigrams:
                top_trigrams[trigram] += 1
            else:
                top_trigrams[trigram] = 1

# Plot top_words and top_trigrams
top_words = dict(sorted(top_words.items(), key=lambda item: item[1], reverse=True))
top_trigrams = dict(sorted(top_trigrams.items(), key=lambda item: item[1], reverse=True))

plt.bar(range(10), list(top_words.values())[:10], align='center')
plt.xticks(range(10), list(top_words.keys())[:10])
plt.xticks(rotation=0)
plt.title('Top 10 words')
plt.show()

plt.bar(range(10), list(top_trigrams.values())[:10], align='center')
plt.xticks(range(10), list(top_trigrams.keys())[:10])
plt.xticks(rotation=15)
plt.title('Top 10 trigrams')
plt.show()