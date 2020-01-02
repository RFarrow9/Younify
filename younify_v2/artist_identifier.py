from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import nltk
import string
import re
import pandas as pd
import spacy
from spacy.lang.en import English

""""Assume that we are using english dictionaries"""

nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
parser = English()
stopwords = stopwords.words('english')

punctuations = string.punctuation

STOPLIST = set(stopwords + list(ENGLISH_STOP_WORDS))
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "”"]


df = pd.read_csv("./resources/output_enriched.csv")

train, test = train_test_split(df, test_size=0.33, random_state=42)


# Define function to cleanup text by removing personal pronouns, stopwords, and punctuation
def cleanup_text(docs, logging=False):
    texts = []
    counter = 1
    for doc in docs:
        if counter % 1000 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))
        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])
        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
        tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
        tokens = ' '.join(tokens)
        texts.append(tokens)
    return pd.Series(texts)


def tokenizeText(sample):
    tokens = parser(sample)
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas
    tokens = [tok for tok in tokens if tok not in STOPLIST]
    tokens = [tok for tok in tokens if tok not in SYMBOLS]
    return tokens


def printNMostInformative(vectorizer, clf, N):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    topClass1 = coefs_with_fns[:N]
    topClass2 = coefs_with_fns[:-(N + 1):-1]
    print("Class 1 best: ")
    for feat in topClass1:
        print(feat)
    print("Class 2 best: ")
    for feat in topClass2:
        print(feat)


def cleanText(text):
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = text.lower()
    return text


class CleanTextTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return [cleanText(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}


if __name__ == "__main__":
    vectorizer = CountVectorizer(tokenizer=tokenizeText, ngram_range=(1,1))
    clf = LinearSVC()
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])

    # data
    train1 = train['Title'].tolist()
    labelsTrain1 = train['Conference'].tolist()

    test1 = test['Title'].tolist()
    labelsTest1 = test['Conference'].tolist()
    # train
    pipe.fit(train1, labelsTrain1)

    # test
    preds = pipe.predict(test1)
    print("accuracy:", accuracy_score(labelsTest1, preds))
    print("Top 10 features used to predict: ")

    printNMostInformative(vectorizer, clf, 10)

    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])
    transform = pipe.fit_transform(train1, labelsTrain1)
    vocab = vectorizer.get_feature_names()

    for i in range(len(train1)):
        s = ""
        indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i+1]]
        numOccurences = transform.data[transform.indptr[i]:transform.indptr[i+1]]
        for idx, num in zip(indexIntoVocab, numOccurences):
            s += str((vocab[idx], num))

            from sklearn import metrics

    print(metrics.classification_report(labelsTest1, preds, target_names=df['Conference'].unique()))