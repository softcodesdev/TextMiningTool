
from editor_home import*


from PyQt5 import QtCore, QtGui, QtWidgets

from register import *

import mysql.connector as mc
class Ui_Login(object):

    def UserRegistration(self):
        self.reg_user = QtWidgets.QMainWindow()
        self.re = Ui_Register()
        self.re.setupUi(self.reg_user)
        self.reg_user.setStyleSheet("QMainWindow{background:#660033;}")
        self.reg_user.show()

        LOGIN.hide()

    def login(self):
        try:
            Username = self.lineEdit_username.text()
            Pasword = self.lineEdit_password.text()
            print(Username)

            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="christian_tool"

            )

            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT username,password from users where username like '" + Username + "'and password like '" + Pasword + "'")
            result = mycursor.fetchone()

            if result == None:

                msgBox = QtWidgets.QMessageBox()

                msgBox.setWindowTitle("Failure ")
                msgBox.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setStyleSheet(
                    'QMessageBox {background-color: red; color: white;}')

                msgBox.setInformativeText("Please Enter correct UserName and Password?")
                msgBox.addButton(QtWidgets.QMessageBox.Ok)

                ret = msgBox.exec_()

                if ret == QtWidgets.QMessageBox.Ok:
                    self.lineEdit_username.clear()
                    self.lineEdit_username.setFocus()
                    self.lineEdit_username.setStyleSheet("color: rgb(255, 0, 0);")
                    self.lineEdit_username.setToolTip(" Enter Correct UserName ")
                    self.lineEdit_password.clear()
                    self.lineEdit_password.setToolTip(" Enter Correct Password ")
                    return
                else:
                    print("Oops! Something wrong")
                    return


            else:
                print("User Account  Found !")

                self.welcomeWindow = QtWidgets.QMainWindow()
                self.ui = Ui_debugTextBrowser()
                self.ui.setupUi(self.welcomeWindow)
                self.welcomeWindow.setStyleSheet("QMainWindow{background:#660033;}")
                msgBox1 = QtWidgets.QMessageBox()
                msgBox1.setWindowTitle("Login Success")
                msgBox1.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
                msgBox1.setIcon(QtWidgets.QMessageBox.Information)

                msgBox1.setInformativeText("Login Successful!")

                ret = msgBox1.exec_()

                self.welcomeWindow.show()
                LOGIN.hide()


        except mc.Error as e:

            msgBox2 = QtWidgets.QMessageBox()
            msgBox2.setWindowTitle("Database Failure")
            msgBox2.setWindowIcon(QtGui.QIcon('uploads/images/church.png'))
            msgBox2.setIcon(QtWidgets.QMessageBox.Information)

            msgBox2.setInformativeText("e")
            print(e)

    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(727, 521)
        font = QtGui.QFont()
        font.setBold(True)
        # font.setWeight(75)

        Login.setFixedSize(727,521)
        Login.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("uploads/images/church.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Login)
        self.label.setStyleSheet("color: #FFFFFF;")

        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(140, 30, 361, 20))
        self.label.setObjectName("label")
        self.label_login = QtWidgets.QLabel(Login)
        self.label_login.setStyleSheet("color: #FFFFFF;")
        self.label_login.setGeometry(QtCore.QRect(200, 90, 81, 21))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        self.label_login.setFont(font)
        self.label_login.setObjectName("label_login")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(50, 140, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: #FFFFFF;")
        self.label_password = QtWidgets.QLabel(Login)
        self.label_password.setGeometry(QtCore.QRect(50, 200, 61, 16))
        self.label_password.setObjectName("label_password")
        self.label_password.setStyleSheet("color: #FFFFFF;")
        self.lineEdit_username = QtWidgets.QLineEdit(Login)
        self.lineEdit_username.setGeometry(QtCore.QRect(130, 130, 181, 31))
        self.lineEdit_username.setPlaceholderText("")
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setPlaceholderText("Please enter Username")
        self.lineEdit_password = QtWidgets.QLineEdit(Login)
        self.lineEdit_password.setGeometry(QtCore.QRect(130, 200, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText("Enter password")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.pushButton = QtWidgets.QPushButton(Login)
        self.pushButton.setGeometry(QtCore.QRect(60, 270, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton.setFont(font)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.login)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Login)
        self.commandLinkButton.setGeometry(QtCore.QRect(190, 270, 181, 31))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.commandLinkButton.setStyleSheet("color: #FFFFFF;")
        self.frame = QtWidgets.QFrame(Login)
        self.frame.setGeometry(QtCore.QRect(389, 30, 311, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_image = QtWidgets.QLabel(self.frame)
        self.label_image.setGeometry(QtCore.QRect(0, -20, 311, 451))
        self.label_image.setText("")
        self.label_image.setPixmap(QtGui.QPixmap("uploads/images/mary.png"))
        self.label_image.setObjectName("label_image")
        self.pushButton_register = QtWidgets.QPushButton(Login)
        self.pushButton_register.setGeometry(QtCore.QRect(550, 440, 111, 23))
        self.pushButton_register.setObjectName("pushButton_register")
        self.pushButton_register.clicked.connect(self.UserRegistration)
        self.register_label = QtWidgets.QLabel(Login)
        self.register_label.setGeometry(QtCore.QRect(400, 440, 111, 20))
        self.register_label.setObjectName("register_label")
        self.register_label.setStyleSheet("color: #2874A6;")
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(15)
        self.register_label.setFont(font)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "LOGIN"))
        self.label.setText(_translate("Login", "CHRISTIAN TEXT MINING TOOL"))
        self.label_login.setText(_translate("Login", "LOGIN"))
        self.label_2.setText(_translate("Login", "UserName"))
        self.label_password.setText(_translate("Login", "Password"))
        self.lineEdit_username.setToolTip(_translate("Login", "Enter Username"))
        self.pushButton.setText(_translate("Login", "SIGN IN"))
        self.commandLinkButton.setText(_translate("Login", "Forgot Password"))
        self.pushButton_register.setText(_translate("Login", "REGISTER"))
        self.register_label.setText(_translate("Login", "New User"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LOGIN = QtWidgets.QMainWindow()
    ui = Ui_Login()
    LOGIN.setStyleSheet("QMainWindow{background:#660033;}")
    ui.setupUi(LOGIN)
    LOGIN.show()
    sys.exit(app.exec_())