# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extrusion_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1153, 714)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        self.order_groupBox = QtWidgets.QGroupBox(Form)
        self.order_groupBox.setGeometry(QtCore.QRect(10, 9, 1131, 101))
        self.order_groupBox.setObjectName("order_groupBox")
        self.label = QtWidgets.QLabel(self.order_groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.order_no_label = QtWidgets.QLabel(self.order_groupBox)
        self.order_no_label.setGeometry(QtCore.QRect(50, 20, 71, 16))
        self.order_no_label.setObjectName("order_no_label")
        self.label_2 = QtWidgets.QLabel(self.order_groupBox)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 21, 16))
        self.label_2.setObjectName("label_2")
        self.doc_date_label = QtWidgets.QLabel(self.order_groupBox)
        self.doc_date_label.setGeometry(QtCore.QRect(160, 20, 91, 16))
        self.doc_date_label.setObjectName("doc_date_label")
        self.label_3 = QtWidgets.QLabel(self.order_groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 44, 861, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.order_groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 81, 16))
        self.label_4.setObjectName("label_4")
        self.quantity_label = QtWidgets.QLabel(self.order_groupBox)
        self.quantity_label.setGeometry(QtCore.QRect(110, 70, 131, 16))
        self.quantity_label.setObjectName("quantity_label")
        self.label_6 = QtWidgets.QLabel(self.order_groupBox)
        self.label_6.setGeometry(QtCore.QRect(260, 70, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.order_groupBox)
        self.label_7.setGeometry(QtCore.QRect(340, 70, 121, 16))
        self.label_7.setObjectName("label_7")
        self.film_params_groupBox = QtWidgets.QGroupBox(Form)
        self.film_params_groupBox.setGeometry(QtCore.QRect(10, 120, 1131, 191))
        self.film_params_groupBox.setObjectName("film_params_groupBox")
        self.groupBox = QtWidgets.QGroupBox(self.film_params_groupBox)
        self.groupBox.setGeometry(QtCore.QRect(530, 10, 591, 171))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 571, 141))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.widget = QtWidgets.QWidget(self.film_params_groupBox)
        self.widget.setGeometry(QtCore.QRect(20, 30, 466, 138))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.width_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.width_lineEdit.setReadOnly(True)
        self.width_lineEdit.setObjectName("width_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.width_lineEdit)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.fold_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.fold_lineEdit.setReadOnly(True)
        self.fold_lineEdit.setObjectName("fold_lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fold_lineEdit)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.thickness_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.thickness_lineEdit.setReadOnly(True)
        self.thickness_lineEdit.setObjectName("thickness_lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.thickness_lineEdit)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.color_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.color_lineEdit.setReadOnly(True)
        self.color_lineEdit.setObjectName("color_lineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.color_lineEdit)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.emboss_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.emboss_lineEdit.setReadOnly(True)
        self.emboss_lineEdit.setObjectName("emboss_lineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.emboss_lineEdit)
        self.horizontalLayout.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.corona_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.corona_lineEdit.setReadOnly(True)
        self.corona_lineEdit.setObjectName("corona_lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.corona_lineEdit)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.weight_1m_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.weight_1m_lineEdit.setReadOnly(True)
        self.weight_1m_lineEdit.setObjectName("weight_1m_lineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.weight_1m_lineEdit)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.roll_lenght_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.roll_lenght_lineEdit.setReadOnly(True)
        self.roll_lenght_lineEdit.setObjectName("roll_lenght_lineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.roll_lenght_lineEdit)
        self.label_17 = QtWidgets.QLabel(self.widget)
        self.label_17.setObjectName("label_17")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.roll_weight_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.roll_weight_lineEdit.setReadOnly(True)
        self.roll_weight_lineEdit.setObjectName("roll_weight_lineEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.roll_weight_lineEdit)
        self.horizontalLayout.addLayout(self.formLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 320, 1131, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget2 = QtWidgets.QWidget(Form)
        self.widget2.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.order_groupBox.setTitle(_translate("Form", " Заказ "))
        self.label.setText(_translate("Form", "№"))
        self.order_no_label.setText(_translate("Form", "[order_no]"))
        self.label_2.setText(_translate("Form", "от"))
        self.doc_date_label.setText(_translate("Form", "[doc_date]"))
        self.label_3.setText(_translate("Form", "[name]"))
        self.label_4.setText(_translate("Form", "Количество:"))
        self.quantity_label.setText(_translate("Form", "[quantity + meas_unit]"))
        self.label_6.setText(_translate("Form", "Вес заказа:"))
        self.label_7.setText(_translate("Form", "[order_weight + кг]"))
        self.film_params_groupBox.setTitle(_translate("Form", " Характеристики рукава "))
        self.groupBox.setTitle(_translate("Form", " Комментарий к заказу "))
        self.label_5.setText(_translate("Form", "Ширина:"))
        self.width_lineEdit.setText(_translate("Form", "[width] + см"))
        self.label_9.setText(_translate("Form", "Фальцы:"))
        self.fold_lineEdit.setText(_translate("Form", "[fold]"))
        self.label_11.setText(_translate("Form", "Толщина:"))
        self.thickness_lineEdit.setText(_translate("Form", "[thickness] + мкм"))
        self.label_13.setText(_translate("Form", "Цвет пленки:"))
        self.color_lineEdit.setText(_translate("Form", "[color]"))
        self.label_10.setText(_translate("Form", "Тиснение:"))
        self.emboss_lineEdit.setText(_translate("Form", "[emboss]"))
        self.label_14.setText(_translate("Form", "Коронация:"))
        self.corona_lineEdit.setText(_translate("Form", "[corona]"))
        self.label_12.setText(_translate("Form", "Вес 1 метра:"))
        self.weight_1m_lineEdit.setText(_translate("Form", "[weight_1m] + г"))
        self.label_16.setText(_translate("Form", "Метраж рулона:"))
        self.roll_lenght_lineEdit.setText(_translate("Form", "[roll_lenght] + м"))
        self.label_17.setText(_translate("Form", "Вес рулона:"))
        self.roll_weight_lineEdit.setText(_translate("Form", "[roll_weight] + кг"))
