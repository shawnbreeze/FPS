# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extrusion_main_status.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_extrusion_window(object):
    def setupUi(self, extrusion_window):
        extrusion_window.setObjectName("extrusion_window")
        extrusion_window.resize(1280, 720)
        extrusion_window.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget(extrusion_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.extr_tabs = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.extr_tabs.setFont(font)
        self.extr_tabs.setObjectName("extr_tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.extr_tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.extr_tabs.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.extr_tabs)
        extrusion_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(extrusion_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 27))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menu.setFont(font)
        self.menu.setObjectName("menu")
        extrusion_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(extrusion_window)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        extrusion_window.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(extrusion_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.action.setFont(font)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(extrusion_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.action_2.setFont(font)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(extrusion_window)
        QtCore.QMetaObject.connectSlotsByName(extrusion_window)

    def retranslateUi(self, extrusion_window):
        _translate = QtCore.QCoreApplication.translate
        extrusion_window.setWindowTitle(_translate("extrusion_window", "MainWindow"))
        self.extr_tabs.setTabText(self.extr_tabs.indexOf(self.tab), _translate("extrusion_window", "Tab 1"))
        self.extr_tabs.setTabText(self.extr_tabs.indexOf(self.tab_2), _translate("extrusion_window", "Tab 2"))
        self.menu.setTitle(_translate("extrusion_window", "??????????"))
        self.action.setText(_translate("extrusion_window", "???????????? ??????????"))
        self.action_2.setText(_translate("extrusion_window", "?????????????????? ??????????"))
