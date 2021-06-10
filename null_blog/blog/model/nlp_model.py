from joblib import load

from .preprocessing import TextTransformer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import os

# instanciate a transformer for preprocessing text
transformer = TextTransformer(stopwords=stopwords.words('english'), stemmer=PorterStemmer())

# unpacking the model
model_file_name = 'model.pkl'
path_to_model = os.path.join(os.getcwd(), f'blog\model\{model_file_name}')
model = load(path_to_model)

# function used in views to check if text content is offensive
def is_offensive(text):
    '''
        a wrapper function for transforming a piece of text and classifying it as offensive or not offensive
        @param text: string
            text used for evaluation
        @returns: integer (0 or 1)
            a prediction on the given text
    '''
    text = transformer.transform([text])

    return model.predict(text)
