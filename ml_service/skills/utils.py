import joblib
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class TextPreprocessor:

    @staticmethod
    # Preprocessing function
    def preprocess_text(text):
        # Lowercase the text
        text = text.lower()

        # Remove tabulation and punctuation
        text = re.sub('[^\w\s]', ' ', text)

        # Remove digits
        text = re.sub('\d+', '', text)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_text = [word for word in words if word not in stop_words]
        text = ' '.join(filtered_text)

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        words = word_tokenize(text)
        lemmatized_text = [lemmatizer.lemmatize(word) for word in words]
        text = ' '.join(lemmatized_text)

        return text