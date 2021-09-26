from __future__ import division

from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import warnings
import string
import nltk
# from  normalise import normalise
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
# below are imports for TF-IDF feature extraction

import codecs
import re
import  collections
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
import matplotlib
from nltk.corpus import stopwords
# end of imports

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat

# class SyntaxHighlighter(QSyntaxHighlighter):
#     def __init__(self, parnet):
#         super().__init__(parnet)
#         self._highlight_lines = {}
#
#     def highlight_line(self, line_num, fmt):
#         if isinstance(line_num, int) and line_num >= 0 and isinstance(fmt, QTextCharFormat):
#             self._highlight_lines[line_num] = fmt
#             block = self.document().findBlockByLineNumber(line_num)
#             self.rehighlightBlock(block)
#
#     def clear_highlight(self):
#         self._highlight_lines = {}
#         self.rehighlight()
#
#     def highlightBlock(self, text):
#         blockNumber = self.currentBlock().blockNumber()
#         fmt = self._highlight_lines.get(blockNumber)
#         if fmt is not None:
#             self.setFormat(0, len(text), fmt)
from results_display import *


class Ui_home(object):

    def DataCleaningAndpreprocessing(self):
        # let create a bunch of sentences to clean
        warnings.filterwarnings('ignore')
        raw_docs = [self.typed_text.toPlainText()]
        #
        # raw_docs = [doc.lower() for doc in raw_docs]
        # print(raw_docs)
        # # word tokenize
        #
        # tokenized_docs = [word_tokenize(doc) for doc in raw_docs]
        # print(tokenized_docs)
        # # sentence tokenization
        # sent_token = [sent_tokenize(doc) for doc in raw_docs]
        # print(sent_token)
        # regex = re.compile('[%s]' % re.escape(string.punctuation))
        # tokenized_docs_no_punctuation = []
        # for review in tokenized_docs:
        #     new_review = []
        #     for token in review:
        #         new_token = regex.sub(u'', token)
        #         if not new_token == u'':
        #             new_review.append(new_token)
        #     tokenized_docs_no_punctuation.append(new_review)
        #
        # print(tokenized_docs_no_punctuation)
        # tokenized_docs_no_stopwords = []
        # for doc in tokenized_docs_no_punctuation:
        #     new_term_vector = []
        #     for word in doc:
        #         if not word in stopwords.words('english'):
        #             tokenized_docs_no_stopwords.append(new_term_vector)
        # print(tokenized_docs_no_stopwords)
        #
        # porter = PorterStemmer()
        # wordnet = WordNetLemmatizer()
        # preprocessed_docs = []
        # for doc in tokenized_docs_no_punctuation:
        #     final_doc = []
        #     for word in doc:
        #         # final_doc.append(porter.stem(word))
        #          final_doc.append(wordnet.lemmatize(word))
        #     preprocessed_docs.append(final_doc)
        # print(preprocessed_docs)

        # Read data
        with codecs.open("dataset\Secret_teachings.txt", "r", encoding="utf-8") as f:
            user_data = f.read()
        # with codecs.open("user_entered_text.txt", "r", encoding="utf-8") as f:
        #     saved_data = f.read()
        saved_data= self.typed_text.toPlainText()
        print(saved_data)
        esw = stopwords.words('english')
        esw.append("would")
        word_pattern = re.compile("^\w+$")

        def get_text_counter(text):
            tokens = WordPunctTokenizer().tokenize(PorterStemmer().stem(text))
            tokens = list(map(lambda x: x.lower(), tokens))
            tokens = [token for token in tokens if re.match(word_pattern, token) and token not in esw]
            return collections.Counter(tokens), len(tokens)

        def make_df(counter, size):
            abs_freq = np.array([el[1] for el in counter])
            rel_freq = abs_freq / size
            index = [el[0] for el in counter]
            df = pd.DataFrame(data=np.array([abs_freq, rel_freq]).T, index=index,
                              columns=["Absolute frequency", "Relative frequency"])
            df.index.name = "Most Common words"
            return df

        je_counter, je_size = get_text_counter(user_data)
        make_df(je_counter.most_common(10), je_size)
        je_df = make_df(je_counter.most_common(1000), je_size)
        je_df.to_csv("USER_1000.csv")

        wh_counter, wh_size = get_text_counter(saved_data)
        make_df(wh_counter.most_common(10), wh_size)
        # finding the most common words across the two documents.
        all_counter = wh_counter + je_counter
        all_df = make_df(wh_counter.most_common(1000), 1)
        most_common_words = all_df.index.values

        #  create a data frame with the word frequency differences
        df_data = []
        for word in most_common_words:
            je_c = je_counter.get(word, 0) / je_size
            wh_c = wh_counter.get(word, 0) / wh_size
            d = abs(je_c - wh_c)
            df_data.append([je_c, wh_c, d])
        dist_df = pd.DataFrame(data=df_data, index=most_common_words,
                               columns=["Related_topics", "User entered relative frequency",
                                        "Relative frequency difference"])
        # dist_df.index.name = "Most common words"
        dist_df.sort_values("Relative frequency difference", ascending=False, inplace=True)
        print(dist_df.to_string())
        # print(dist_df.Related_topics)
        print(dist_df['Related_topics'])
        # exists = 0.000000 in dist_df.Related_topics
        # print(exists)
        available_result = dist_df['Related_topics'] > 0.0
        print(available_result)
        #     displaying the most distinctive words.

        dist_df.head()

        # then after we can save the list of distinctive words into a csv file.

        dist_df.to_csv("related_info.csv")
        print(
            "...................................Obtain values from CSV file ......................"
        )
        restults_cv = pd.read_csv("related_info.csv")















        # letus see whats in our dataset
        # names = ['Bad words','Class']
        # data = pd.read_csv("dataset/bad-words.csv",names=names)
        # data.head()
        # print(data.columns)
        # print(data.describe())
        # print(data.head())
        # new = data
        # user_input = preprocessed_docs
        # if new==user_input:
        #     print(True)
        # else:
        #     print(False)
        # X = data.iloc[:, :0].values
        # y = data.iloc[:, 4].values
        # # # To avoid over-fitting, we will divide our dataset into training and test splits, which gives us a better idea as to how our algorithm performed during the testing phase. This way our algorithm is tested on un-seen data, as it would be in a production application.
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        # scaler = StandardScaler()
        # scaler.fit(X_train)
        #
        # X_train = scaler.transform(X_train)
        # X_test = scaler.transform(X_test)
        # classifier = KNeighborsClassifier(n_neighbors=5)
        # classifier.fit(X_train, y_train)
        # y_pred = classifier.predict(X_test)
        # print(confusion_matrix(y_test, y_pred))
        # print(classification_report(y_test, y_pred))

    def checkresults(self):
        self.results_display = QtWidgets.QMainWindow()
        self.ui = Ui_RESULTS()
        self.ui.setupUi(self.results_display)
        self.results_display.setStyleSheet("QMainWindow{background:#660033;}")
        self.results_display.show()
        HOME.hide()

    def UserRfegistration(self):
       # we need to handle sentances that have commas?

       what_user_has_entered = self.typed_text.toPlainText()
       print(what_user_has_entered)
       if(len(what_user_has_entered)<1):
           print("No text Entered")
       else:
           with open('user_entered_text.csv','w' ,newline='') as f:
               words_to_be_saved = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
               words_to_be_saved.writerow([what_user_has_entered])
           self.typed_text.clear()



    def setupUi(self, home):
        home.setObjectName("home")
        home.resize(653, 653)
        home.setFixedSize(653,653)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uploads/images/church.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        home.setWindowIcon(icon)

        self.analyebtn = QtWidgets.QPushButton(home)
        self.analyebtn.setGeometry(QtCore.QRect(410, 600, 211, 51))
        self.analyebtn.setObjectName("analyebtn")
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(16)
        self.analyebtn.setFont(font)
        # self.analyebtn.clicked.connect(self.Analyzedata)
        self.analyebtn.clicked.connect(self.DataCleaningAndpreprocessing)
        self.analyebtn.clicked.connect(self.checkresults)
        self.typed_text = QtWidgets.QPlainTextEdit(home)
        self.typed_text.setGeometry(QtCore.QRect(30, 30, 601, 551))
        self.typed_text.setStyleSheet("font: 18pt \"Arial\";")
        self.typed_text.setOverwriteMode(True)
        self.typed_text.setObjectName("typed_text")
        self.typed_text.setPlaceholderText("Enter text")

        # self.typed_text.textChanged.connect(self.onTextChanged)
        # for i in range(1, 21):
        #     self.typed_text.appendPlainText('Line {0}'.format(i))
        #
        # self.highlighter = SyntaxHighlighter(self.typed_text.document())

        self.retranslateUi(home)
        QtCore.QMetaObject.connectSlotsByName(home)

    # def onTextChanged(self, text):
    #     fmt = QTextCharFormat()
    #     fmt.setBackground(QColor('yellow'))
    #
    #     self.highlighter.clear_highlight()
    #
    #     try:
    #         lineNumber = int(text) - 1
    #         self.highlighter.highlight_line(lineNumber, fmt)
    #     except ValueError:
    #         pass

    def retranslateUi(self, home):
        _translate = QtCore.QCoreApplication.translate
        home.setWindowTitle(_translate("home", "CHRISTIAN TEXT MINING TOOL"))
        self.analyebtn.setText(_translate("home", "ANALYZE CONTENT"))
        self.typed_text.setPlainText(_translate("home", ""))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HOME = QtWidgets.QMainWindow()
    ui = Ui_home()
    HOME.setStyleSheet("QMainWindow{background:#660033;}")
    ui.setupUi(HOME)
    HOME.show()
    sys.exit(app.exec_())