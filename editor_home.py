
from __future__ import division

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QVBoxLayout, QFileDialog
   
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
from results_display import *
import codecs
import re
import  collections
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
import matplotlib
from nltk.corpus import stopwords
class Ui_debugTextBrowser(object):
    def getfile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select file",
            "",
            "*.*", )
        file = open(fileName,'r')
        with file:
            text = file.read()
            self.textBrowser.setPlainText(text)
            self.lineEdit_selector_file.setText(fileName)

        return fileName



    def DataCleaningAndpreprocessing(self):
        # let create a bunch of sentences to clean
        warnings.filterwarnings('ignore')
        raw_docs = [self.typed_text.toPlainText()]
        #
       

        # Read data 

        with codecs.open("Catechism_of_the_Catholic_Church.txt", "r", encoding="utf-8") as f:
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
        make_df(je_counter.most_common(40), je_size)
        je_df = make_df(je_counter.most_common(40), je_size)
        je_df.to_csv("results.csv")

        wh_counter, wh_size = get_text_counter(saved_data)
        make_df(wh_counter.most_common(40), wh_size)
        # finding the most common words across the two documents.
        all_counter = wh_counter + je_counter
        all_df = make_df(wh_counter.most_common(40), 1)
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

    def checkresults(self):
        self.results_display = QtWidgets.QMainWindow()
        self.ui = Ui_RESULTS()
        self.ui.setupUi(self.results_display)
        self.results_display.setStyleSheet("QMainWindow{background:#660033;}")
        self.results_display.show()
        # HOME.hide()

    def EditorConfirmSelectedText(self):

       what_editor_has_confirmed = self.textBrowser.toPlainText()

       if(len(what_editor_has_confirmed)<1):
           print("No text to confirm")
       else:

           with open('user_selected_text.txt', 'w') as f:
               f.write(what_editor_has_confirmed)
           self.typed_text.clear()


    def setupUi(self, debugTextBrowser):
        debugTextBrowser.setObjectName("debugTextBrowser")
        debugTextBrowser.resize(745, 719)
        debugTextBrowser.setFixedSize(745, 719)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uploads/images/church.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        debugTextBrowser.setWindowIcon(icon)
        # self.textBrowser = QtWidgets.QTextBrowser(debugTextBrowser)
        self.textBrowser = QtWidgets.QPlainTextEdit(debugTextBrowser)
        self.textBrowser.setGeometry(QtCore.QRect(10, 500, 701, 171))
        self.textBrowser.setStyleSheet("font: 18pt \"Arial\";")
        # self.textBrowser.setDisabled(True)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(debugTextBrowser)
        self.label.setGeometry(QtCore.QRect(10, 20, 191, 91))
        self.label.setMinimumSize(QtCore.QSize(130, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Softcodes/Desktop/mary.png"))
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(debugTextBrowser)
        self.frame.setGeometry(QtCore.QRect(240, 10, 461, 62))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_selector_file = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_selector_file.setObjectName("lineEdit_selector_file")
        self.lineEdit_selector_file.setStyleSheet("font: 13pt \"Arial\";")
        self.lineEdit_selector_file.setDisabled(True)
        self.gridLayout.addWidget(self.lineEdit_selector_file, 1, 1, 1, 1)
        self.pushButton_choose_file = QtWidgets.QPushButton(self.frame)
        self.pushButton_choose_file.setStyleSheet("font: 18pt \"Arial\";")
        self.pushButton_choose_file.setObjectName("pushButton_choose_file")
        self.pushButton_choose_file.clicked.connect(self.getfile)
        self.gridLayout.addWidget(self.pushButton_choose_file, 1, 2, 1, 1)
        self.label_filename = QtWidgets.QLabel(self.frame)
        self.label_filename.setObjectName("label_filename")
        self.label_filename.setStyleSheet("color: #FFFFFF;")
        self.gridLayout.addWidget(self.label_filename, 1, 0, 1, 1)
        self.typed_text = QtWidgets.QPlainTextEdit(debugTextBrowser)
        self.typed_text.setGeometry(QtCore.QRect(10, 90, 701, 351))
        self.typed_text.setStyleSheet("font: 18pt \"Open Sans Regular\";")
        self.typed_text.setOverwriteMode(True)
        self.typed_text.setObjectName("typed_text")
        self.typed_text.setPlaceholderText("Enter text or Story to be analyzed!")
        self.typed_text.setObjectName("typed_text")
        self.widget = QtWidgets.QWidget(debugTextBrowser)
        self.widget.setGeometry(QtCore.QRect(10, 450, 626, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(468, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.analyebtn = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(16)
        self.analyebtn.setFont(font)
        # self.analyebtn.clicked.connect(self.Analyzedata)
        self.analyebtn.clicked.connect(self.DataCleaningAndpreprocessing)
        self.analyebtn.clicked.connect(self.checkresults)
        self.analyebtn.setObjectName("analyebtn")
        self.horizontalLayout.addWidget(self.analyebtn)

        self.pushButton_confirm_data_selected = QtWidgets.QPushButton(debugTextBrowser)
        self.pushButton_confirm_data_selected.setGeometry(QtCore.QRect(450, 682, 261, 31))
        self.pushButton_confirm_data_selected.clicked.connect(self.EditorConfirmSelectedText)
        self.pushButton_confirm_data_selected.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        self.pushButton_confirm_data_selected.setObjectName("pushButton_confirm_data_selected")

        self.retranslateUi(debugTextBrowser)
        QtCore.QMetaObject.connectSlotsByName(debugTextBrowser)
        debugTextBrowser.setTabOrder(self.lineEdit_selector_file, self.pushButton_choose_file)
        debugTextBrowser.setTabOrder(self.pushButton_choose_file, self.textBrowser)

    def retranslateUi(self, debugTextBrowser):
        _translate = QtCore.QCoreApplication.translate
        debugTextBrowser.setWindowTitle(_translate("debugTextBrowser", "CHRISTIAN TEXT MINING TOOL"))
        self.label.setText(_translate("debugTextBrowser", ""))
        self.pushButton_choose_file.setText(_translate("debugTextBrowser", "Browse File"))
        self.label_filename.setText(_translate("debugTextBrowser", "FILE NAME"))
        self.analyebtn.setText(_translate("debugTextBrowser", "SUBMIT DATA FOR ANALYSIS"))
        self.pushButton_confirm_data_selected.setText(_translate("debugTextBrowser", "Confirm Text selected"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HOME = QtWidgets.QMainWindow()
    ui = Ui_debugTextBrowser()
    HOME.setStyleSheet("QMainWindow{background:#660033;}")
    ui.setupUi(HOME)
    HOME.show()
    sys.exit(app.exec_())