
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
nltk.download('genesis')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
genesis_ic = wn.ic(genesis, False, 0.0)

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from sklearn.metrics import roc_auc_score
class KNN_NLC_Classifer():
    def __init__(self, k=1, distance_type = 'path'):
        self.k = k
        self.distance_type = distance_type

    # This function is used for training
    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    # This function runs the K(1) nearest neighbour algorithm and
    # returns the label with closest match. 
    def predict(self, x_test):
        self.x_test = x_test
        y_predict = []

        for i in range(len(x_test)):
            max_sim = 0
            max_index = 0
            for j in range(self.x_train.shape[0]):
                temp = self.document_similarity(x_test[i], self.x_train[j])
                if temp > max_sim:
                    max_sim = temp
                    max_index = j
            y_predict.append(self.y_train[max_index])
        return y_predict
    def convert_tag(self, tag):
      
        tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
        try:
            return tag_dict[tag[0]]
        except KeyError:
            return None


    def doc_to_synsets(self, doc):
       
        tokens = word_tokenize(doc+' ')
        
        l = []
        tags = nltk.pos_tag([tokens[0] + ' ']) if len(tokens) == 1 else nltk.pos_tag(tokens)
        
        for token, tag in zip(tokens, tags):
            syntag = self.convert_tag(tag[1])
            syns = wn.synsets(token, syntag)
            if (len(syns) > 0):
                l.append(syns[0])
        return l
    def document_similarity(self,doc1, doc2):
          """Finds the symmetrical similarity between doc1 and doc2"""

          synsets1 = self.doc_to_synsets(doc1)
          synsets2 = self.doc_to_synsets(doc2)
          
          return (self.similarity_score(synsets1, synsets2) + self.similarity_score(synsets2, synsets1)) / 2

	
    
    FILENAME = "related_info.csv"          

    dataset = pd.read_csv(FILENAME, header = None)
    dataset.rename(columns = {0:'text', 1:'answer'}, inplace = True)
    dataset['output'] = np.where(dataset['answer'] == 'temperature', 1,0)
    Num_Words = dataset.shape[0]
    print(dataset.head())
    print("\nSize of input file is ", dataset.shape)
    import re
    nltk.download('stopwords')
    s = stopwords.words('english')
	#add additional stop words
    s.extend(['today', 'tomorrow', 'outside', 'out', 'there'])
    ps = nltk.wordnet.WordNetLemmatizer()
    for i in range(dataset.shape[0]):
	    review = re.sub('[^a-zA-Z]', ' ', dataset.loc[i,'text'])
	    review = review.lower()
	    review = review.split()
	    review = [ps.lemmatize(word) for word in review if not word in s]
	    review = ' '.join(review)
	    dataset.loc[i, 'text'] = review
    X_train = dataset['text']
    y_train = dataset['output']
    print("Below is the sample of training text after removing the stop words")
    print(dataset['text'][:10])
	
	# 4. Train the Classifier
    classifier = KNN_NLC_Classifer(k=1, distance_type='path')
    classifier.fit(X_train, y_train)
    final_test_list = ['will it rain', 'Is it hot outside?' , 'What is the expected high for today?' , 
	                   'Will it be foggy tomorrow?', 'Should I prepare for sleet?',
	                     'Will there be a storm today?', 'do we need to take umbrella today',
	                    'will it be wet tomorrow', 'is it humid tomorrow', 'what is the precipitation today',
	                    'is it freezing outside', 'is it cool outside', "are there strong winds outside",]
    test_corpus = []
    for i in range(len(final_test_list)):
	    review = re.sub('[^a-zA-Z]', ' ', final_test_list[i])
	    review = review.lower()
	    review = review.split()

	    review = [ps.lemmatize(word) for word in review if not word in s]
	    review = ' '.join(review)
	    test_corpus.append(review)
    y_pred_final = classifier.predict(test_corpus)
    output_df = pd.DataFrame(data = {'text': final_test_list, 'code': y_pred_final})
    output_df['answer'] = np.where(output_df['code']==1, 'Temperature','Conditions')
    print(output_df)