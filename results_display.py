
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat
from viewrelationship import*
class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parnet):
        super().__init__(parnet)
        self._highlight_lines = {}

    def highlight_line(self, line_num, fmt):
        if isinstance(line_num, float) and line_num >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line_num] = fmt
            block = self.document().findBlockByLineNumber(line_num)
            self.rehighlightBlock(block)

    def clear_highlight(self):
        self._highlight_lines = {}
        self.rehighlight()

    def highlightBlock(self, text):
        blockNumber = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(blockNumber)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)
   
class Ui_RESULTS(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uploads/images/church.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.model = QtGui.QStandardItemModel()
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 1180, 471))
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet("font: 18pt \"Arial\";")
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().resizeSection(0, 150)

        self.check_results = QtWidgets.QPushButton(self.centralwidget)
        self.check_results.setGeometry(QtCore.QRect(50, 500, 201, 31))
        self.check_results.setObjectName("check_results")
        self.check_results.setStyleSheet("font: 10pt \"Arial\";")
        self.check_results.clicked.connect(self.loadCsv)
        # added button
        self.view_relationship = QtWidgets.QPushButton(self.centralwidget)
        self.view_relationship.setGeometry(QtCore.QRect(530, 500, 141, 31))
        self.view_relationship.setObjectName("editview_relationship")
        self.view_relationship.setStyleSheet("font: 10pt \"Arial\";")
        self.view_relationship.clicked.connect(self.checkresultsbyknn)
        # just testing
        self.edit_results = QtWidgets.QPushButton(self.centralwidget)
        self.edit_results.setGeometry(QtCore.QRect(930, 500, 191, 31))
        self.edit_results.setObjectName("edit_results")
        self.edit_results.setStyleSheet("font: 10pt \"Arial\";")
        self.edit_results.clicked.connect(self.writeCsv)

        self.label_note = QtWidgets.QLabel(self.centralwidget)
        self.label_note.setGeometry(QtCore.QRect(260, 530, 651, 20))
        self.label_note.setStyleSheet("color: #2874A6;")
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_note.setFont(font)
        self.label_note.setTextFormat(QtCore.Qt.RichText)
        self.label_note.setWordWrap(True)
        self.label_note.setObjectName("label_note")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def checkresultsbyknn(self):
        self.reg_user = QtWidgets.QMainWindow()
        self.re = Ui_home()
        self.re.setupUi(self.reg_user)
        self.reg_user.setStyleSheet("QMainWindow{background:#660033;}")
        self.reg_user.show()

        ReSULTS.hide()
    def writeCsv(self, fileName):
        with open('related_info.csv', "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)
    def loadCsv(self):

        with open('related_info.csv', "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]

                self.model.appendRow(items)


    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CHRISTIAN TEXT MINING TOOL- ANALYSIS RESULTS"))
        self.check_results.setText(_translate("MainWindow", "VIEW ANALYZED CONTENT"))
        self.view_relationship.setText(_translate("MainWindow", "VIEW RELATIONSHIP"))
        self.edit_results.setText(_translate("MainWindow", "SAVE CHANGES"))
        
       
        self.label_note.setText(
            _translate("MainWindow", "Note: Related words or phrases have values greater than zero"))

if __name__ == "__main__":
    import sys


    def data(self, index, role):

        if role == Qt.ForegroundRole:
            value = self.tableView[index.row()][index.column()]

            if (
                    (isinstance(value, int) or isinstance(value, float))
                    and value > 0
            ):
                return QtGui.QColor('red')
    app = QtWidgets.QApplication(sys.argv)
    ReSULTS = QtWidgets.QMainWindow()
    ui = Ui_RESULTS()
    ReSULTS.setStyleSheet("QMainWindow{background:#660033;}")
    ui.setupUi(ReSULTS)
    ReSULTS.show()
    sys.exit(app.exec_())