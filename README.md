# Detecting Fake News during US Election Cycles

## Authors
Daniel Pedrinho Nº107378\
Salomé Dias Nº118163

## Abstract
The objective of this project is to mine a dataset of news articles from arquivo.pt, analyse it and classify it as either fake news or not.

## Model Information
Model used was a **Passive-Aggressive Classifier**, which was taken from the article referenced in model.py, with an accuracy of 0.998.
After the training, the model was fed with the news articles from the data training set which had not been used.

## Results 
### Top 10 words

During election cycles
![Top 10 words](images\words_during.png)

Outside of election cycles
![Top 10 words](images\words_outside.png)

## Top 10 Trigrams

During election cycles
![Top 10 Trigrams](images\trigrams_during.png)

Outside of election cycles
![Top 10 Trigrams](images\trigrams_outside.png)

## Comparisons
During election cycle:\
Total news articles:  495\
Fake news articles:  118

Outside of election cycle:\
Total news articles:  316\
Fake news articles:  121

## References 
https://towardsdatascience.com/how-to-build-a-fake-news-detection-web-app-using-flask-c0cfd1d9c2d4