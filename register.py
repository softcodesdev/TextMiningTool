from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from login import *
import mysql.connector as mc
import MySQLdb as mdb
class Ui_Register(object):

    def messagebox(self,title,message):
        msg=QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def InsertData(self):
        try:
            con = mdb.connect('localhost', 'root', '', 'christian_tool')
            with con:
                cur = con.cursor()

                data = cur.execute("INSERT INTO `users`( `username`, `password`, `fname`, `lname`)"
                            "VALUES('%s', '%s', '%s', '%s')" % (''.join(self.lineEdit.text()),
                                                    ''.join(self.lineEdit_2.text()),
                                                    ''.join(self.lineEdit_firstName.text()),
                                                    ''.join(self.lineEdit_lastName.text())))
            if(data):
                self.messagebox("Congraturations", "You Have Successfully Added A User!!")
                self.facultyedit.clear()

                QMessageBox.about(self, 'Connection', 'Data Inserted Successfully')
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Account created!")
                msgBox.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setInformativeText("Account created!")

        except mc.Error as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setInformativeText(e)

    def Backto_login(self):
        self.back_login = QtWidgets.QMainWindow()
        self.re = Ui_Login()
        self.re.setupUi(self.back_login)
        self.back_login.show()
        REGISTER.hide()

    def register_account(self):
        FirstNmae = self.lineEdit_firstName.text()
        Lname = self.lineEdit_lastName.text()
        department = self.choose_department.itemText()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()


    def setupUi(self, Frame):
        Frame.setObjectName("CREATE ACCOUNT")
        Frame.resize(628, 505)
        Frame.setFixedSize(628,505)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uploads/images/church.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Frame.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(190, 30, 361, 20))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: #FFFFFF;")
        self.label_re = QtWidgets.QLabel(Frame)
        self.label_re.setGeometry(QtCore.QRect(300, 90, 151, 31))
        self.label_re.setObjectName("label_re")
        self.label_re.setStyleSheet("color: #FFFFFF;")
        self.label_fname = QtWidgets.QLabel(Frame)
        self.label_fname.setGeometry(QtCore.QRect(120, 160, 101, 20))
        self.label_fname.setObjectName("label_fname")
        self.label_fname.setStyleSheet("color: #FFFFFF;")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(120, 210, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: #FFFFFF;")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(120, 270, 81, 21))
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: #FFFFFF;")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(120, 330, 61, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.setStyleSheet("color: #FFFFFF;")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(120, 390, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet("color: #FFFFFF;")
        self.lineEdit_firstName = QtWidgets.QLineEdit(Frame)
        self.lineEdit_firstName.setGeometry(QtCore.QRect(240, 160, 231, 31))
        self.lineEdit_firstName.setObjectName("lineEdit_firstName")
        self.lineEdit_firstName.setPlaceholderText("Please Enter Name")
        self.lineEdit_lastName = QtWidgets.QLineEdit(Frame)
        self.lineEdit_lastName.setGeometry(QtCore.QRect(240, 220, 231, 31))
        self.lineEdit_lastName.setObjectName("lineEdit_lastName")
        self.choose_department = QtWidgets.QComboBox(Frame)
        self.choose_department.setGeometry(QtCore.QRect(240, 270, 231, 41))
        # geek list
        departments = ["Editor", "Writer"]

        # adding list of items to combo box
        self.choose_department.addItems(departments)

        self.choose_department.setObjectName("choose_department")
        self.lineEdit = QtWidgets.QLineEdit(Frame)
        self.lineEdit.setGeometry(QtCore.QRect(240, 340, 231, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 390, 231, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_register = QtWidgets.QPushButton(Frame)
        self.pushButton_register.setGeometry(QtCore.QRect(370, 460, 121, 31))
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.clicked.connect(self.InsertData)
        self.label_6 = QtWidgets.QLabel(Frame)
        self.label_6.setGeometry(QtCore.QRect(26, 30, 141, 101))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("uploads/images/church_logo.png"))
        self.label_6.setObjectName("label_6")
        self.pushButton_back_tologin = QtWidgets.QPushButton(Frame)
        self.pushButton_back_tologin.setGeometry(QtCore.QRect(200, 460, 131, 31))
        self.pushButton_back_tologin.setObjectName("pushButton_back_tologin")
        self.pushButton_back_tologin.clicked.connect(self.Backto_login)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "CREATE ACCOUNT"))
        # label_re
        self.label.setText(_translate("Frame", "CHRISTIAN TEXT MINING TOOL"))
        self.label_re.setText(_translate("Frame", "CREATE ACCOUNT"))
        self.label_fname.setText(_translate("Frame", "First Name"))
        self.label_2.setText(_translate("Frame", "Last Name"))
        self.label_3.setText(_translate("Frame", "Department"))
        self.label_4.setText(_translate("Frame", "Username"))
        self.label_5.setText(_translate("Frame", "Password"))
        self.pushButton_register.setText(_translate("Frame", "REGISTER"))
        self.pushButton_back_tologin.setText(_translate("Frame", "Back to Login"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    REGISTER = QtWidgets.QMainWindow()
    REGISTER.setWindowTitle("REGISTER")
    ui = Ui_Register()

    ui.setupUi(REGISTER)
    REGISTER.show()
    sys.exit(app.exec_())