# Model taken from Medium article: https://towardsdatascience.com/how-to-build-a-fake-news-detection-web-app-using-flask-c0cfd1d9c2d4
# with data from:  https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn import metrics

import pickle
    
def main():

    true = pd.read_csv('model_training/True.csv')
    fake = pd.read_csv('model_training/Fake.csv')
    
    true['label'] = 1
    fake['label'] = 0

    frames = [true.loc[:5000][:], fake.loc[:5000][:]]
    data = pd.concat(frames)

    # Remove missing values
    data = data.dropna()
    data2 = data.copy()
    data2.reset_index(inplace=True)

    nltk.download('stopwords')
    ps = PorterStemmer()
    corpus = []

    for i in range(0, len(data2)):
        review = re.sub('[^a-zA-Z]', ' ', data2['text'][i])
        review = review.lower()
        review = review.split()

        review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        corpus.append(review)

    tfidf_v = TfidfVectorizer(max_features=5000, ngram_range=(1,3))
    x = tfidf_v.fit_transform(corpus).toarray()
    y = data2['label']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    classifier = PassiveAggressiveClassifier(max_iter=1000)
    classifier.fit(x_train, y_train)
    pred = classifier.predict(x_test)
    score = metrics.accuracy_score(y_test, pred)
    print("Accuracy: %0.3f" % score)

    # Tokenization
    review = re.sub('[^a-zA-Z]', ' ', fake['text'][13070])
    review = review.lower()
    review = review.split() 
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)# Vectorization
    val = tfidf_v.transform([review]).toarray()# Predict 
    classifier.predict(val)

    # Dump model and vectorizer
    pickle.dump(classifier, open('model2.pkl', 'wb'))
    pickle.dump(tfidf_v, open('tfidfvect2.pkl', 'wb'))

if __name__ == "__main__":
    main()