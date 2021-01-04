#Sentiment Analysis

from textblob import TextBlob
import nltk

# from newspaper import Article

from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

#First version
'''
url = 'https://www.everythingcomputerscience.com'
article = Article(url)

#Get the resources and tools
article.download()
article.parse()
nltk.download('punkt')

#for keyword extraction
article.nlp()

#Get summary of the article
summary = article.summary
print(summary)

#Create textblob object- applies nlp to text
tBlob = TextBlob(summary)

# -1(negative) <= sentiment <= 1 (postive)
sentiment = tBlob.sentiment.polarity

#Same as polarity
subj = tBlob.sentiment.subjectivity

print(sentiment)
'''

def Analyze(text):
    #Simple version, works completely fine without having to download anything else
    #   Purely using TextBlob
    
    tBlob = TextBlob(text)
    print('TextBlob said this: {}'.format(tBlob.sentiment.polarity))
    

    #Using nltk and sklearn

    #stop words are words like "is", "a"
    stopWords = stopwords.words('english')
    sentAnalyzer = SentimentIntensityAnalyzer()
    scores = sentAnalyzer.polarity_scores(text=text)
    print('Vader said this: {}'.format(scores['compound']))
    return (tBlob.sentiment.polarity, scores['compound'])

#Analyze('Not bad')