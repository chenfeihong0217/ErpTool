# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from common.interface import *
# from PyQt5.QtWidgets import QApplication, QMainWindow,QDockWidget

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(459, 285)
        DockWidget.setAutoFillBackground(False)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setGeometry(QtCore.QRect(-10, 73, 491, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(100, 20, 271, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.dockWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 100, 51, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.dockWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 90, 161, 131))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setCurrentText("")
        list2 = ["测试环境","预发环境"]
        self.comboBox_2.addItems(list2)
        # self.comboBox_2.currentIndexChanged.connect(self.currentText())
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.pushButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(160, 222, 131, 31))
        self.pushButton.setIconSize(QtCore.QSize(15, 15))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.buttonClicked)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "ERP"))
        self.label.setText(_translate("DockWidget", "爱上租后台管理辅助工具"))
        self.label_2.setText(_translate("DockWidget", "账号："))
        self.label_3.setText(_translate("DockWidget", "密码："))
        self.label_4.setText(_translate("DockWidget", "环境："))
        self.pushButton.setText(_translate("DockWidget", "安 全 登 录"))


    def buttonClicked(self):
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()
        environment = self.comboBox_2.currentText()
        print("账号为:%s，密码为:%s，环境为:%s" % (account,password,environment))
        print(environment)
        if environment =="测试环境":
            host_set("test")
            set_conf("loginUser",user=account)
            set_conf("loginUser",pwd=password)
            resule = get_cookie()
            print(resule)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


