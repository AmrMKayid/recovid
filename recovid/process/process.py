from recovid import *


def clean(text: str = ''):
  r"""
  Remove punctuations and special characters
  """
  text = text.lower()
  text = re.sub('\(|\)|:|,|;|\.|’|”|“|\?|%|>|<', '', text)
  text = re.sub('/', ' ', text)
  text = text.replace("'", '')
  return text


def tokenize(text: str = ''):
  r"""
  Tokenize into individual tokens
  """
  words = nltk.word_tokenize(text)
  english_stopwords = list(set(stopwords.words('english')))
  return list(
      set([
          word for word in words
          if len(word) > 1 and not word in english_stopwords and
          not (word.isnumeric() and len(word) != 4) and
          (not word.isnumeric() or word.isalpha())
      ]))


def lemmatize(word_list: list = [],
              lemmatizer: WordNetLemmatizer = WordNetLemmatizer()):
  # Init the Wordnet Lemmatizer
  lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
  return lemmatized_output


def preprocess(text: str = ''):
  text = clean(text)
  tokens = tokenize(text)
  lemmatizer = WordNetLemmatizer()
  tokens = lemmatize(tokens, lemmatizer)

  return tokens
