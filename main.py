#!/usr/bin/python3
# -*- coding: UTF-8


# TODO подсветка фона записей с одной смены
import threading
# import time
# from pprint import pprint
import atexit
from datetime import datetime, timedelta
from PyQt5 import uic
from PyQt5.QtCore import QRegExp, Qt, QSortFilterProxyModel #, QAbstractItemModel, QAbstractTableModel, pyqtSlot, QSignalMapper, QPoint
from PyQt5.QtWidgets import QApplication, QTableView, QMessageBox, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QPushButton, QRadioButton, QMainWindow, QMenu, QSplashScreen, \
    QDesktopWidget, QLabel#, QWidget, QColorDialog
from PyQt5.QtGui import QPalette, QColor, QRegExpValidator, QIntValidator, QBrush, QImage, QPixmap, QStandardItemModel, QStandardItem, QFont, QIcon, QTextCursor, QMovie, QCloseEvent, QTextOption

'''from PyQt5 import QtWidgets'''

import db
import odata
from ui.extr_main import Ui_extrusion_window
from os import remove as rem, system
import simplejson as json
from settings import *
import calculations as calc
import telegram as tg


def cls():
    system('cls')


def readable_datetime(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return date
    return date.strftime('%d.%m.%Y %H:%M:%S')


def readable_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return date
    return date.strftime('%d.%m.%Y')


class Calculator(QDialog):
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/calc_.ui', self)
        self.setWindowTitle('Calc')
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.ui.lcd_display.document().setDefaultTextOption(QTextOption(Qt.AlignRight))
        self.ui.lcd_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.lcd_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()

    def keyPressEvent(self, e) -> None:
        txt = self.ui.lcd_display.toPlainText()
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            QDialog.keyPressEvent(self, e)
            if e.key() == Qt.Key_1:
                self.ui.lcd_display.insertPlainText('1')
            if e.key() == Qt.Key_2:
                self.ui.lcd_display.insertPlainText('2')
            if e.key() == Qt.Key_3:
                self.ui.lcd_display.insertPlainText('3')
            if e.key() == Qt.Key_4:
                self.ui.lcd_display.insertPlainText('4')
            if e.key() == Qt.Key_5:
                self.ui.lcd_display.insertPlainText('5')
            if e.key() == Qt.Key_6:
                self.ui.lcd_display.insertPlainText('6')
            if e.key() == Qt.Key_7:
                self.ui.lcd_display.insertPlainText('7')
            if e.key() == Qt.Key_8:
                self.ui.lcd_display.insertPlainText('8')
            if e.key() == Qt.Key_9:
                self.ui.lcd_display.insertPlainText('9')
            if e.key() == Qt.Key_0:
                self.ui.lcd_display.insertPlainText((txt + '0') if txt != '' and txt != '0' else txt)
            if e.key() == Qt.Key_Comma or e.key() == Qt.Key_Period and txt[-1] not in '+-×÷.,':
                self.ui.lcd_display.insertPlainText(',')
            if e.key() == Qt.Key_Plus and txt[-1] not in '+-×÷.,':
                self.ui.lcd_display.insertPlainText('+')
            if e.key() == Qt.Key_Minus and txt[-1] not in '+-×÷.,':
                self.ui.lcd_display.insertPlainText('-')
            if e.key() in (Qt.Key_division, Qt.Key_Slash) and txt[-1] not in '+-×÷.,':
                self.ui.lcd_display.insertPlainText('÷')
            if e.key() in (Qt.Key_multiply, Qt.Key_Asterisk) and txt[-1] not in '+-×÷.,':
                self.ui.lcd_display.insertPlainText('×')
            if e.key() in (Qt.Key_Backspace, Qt.Key_Delete):
                self.ui.lcd_display.textCursor().deletePreviousChar()
            if e.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.calculate_result()

    def calculate_result(self):
        res = self.ui.lcd_display.toPlainText().replace('×', '*').replace('÷', '/').replace(',', '.')
        print(res)
        # try:
        self.ui.lcd_display.setPlainText(str(eval(res)))
        # except:
        #     print('wrong string', res)








class CommentDialog(QDialog):
    def __init__(self, parent=None, order_no=None, title=None):
        super(CommentDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/comment_dialog.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.order_no = order_no
        data = db.get_order_comment(order_no)
        comment = data[0] + data[1]
        comment = comment.split('\\n')
        for line in comment:
            self.ui.textEdit.append(line)
        self.ui.checkBox.stateChanged.connect(self.checkbox_triggered)
        self.ui.pushButton.clicked.connect(self.ok_clicked)
        self.setWindowTitle(title)
        self.ui.label.setText(f'Комментарий к заказу {order_no}<br><b>{data[2]}</b><br>')
        self.show()

    def checkbox_triggered(self):
        self.ui.pushButton.setEnabled(self.ui.checkBox.isChecked())

    def ok_clicked(self):
        self.accept()
        self.close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.ui.checkBox.isChecked() == False:
            CommentDialog(self, self.order_no, 'Пожалуйста, ознакомьтесь!')
        else:
            self.accept()
            self.close()


class PosList(QDialog):
    def __init__(self, parent=None, order_no=None):
        super(PosList, self).__init__(parent)
        self.ui = uic.loadUi('ui/pos_list.ui', self)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        positions = db.get_order_positions(order_no)
        self.ui.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        header = self.ui.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(600, len(positions)*30+60)
        row = 0
        values = {}
        self.show()
        for pos in positions:
            meterage = calc.order_meterage(pos)
            cur_meterage = db.get_meterage(order_no, pos['name'])
            percentage = (cur_meterage/meterage)*100
            percentage = int(5 * round(float(percentage)/5))
            percentage = 100 if percentage > 100 else percentage
            gif = QMovie(f"ui/sector icons/{percentage}.gif")
            icon = QLabel()
            icon.setMovie(gif)
            # icon.setPixmap(QPixmap(f"ui/sector icons/{percentage}.png"))00 # no animation
            icon.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            values.update({row: percentage})
            self.ui.tableWidget.insertRow(row)
            self.ui.tableWidget.setCellWidget(row, 0, icon)
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(pos['name']))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(meterage)))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(cur_meterage)))
            gif.start()
            row += 1


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.ui = uic.loadUi("ui/splash.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        # self.movie = QMovie("ui/anim_logo1.gif")
        # self.ui.label.setMovie(self.movie)
        # self.movie.start()


    def start(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # self.movie.start()
        self.show()

    def stop(self):
        QApplication.restoreOverrideCursor()
        self.close()


class InfoMessage(QMessageBox):
    def __init__(self, parent=None, msg_text='', critical=False, title='Ошибка'):
        super(InfoMessage, self).__init__(parent)
        image = QImage()
        self.setWindowIcon(QIcon('icon.png'))
        image.load('ui/critical1.png' if critical else 'ui/info.png')
        pixmap = QPixmap(image).scaledToHeight(48, Qt.SmoothTransformation)
        self.setText(msg_text)
        self.setIconPixmap(pixmap)
        self.setFont(QFont('Amazon Ember Display', 10))
        self.setWindowTitle(title)
        self.show()
        self.exec_()


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.ui = uic.loadUi('ui/authorize.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        users = db.get_users()
        self.ui.comboBox.addItems([x[1] for x in users])
        self.setWindowIcon(QIcon('icon.png'))
        self.ui.password_field.setFocus()
        self.ui.login_button.clicked.connect(self.login)
        self.ui.exit_button.clicked.connect(self.exit)
        self.show()

    def login(self):
        user = self.ui.comboBox.currentText()
        password = self.ui.password_field.text()
        if db.login(user, password):
            self.accept()
        else:
            InfoMessage(self, 'Неверный пароль!', True)
            self.ui.password_field.clear()
            self.ui.password_field.setFocus()

    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self.login()

    def exit(self):
        exit()


class OptionsList(QDialog):
    def __init__(self, parent, options=None):
        super(OptionsList, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/options_list_dialog.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.cancel = False
        if options is not None:
            for option in options:
                radiobutton = QRadioButton(option, self)
                radiobutton.setFont(QFont('Amazon Ember Display', 10))
                radiobutton.setObjectName(f'radioButton_{options.index(option)}')
                radiobutton.toggled.connect(self.toggle)
                self.ui.verticalLayout.addWidget(radiobutton)
        ok_button = QPushButton('Ок')
        ok_button.setMinimumHeight(27)
        ok_button.setFont(QFont('Amazon Ember Display', 12))
        ok_button.setObjectName('pushButton')
        ok_button.clicked.connect(self.ok_clicked)
        self.ui.verticalLayout.addWidget(ok_button)
        self.adjustSize()
        self.setFixedSize(self.frameGeometry().width(), self.frameGeometry().height())
        self.show()

    def toggle(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            self.output = radiobutton.text()

    def ok_clicked(self):
        self.parent.ui.comment_textEdit.setText(self.output)
        self.parent.ui.comment_textEdit.moveCursor(QTextCursor.End)
        self.parent.ui.comment_textEdit.setFocus()
        self.close()


class OrderSearchDialog(QDialog):
    def __init__(self, parent, state=GIVEN_STATE):
        super(OrderSearchDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/order_search.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.ui.start_order_button.clicked.connect(self.ok_clicked)
        self.ui.cancel_button.clicked.connect(self.cancel_clicked)
        self.selected = None
        orders = dict(db.get_orders_by_state(state))
        # tableView w/filter -------------------------------------------------
        model = QStandardItemModel(len(orders), 2)
        model.setHorizontalHeaderLabels(['Номер', 'Наименование'])
        row = 0
        for x in orders.keys():
            no_ = QStandardItem(x)
            name_ = QStandardItem(orders[x])
            model.setItem(row, 0, no_)
            model.setItem(row, 1, name_)
            row += 1
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(-1)
        self.ui.tableView.setModel(filter_proxy_model)
        self.ui.lineEdit.textChanged.connect(filter_proxy_model.setFilterRegExp)
        # ---------------------------------------------------------------------
        self.ui.tableView.setFont(QFont('Amazon Ember Cd RC', 11))
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.setColumnWidth(0, 100)
        self.ui.tableView.clicked.connect(self.row_selected)
        self.show()

    def row_selected(self):
        self.selected = self.ui.tableView.selectedIndexes()[0].data()

    def cancel_clicked(self):
        self.reject()
        self.close()

    def ok_clicked(self):
        self.accept()
        self.close()


class NewOrderRequestDialog(QDialog):
    def __init__(self, parent, question=None, title=None):
        super(NewOrderRequestDialog, self).__init__(parent)
        self.parent = parent
        self.selected = None
        self.order_to_start = None
        self.ui = uic.loadUi('ui/question.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        if question is not None:
            self.ui.label.setText(question)
        if title is not None:
            self.ui.setWindowTitle(title)
        self.ui.ok_button.clicked.connect(self.ok_clicked)
        self.ui.cancel_button.clicked.connect(self.cancel_clicked)
        self.show()

    def ok_clicked(self):
        self.close()
        # TODO показать инф окно с итогами по заказу (а надо ли?)
        dialog = OrderSearchDialog(self, IN_WORK_STATE)
        if dialog.exec_() == QDialog.Accepted:
            self.order_to_start = dialog.selected
            self.accept()

    def cancel_clicked(self):
        self.reject()
        self.close()


class TextInputDialog(QDialog):
    def __init__(self, parent, window_title: str, mandatory_flag: bool, options=None):
        super(TextInputDialog, self).__init__(parent)
        self.parent = parent
        self.options = options
        self.mandatory_flag = mandatory_flag
        self.ui = uic.loadUi('ui/add_comment.ui', self)
        self.setWindowTitle(self.parent.ui.extr_tabs.tabText(self.parent.tab_id))
        self.ui.label.setText(window_title)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.ui.ok_pushButton.clicked.connect(self.ok_clicked)
        self.ui.cancel_pushButton.clicked.connect(self.cancel_clicked)
        if options is None:
            self.ui.toolButton.setVisible(False)
        else:
            self.ui.toolButton.setVisible(True)
            self.ui.toolButton.setEnabled(True)
            self.ui.toolButton.clicked.connect(self.show_options)
        self.new_comment = ''
        self.cancel = False
        self.show()

    def ok_clicked(self):
        if self.ui.comment_textEdit.toPlainText() == '' and not self.mandatory_flag:
            self.reject()
            self.close()
        elif self.ui.comment_textEdit.toPlainText() == '' and self.mandatory_flag:
            InfoMessage(self, 'Поле не может быть пустым', True, 'Ошибка')
            self.ui.comment_textEdit.setFocus()
            return
        else:
            self.new_comment = self.ui.comment_textEdit.toPlainText()
            self.cancel = False
            self.accept()
            self.close()

    def show_options(self):
        comment = OptionsList(self, self.options)

    def cancel_clicked(self):
        self.cancel = True
        self.reject()
        self.close()


class RollEnterWindow(QDialog):
    def __init__(self, parent):
        super(RollEnterWindow, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/roll_enter_dialog.ui', self)
        if DARK_THEME:
            self.setStyleSheet('QDialog{background-color: rgb(81,82,84);}')
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        weight_exp = QRegExp('[+-]?([0-9]*[.|,])?[0-9]+')
        try:
            self.order_no = self.parent.ui.extr_tabs.widget(self.parent.tab_id).order_no_label.text().split()[0]
            # self.order_no = js.get_order_no_by_tab_id(parent.tab_id)
        except KeyError:
            NewOrderRequestDialog(self, None, self.parent.ui.extr_tabs.tabText(self.tab_id))
            return
        self.position = self.parent.ui.extr_tabs.widget(self.parent.tab_id).order_name_label.text()
        self.author_name = parent.ui.worker_label.text()
        self.author_id = db.get_user_id_by_name(self.author_name)
        self.multi_order = db.is_multi_order(self.order_no)
        self.ui.position_comboBox.setLineEdit(self.ui.pos_lineEdit)
        if self.multi_order:
            self.ui.position_comboBox.setEnabled(True)  # активация выбора позиций
            self.ui.pos_lineEdit.setEnabled(True)
            self.ui.label_3.setEnabled(True)
            positions = [x[0] for x in db.get_position_names(self.order_no)]
            self.ui.position_comboBox.addItems(positions)
            self.ui.position_comboBox.setCurrentIndex(positions.index(self.parent.ui.extr_tabs.widget(self.parent.tab_id).name_comboBox.currentText()))
            # self.ui.pos_lineEdit.setText(self.parent.ui.extr_tabs.widget(self.parent.tab_id).name_comboBox.currentText())
            self.position = self.ui.position_comboBox.currentText()
        elif not self.multi_order:
            self.ui.position_comboBox.addItems([self.position, ''])
        self.ui.weight_lineEdit.setValidator(QRegExpValidator(weight_exp))
        self.ui.lenght_lineEdit.setValidator(QIntValidator())
        self.ui.waste_radioButton.toggled.connect(self.set_waste)
        self.ui.edge_radioButton.toggled.connect(self.set_waste)
        self.ui.scrap_radioButton.toggled.connect(self.set_waste)
        self.ui.weight_lineEdit.returnPressed.connect(self.weight_enter)
        self.ui.lenght_lineEdit.returnPressed.connect(self.lenght_enter)
        self.ui.pos_lineEdit.returnPressed.connect(self.pos_enter)
        self.ui.ok_button.clicked.connect(self.enter_roll)
        self.ui.quit_button.clicked.connect(self.quit)
        self.ui.waste_toolButton.clicked.connect(self.waste_defects_list)

    def weight_enter(self):
        if self.ui.weight_lineEdit.text() != '':
            self.roll_weight = float(self.ui.weight_lineEdit.text().replace(',', '.'))
            self.ui.lenght_lineEdit.setFocus()
            self.ui.weight_lineEdit.clearFocus()
            return self.roll_weight

    def lenght_enter(self):
        if self.ui.lenght_lineEdit.text() != '' and self.ui.weight_lineEdit.text() != '':
            self.roll_lenght = int(self.ui.lenght_lineEdit.text())
            if self.multi_order:
                self.ui.lenght_lineEdit.clearFocus()
                self.ui.pos_lineEdit.setFocus()
                self.ui.pos_lineEdit.selectAll()
                return self.roll_lenght
            else:
                self.ui.ok_button.setFocus()

    def pos_enter(self):
        self.position = self.ui.position_comboBox.currentText()
        self.ui.ok_button.setFocus()
        self.enter_roll()

    def set_waste(self):
        self.edge = self.ui.edge_radioButton.isChecked()
        self.scrap = self.ui.scrap_radioButton.isChecked()
        self.is_waste = self.ui.waste_radioButton.isChecked()
        if self.ui.waste_radioButton.isChecked():  # выбран БРАК
            self.ui.lenght_lineEdit.setEnabled(False)
            self.ui.label_2.setEnabled(False)
            self.ui.label_3.setEnabled(True if self.multi_order else False)
            self.ui.position_comboBox.setEnabled(True if self.multi_order else False)
            self.ui.comment_textEdit.setFocus()
            self.ui.add_control_checkbox.setEnabled(True)
            self.ui.waste_toolButton.setEnabled(True)
        elif self.ui.scrap_radioButton.isChecked():  # выбран ОБЛОЙ
            self.ui.lenght_lineEdit.setEnabled(False)
            self.ui.label_2.setEnabled(False)
            self.ui.label_3.setEnabled(True if self.multi_order else False)
            self.ui.position_comboBox.setEnabled(True if self.multi_order else False)
            self.ui.add_control_checkbox.setChecked(False)
            self.ui.add_control_checkbox.setEnabled(False)
            self.ui.waste_toolButton.setEnabled(True)
        elif self.ui.edge_radioButton.isChecked():  # выбрана КРОМКА
            self.ui.lenght_lineEdit.setEnabled(False)
            self.ui.label_2.setEnabled(False)
            self.ui.label_3.setEnabled(True if self.multi_order else False)
            self.ui.position_comboBox.setEnabled(True if self.multi_order else False)
            self.ui.add_control_checkbox.setChecked(False)
            self.ui.add_control_checkbox.setEnabled(False)
        else:
            self.ui.lenght_lineEdit.setEnabled(True)  # выбрана ПРОДУКЦИЯ
            self.ui.label_2.setEnabled(True)
            self.ui.add_control_checkbox.setEnabled(True)
            self.ui.label_3.setEnabled(self.multi_order)
            self.ui.position_comboBox.setEnabled(self.multi_order)
            self.ui.waste_toolButton.setEnabled(False)

    def read_form_fields(self):
        self.roll_weight = self.ui.weight_lineEdit.text().replace(',', '.')
        self.roll_lenght = self.ui.lenght_lineEdit.text()
        self.comment = self.ui.comment_textEdit.toPlainText()
        self.add_control = self.ui.add_control_checkbox.isChecked()
        self.is_waste = self.ui.waste_radioButton.isChecked()
        self.scrap = self.ui.scrap_radioButton.isChecked()
        self.edge = self.ui.edge_radioButton.isChecked()

    def enter_roll(self):
        self.read_form_fields()
        if not self.multi_order:
            if self.roll_lenght == '' and not self.is_waste and not self.scrap and not self.edge:
                InfoMessage(self, 'Введите метраж рулона', True)
                self.ui.lenght_lineEdit.setFocus()
                return
            if self.roll_weight == '':
                InfoMessage(self, 'Введите вес!', True)
                self.ui.weight_lineEdit.setFocus()
                return
        elif self.multi_order:
            if self.roll_lenght == '' and not self.is_waste and not self.scrap and not self.edge:
                InfoMessage(self, 'Введите метраж рулона', True)
                self.ui.lenght_lineEdit.setFocus()
                return
            if self.roll_weight == '':
                InfoMessage(self, 'Введите вес рулона')
                self.ui.weight_lineEdit.setFocus()
                return
        if self.is_waste or self.scrap:
            if len(self.comment) < 6:
                InfoMessage(self, 'Укажите причину брака', True)
                self.ui.comment_textEdit.setFocus()
                return
        if self.add_control:
            if len(self.comment) < 6:
                InfoMessage(self, 'Укажите причину необходимости дополнительного контроля', True)
                self.ui.comment_textEdit.setFocus()
                return
        self.write_roll()

    def waste_defects_list(self):
        popup = OptionsList(self, WASTE_REASONS_LIST)
        popup.show()

    def write_roll(self):
        self.read_form_fields()
        time = str(datetime.now().replace(microsecond=0))
        params = db.get_params_by_name(self.position)
        roll_lenght = int(self.roll_lenght if self.roll_lenght != '' else 0)
        roll_weight = float(self.roll_weight if self.roll_weight != '' else 0)
        if not self.is_waste and not self.edge and not self.scrap:
            self.deviation = calc.weight_deviation(params, roll_lenght, roll_weight)
        else:
            self.deviation = ''
        self.deviation = 0 if self.deviation == '' else float(self.deviation)
        if self.deviation <= WASTE_CUTOFF_MIN or self.deviation >= WASTE_CUTOFF_MAX:
            self.is_waste = True
            self.comment += '\n' if self.comment != '' else '' + f'Рулон вышел за пределы допусков {WASTE_CUTOFF_MIN} ... +{WASTE_CUTOFF_MAX} % и автоматически списан в брак.'
        mark = f"{'контроль' * self.add_control}{'брак' * self.is_waste}{'облой' * self.scrap}{'кромка' * self.edge}"
        # записываем рулон/брак в базу
        roll_dict = {'roll_id': 'ъъъ', 'order_no': self.order_no, 'position': self.position, 'lenght': roll_lenght, 'weight': roll_weight, 'is_waste': self.is_waste * 1,
                     'add_control': self.add_control * 1, 'extr_time': time, 'extr_author_id': self.author_id, 'comment': self.comment, 'flex_time': '',
                     'flex_author_id': '', 'cut_time': '', 'cut_author_id': '', 'chief_comment': '', 'deviation': self.deviation, 'is_edge': self.edge * 1,
                     'is_scrap': self.scrap * 1, 'extr_id': self.parent.tab_id, 'flex_id': 0, 'cut_id': 0, 'is_stop': 0, 'is_start': 0,
                     'shift_id':self.parent.shift_id}
        roll_id = db.add_roll(roll_dict)

        # выводим значения в таблицу
        row = self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.rowCount()
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.insertRow(row)
        deviation_ = QTableWidgetItem(str('{:+}'.format(self.deviation)))
        # проверка на допуски по весу и окраска отклонения в цвета
        if MIN_YELLOW[0] <= self.deviation <= MIN_YELLOW[1] or MAX_YELLOW[0] <= self.deviation <= MAX_YELLOW[1]:
            deviation_.setForeground(QBrush(QColor(158, 65, 4)))
        elif self.deviation > MAX_RED or self.deviation < MIN_RED:
            deviation_.setForeground(QBrush(QColor(158, 4, 4)))
        # вывод значений в таблицу
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 0, QTableWidgetItem(str(roll_id)))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 1, QTableWidgetItem(time))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 2, QTableWidgetItem(self.position if self.multi_order else ''))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 3, QTableWidgetItem(str(roll_weight) if roll_weight > 0 else ''))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 4, QTableWidgetItem(str(roll_lenght) if roll_lenght > 0 else ''))
        # ставим жирный шрифт при выходе за пределы желтой зоны
        font = QFont()
        bold = self.deviation <= MIN_YELLOW[1] or self.deviation >= MAX_YELLOW[1]
        font.setBold(bold)
        deviation_.setFont(font)
        mark_object = QTableWidgetItem(mark)
        mark_object.setForeground(QBrush(QColor(255, 170, 4)))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 5, QTableWidgetItem(deviation_ if self.deviation != 0 else ''))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 6, QTableWidgetItem(self.author_name))
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 7, mark_object)
        comment_obj = QTableWidgetItem(self.comment)
        if self.comment != '':
            comment_obj.setToolTip(self.comment)
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.setItem(row, 8, comment_obj)
        self.parent.ui.extr_tabs.widget(self.parent.tab_id).tableWidget.scrollToBottom()
        self.accept()
        self.close()
        # показываем коэффициенты релулировки шнека/вытяжки
        if abs(self.deviation) >= MAX_YELLOW[0]:
            if self.deviation < 0:
                screw_k = round(1 + abs(self.deviation) * 0.01, 4)
                drawing_k = round(1 - abs(self.deviation) * 0.01, 4)
            else:
                screw_k = round(1 - abs(self.deviation) * 0.01, 4)
                drawing_k = round(1 + abs(self.deviation) * 0.01, 4)
            InfoMessage(self, f'Вес рулона вышел за пределы допусков! ({MIN_YELLOW[1]} ... +{MAX_YELLOW[0]}%)\nНужна корректировка параметров.\n\nКоэффициент для:'
                              f'\n\nшнека = {screw_k}\nвытяжки = {drawing_k}', False, self.parent.ui.extr_tabs.tabText(self.parent.tab_id))
        if self.add_control:
            threading.Thread(tg.control_notification(roll_id)).start()
        if self.is_waste:
            pass # TODO сообщение в телегу о браке

    def quit(self):
        self.reject()
        self.close()


class RequestDialog(QDialog):
    def __init__(self, parent, question=None, title=None):
        super(RequestDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi('ui/question.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        if question is not None:
            self.ui.label.setText(question)
        if title is not None:
            self.ui.setWindowTitle(title)
        self.ui.ok_button.clicked.connect(self.ok_clicked)
        self.ui.cancel_button.clicked.connect(self.cancel_clicked)
        self.show()

    def ok_clicked(self):
        self.accept()
        self.close()

    def cancel_clicked(self):
        self.reject()
        self.close()


class NewRepairRequest(QDialog):
    def __init__(self, parent=None, worker_id=None, worker_role=None):
        super(NewRepairRequest, self).__init__(parent)
        self.worker_id = worker_id
        self.worker_role = worker_role
        self.ui = uic.loadUi('ui/repair_new_request.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.ui.ok_button.clicked.connect(self.submit_request)
        self.ui.priority_comboBox.addItems(REPAIR_PRIORITIES)
        self.ui.area_comboBox.addItems(REPAIR_AREAS)
        self.ui.area_comboBox.setCurrentIndex(self.worker_role)

    def submit_request(self):
        priority = self.ui.priority_comboBox.currentIndex()
        area = self.ui.area_comboBox.currentIndex()
        if self.ui.repair_item_lineEdit.text() == '':
            InfoMessage(msg_text='Укажите оборудование!', critical=True)
            return
        if self.ui.description_textEdit.toPlainText() == '':
            InfoMessage(msg_text='Опишите проблему!', critical=True)
            return
        repair_item = self.ui.repair_item_lineEdit.text()
        description = self.ui.description_textEdit.toPlainText()
        self.request_dict = {'state': 0, 'author_id': self.worker_id, 'area': int(area), 'repair_item': repair_item, 'description': description, 'priority': priority}
        self.accept()
        self.close()


class RepairServiceClient(QDialog):
    def __init__(self, worker_id, role):
        super(RepairServiceClient, self).__init__()
        self.worker_id = worker_id
        self.worker_role = role
        self.ui = uic.loadUi('ui/repair_service_client.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.setSelectionBehavior(QTableView.SelectRows)
        if DARK_THEME:
            self.setStyleSheet('QDialog{background-color: rgb(81,82,84);}')
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        vheader = self.ui.tableView.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        # tableView w/filter -------------------------------------------------
        self.requests = db.get_repair_requests()
        self.model = QStandardItemModel(0, 9)
        self.model.setHorizontalHeaderLabels(['Номер', 'Дата', "Срочность", "Автор", "Участок", "Оборудование", "Статус", "Обновлено", "Описание"])
        for req in self.requests:
            id = QStandardItem(str(req['request_id']))
            state = QStandardItem(REPAIR_STATES[req['state']])
            date = QStandardItem(readable_datetime(req['date_created']))
            author_id = QStandardItem(db.get_user_name_by_id(req['author_id']))
            area = QStandardItem(REPAIR_AREAS[req['area']])
            repair_item = QStandardItem(req['repair_item'])
            priority = QStandardItem(REPAIR_PRIORITIES[req['priority']])
            description = QStandardItem(req['description'])
            renewed = QStandardItem(req['date_renewed'])
            if req['priority'] == 0:
                priority.setForeground(QBrush(QColor(51, 204, 0)))
            if req['priority'] == 1:
                priority.setForeground(QBrush(QColor(204, 153, 51)))
            if req['priority'] == 2:
                priority.setForeground(QBrush(QColor(204, 0, 0)))
            self.model.appendRow([id, date, priority, author_id, area, repair_item, state, renewed, description])
        self.ui.new_request_button.clicked.connect(self.new_request)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self.ui.tableView.setModel(self.proxy)
        # self.ui.tableView.setSortingEnabled(True)
        self.ui.id_lineEdit.textChanged.connect(self.proxy.setFilterFixedString)
        # ---------------------------------------------------------------------
        self.ui.tableView.setColumnWidth(0, 60)
        self.ui.tableView.setColumnWidth(1, 140)
        self.ui.tableView.setColumnWidth(3, 120)
        self.ui.tableView.setColumnWidth(7, 140)
        self.ui.status_comboBox.addItems(REPAIR_STATES)
        self.ui.priority_comboBox.addItems(REPAIR_PRIORITIES)
        self.ui.author_comboBox.addItems([x[1] for x in db.get_users()])
        self.ui.area_comboBox.addItems(REPAIR_AREAS)
        self.ui.area_comboBox.setCurrentIndex(1+self.worker_role)
        self.show()


    def new_request(self):
        dialog = NewRepairRequest(self, self.worker_id, self.worker_role)
        if dialog.exec_() == QDialog.Accepted:
            request_id = db.submit_repair_request(dialog.request_dict)
            row = self.model.rowCount()
            # print(row)
            id = QStandardItem(str(request_id))
            state = QStandardItem(REPAIR_STATES[dialog.request_dict['state']])
            date = QStandardItem(readable_datetime(dialog.request_dict['date_created']))
            author_id = QStandardItem(db.get_user_name_by_id(dialog.request_dict['author_id']))
            area = QStandardItem(REPAIR_AREAS[dialog.request_dict['area']])
            repair_item = QStandardItem(dialog.request_dict['repair_item'])
            priority = QStandardItem(REPAIR_PRIORITIES[dialog.request_dict['priority']])
            if dialog.request_dict['priority'] == 0:
                priority.setForeground(QBrush(QColor(51, 204, 0)))
            if dialog.request_dict['priority'] == 1:
                priority.setForeground(QBrush(QColor(204, 153, 51)))
            if dialog.request_dict['priority'] == 2:
                priority.setForeground(QBrush(QColor(204, 0, 0)))
            renewed = QStandardItem('')
            description = QStandardItem(dialog.request_dict['description'])
            self.model.appendRow([id, date, priority, author_id, area, repair_item, state, renewed, description])


class ExtrusionWindow(QMainWindow):
    def __init__(self, parent=None, worker_id=None):
        super(ExtrusionWindow, self).__init__(parent)
        self.ui = Ui_extrusion_window()
        self.user_role = db.get_user_role(worker_id)
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # окно всегда поверх остальных
        self.worker_id = worker_id
        self.shift_id = None
        self.first_run = True
        index = -1
        extruders = db.get_extruders()
        extr_ids = db.get_extr_ids_list()
        if CONNECT_1C:
            busy_dict = db.get_busy_extrs_dict_1s()
        else:
            busy_dict = db.get_busy_extrs_dict(extr_ids)
        self.users = db.get_users_as_dict()
        for extruder in extruders:
            extr_tab = uic.loadUi('ui/extr_tab_.ui')
            if extruder[10]:
                tab_name = extruder[1] + ' (в ремонте)'
                index = self.ui.extr_tabs.addTab(extr_tab, tab_name)
                self.ui.extr_tabs.setTabEnabled(index, False)
            else:
                name = f'{extruder[1]} (остановлен)' if db.extr_is_idle(extruder[0]) else extruder[1]
                valid_tab = self.ui.extr_tabs.addTab(extr_tab, name)
                self.ui.extr_tabs.widget(valid_tab).tableWidget.customContextMenuRequested.connect(self.table_context)
                self.ui.extr_tabs.widget(valid_tab).roll_pushButton.clicked.connect(self.roll_enter_button_clicked)
                self.ui.extr_tabs.widget(valid_tab).stopstart_pushButton.clicked.connect(self.stopstart_button_clicked)
                self.ui.extr_tabs.widget(valid_tab).end_order_pushButton.clicked.connect(self.end_order_button_clicked)
                self.ui.extr_tabs.widget(valid_tab).comment_label.setAcceptRichText(True)
                self.ui.extr_tabs.widget(valid_tab).setEnabled(busy_dict[valid_tab])  # TODO баг с отключением вкладки
        self.ui.extr_tabs.currentChanged.connect(self.tab_change)
        self.ui.actionStartShift.triggered.connect(self.extr_shift_start)
        self.ui.actionEndShift.triggered.connect(self.extr_shift_end)
        self.ui.actionEndShift.setEnabled(False)
        self.ui.actionExit.triggered.connect(self.close_app)
        self.ui.actionRepairService.triggered.connect(self.repair_service)
        self.ui.worker_label.setText(username)
        self.current_order_no = None
        self.current_orders_data = {}
        self.ui.extr_tabs.setCurrentIndex(index + 1)
        self.tab_id = index + 1
        self.extr_get_state()
        self.extr_states = {}
        self.view_mode = True
        self.switch_view_mode(self.view_mode, False)
        self.stopstart_buttons_text()
        self.check_shift()
        self.show()
        sp.stop()
        self.update_productivity()

    def onHeaderClicked(self, logicalIndex):
        if logicalIndex == 1:
            print("клик по дате")

    def extr_shift_start(self):
        last_shift = db.extr_get_last_shift()
        if last_shift['end_time'] == '':
            dialog = RequestDialog(self, f'''Последняя смена от<br><b>{readable_date(last_shift["start_time"])} {db.get_user_name_by_id(last_shift['worker_id'])}</b><br>не была закрыта.<br>Закрыть смену и начать новую?<br>''', 'Закрытие смены')
            if dialog.exec_() == QDialog.Accepted:
                self.extr_shift_end(last_shift['shift_id'], popup=False)
                self.shift_id = db.extr_new_shift(self.worker_id, datetime.now().replace(microsecond=0))
                print(f'shift {self.shift_id} started')
                self.ui.actionStartShift.setEnabled(False)
                self.ui.actionEndShift.setEnabled(True)
                self.switch_view_mode(False, False)
        else:
            dialog = RequestDialog(self, 'Начать новую смену?\n', 'Открытие смены')
            if dialog.exec_() == QDialog.Accepted:
                self.extr_shift_end(last_shift['shift_id'], popup=False)
                self.shift_id = db.extr_new_shift(self.worker_id, datetime.now().replace(microsecond=0))
                print(f'shift {self.shift_id} started')
                self.ui.actionStartShift.setEnabled(False)
                self.ui.actionEndShift.setEnabled(True)
                self.switch_view_mode(False, False)
        self.ui.worker_label.setText(db.get_user_name_by_id(self.worker_id))
        self.ui.shift_no_label.setText(f'Смена № {self.shift_id}')
        self.update_summary()

    def extr_shift_end(self, shift_id, popup=True):
        if popup:
            dialog = RequestDialog(self, 'Закрыть смену и выйти?\n', 'Закрытие смены')
            if dialog.exec_() == QDialog.Accepted:
                if shift_id is False:
                    shift_id = self.shift_id
                self.switch_view_mode(True, True)
                db.extr_end_shift(shift_id, datetime.now().replace(microsecond=0))
                print(f'shift {shift_id} ended')
                threading.Thread(tg.extr_shift_output_notification(shift_id)).start()
                self.ui.actionStartShift.setEnabled(True)
                self.ui.actionEndShift.setEnabled(False)
                self.ui.worker_label.setText('')
                self.ui.total_output_label.setText('Выработка: 0 кг')
                self.ui.total_waste_label.setText('Брак: 0 кг')
                self.ui.shift_no_label.setText('Смена не начата')
                login = LoginWindow()
                if login.exec_() == QDialog.Accepted:
                    sp = SplashScreen()
                    sp.start()
                    if CONNECT_1C:
                        if REFILL_STATES:
                            odata.get_order_states(sp)
                        if REFILL_MEAS_UNITS:
                            odata.get_meas_units(sp)
                        if REFILL_PROPERTIES:
                            odata.get_properties_values(sp)
                        if REFILL_NOMENCLATURE:
                            odata.get_nomenclature(sp)
                        if REFILL_ORDERS:
                            odata.get_orders(sp)
                    sp.ui.splash_label.setText('Подготовка к запуску...')
                    QApplication.processEvents()
                    username = login.ui.comboBox.currentText()
                    # TODO здесь проверка на роль юзера и открытие соотвествующего его роли интерфейса
                    self.worker_id = db.get_user_id_by_name(username)
                    self.check_shift()
                    self.ui.worker_label.setText(username)
                    self.activateWindow()
                    sp.stop()
        if not popup:
            if shift_id is False:
                shift_id = self.shift_id
            self.switch_view_mode(True, True)
            db.extr_end_shift(shift_id, datetime.now().replace(microsecond=0))
            print(f'shift {shift_id} ended')
            threading.Thread(tg.extr_shift_output_notification(shift_id)).start()
            self.ui.actionStartShift.setEnabled(True)
            self.ui.actionEndShift.setEnabled(False)
            self.ui.worker_label.setText('')
            self.ui.total_output_label.setText('Выработка: 0 кг')
            self.ui.total_waste_label.setText('Брак: 0 кг')
            self.ui.shift_no_label.setText('Смена не начата')

    def update_current_orders_data(self, order, tab_id):
        # cls()
        data = {tab_id: order}
        self.current_orders_data.update(data)
        # print(self.current_orders_data[self.tab_id])

    def start_new_order(self, order_no):
        db.extr_shift_increase_readjustments(self.shift_id)
        if order_no is not None:
            self.current_order_no = order_no
            position = db.get_position_names(order_no)[0][0]
            self.ui.extr_tabs.widget(self.tab_id).tableWidget.setRowCount(0)
            if not CONNECT_1C:
                time = db.extr_get_start_time(order_no)
                if not time:
                    db.extr_start_order(order_no)
                db.extr_new_order_started(order_no, self.tab_id)
                self.fill_order_fields(order_no, position)
                self.extr_fill_table(order_no, self.tab_id)
                db.extr_update_current_order(order_no, self.tab_id)
            else:
                time = db.extr_get_start_time(order_no)
                if not time:
                    db.extr_start_order(order_no)
                key = db.get_order_key_by_no(order_no)
                self.fill_order_fields(self.tab_id, key)
                self.extr_fill_table(db.get_order_no_by_guid(key), self.tab_id)
                db.extr_update_current_order(key, self.tab_id)
            self.ui.extr_tabs.widget(self.tab_id).setEnabled(True)
            self.order_no = order_no
            CommentDialog(self, order_no, self.ui.extr_tabs.tabText(self.tab_id))
            # TODO здесь начатый заказ должен записаться в 1С (поле extr_id), так же меняются состояния заказов, нового на EXTRUSION_STATE, старого на FLEX_STATE/SEAL_STATE

    def tab_change(self):
        self.tab_id = self.ui.extr_tabs.currentIndex()
        try:
            self.current_order_no = self.ui.extr_tabs.widget(self.tab_id).order_no_label.text().split()[0]
        except IndexError:
            if not self.first_run and not self.view_mode:
                self.current_order_no = None
                dialog = NewOrderRequestDialog(self, None, self.ui.extr_tabs.tabText(self.tab_id))
                if dialog.exec_() == QDialog.Accepted:
                    self.start_new_order(dialog.order_to_start)

    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key_Enter and not self.view_mode and self.shift_id is not None or e.key() == Qt.Key_Return and not self.view_mode and self.shift_id is not None:
            if not db.extr_is_idle(self.tab_id):
                if self.current_order_no is not None:
                    roll_enter = RollEnterWindow(self)
                    roll_enter.show()
                    if roll_enter.exec_() == QDialog.Accepted:
                        order = self.current_orders_data[self.tab_id]
                        self.update_weight_meterage(order, self.tab_id, db.is_multi_order(order['order_no']))
                        db.extr_write_shift_summary(self.shift_id)
                else:
                    dialog = NewOrderRequestDialog(self, None, self.ui.extr_tabs.tabText(self.tab_id))
                    if dialog.exec_() == QDialog.Accepted:
                        db.extr_end_order(self.current_order_no)
                        self.start_new_order(dialog.output)
            else:
                dialog = RequestDialog(self, 'Подтвердите запуск!\n', self.ui.extr_tabs.tabText(self.tab_id))
                if dialog.exec_() == QDialog.Accepted:
                    self.start_extruder()

    def roll_enter_button_clicked(self):
        if self.current_order_no is not None and not self.view_mode:
            roll_enter = RollEnterWindow(self)
            roll_enter.show()
            if roll_enter.exec_() == QDialog.Accepted:
                order = self.current_orders_data[self.tab_id]
                self.update_weight_meterage(order, self.tab_id, db.is_multi_order(order['order_no']))
                db.extr_write_shift_summary(self.shift_id)
        else:
            dialog = NewOrderRequestDialog(self, None, self.ui.extr_tabs.tabText(self.tab_id))
            if dialog.exec_() == QDialog.Accepted:
                db.extr_end_order(self.current_order_no)
                self.start_new_order(dialog.output)

    def stopstart_buttons_text(self):
        extruders = db.get_extruders()
        for x in extruders:
            self.ui.extr_tabs.widget(x[0]).stopstart_pushButton.setText('Остановка' if x[11] == 0 else 'Запуск')
            self.extr_states.update({x[0]: x[11]})

    def stop_extruder(self, comment):
        db.extr_set_idle(self.tab_id, True)
        self.extr_states.update({self.tab_id: 1})
        self.ui.extr_tabs.widget(self.tab_id).stopstart_pushButton.setText('Запуск')
        time = str(datetime.now().replace(microsecond=0))
        # добавляем остановку в базу
        roll_id = db.extr_idle_start(self.current_orders_data[self.tab_id]['order_no'], self.current_orders_data[self.tab_id]['name'], time, self.worker_id,
                                     comment, self.tab_id, self.shift_id)
        # добавление строки в таблицу
        row = self.ui.extr_tabs.widget(self.tab_id).tableWidget.rowCount()
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.insertRow(row)
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 0, QTableWidgetItem(str(roll_id)))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 1, QTableWidgetItem(time))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 2, QTableWidgetItem(self.current_orders_data[self.tab_id]['name']))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 6, QTableWidgetItem(self.users[self.worker_id]))
        mark = QTableWidgetItem('остановка')
        mark.setForeground(QBrush(QColor(255, 170, 4)))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 7, QTableWidgetItem(mark))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 8, QTableWidgetItem(comment))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.scrollToBottom()
        new_text = self.ui.extr_tabs.tabText(self.tab_id) + ' (остановлен)'
        self.ui.extr_tabs.setTabText(self.tab_id, new_text)
        self.update_summary()

    def start_extruder(self):
        db.extr_set_idle(self.tab_id, False)
        self.extr_states.update({self.tab_id: 0})
        self.ui.extr_tabs.widget(self.tab_id).stopstart_pushButton.setText('Остановка')
        time = str(datetime.now().replace(microsecond=0))
        # добавляем остановку в базу
        roll_id = db.extr_idle_stop(self.current_orders_data[self.tab_id]['order_no'], self.current_orders_data[self.tab_id]['name'], time, self.worker_id,
                                    self.tab_id, self.shift_id)
        # добавление строки в таблицу
        row = self.ui.extr_tabs.widget(self.tab_id).tableWidget.rowCount()
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.insertRow(row)
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 0, QTableWidgetItem(str(roll_id)))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 1, QTableWidgetItem(time))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 2, QTableWidgetItem(self.current_orders_data[self.tab_id]['name']))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 6, QTableWidgetItem(self.users[self.worker_id]))
        mark = QTableWidgetItem('запуск')
        mark.setForeground(QBrush(QColor(255, 170, 4)))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row, 7, QTableWidgetItem(mark))
        self.ui.extr_tabs.widget(self.tab_id).tableWidget.scrollToBottom()
        self.update_idles(self.current_orders_data[self.tab_id]['order_no'], self.tab_id)
        new_text = db.get_extruder_name_by_id(self.tab_id)
        self.ui.extr_tabs.setTabText(self.tab_id, new_text)
        self.update_summary()

    def stopstart_button_clicked(self):
        current_state = self.extr_states[self.tab_id]
        if current_state == 0:
            dialog = TextInputDialog(self, 'Укажите причину остановки', True, STOPPAGE_REASONS_LIST)
            if dialog.exec_() == QDialog.Accepted:
                self.stop_extruder(dialog.new_comment)
        else:
            dialog = RequestDialog(self, question='Подтвердите запуск!\n', title=self.ui.extr_tabs.tabText(self.tab_id))
            if dialog.exec_() == QDialog.Accepted:
                self.start_extruder()

    def end_order_button_clicked(self):
        value = self.ui.extr_tabs.widget(self.tab_id).progressBar.value()
        if value >= 100:
            dialog = OrderSearchDialog(self, IN_WORK_STATE)
            if dialog.exec_() == QDialog.Accepted:
                new_order = dialog.selected
                db.extr_end_order(self.current_order_no)
                self.start_new_order(new_order)
        else:
            dialog = NewOrderRequestDialog(self, question=f"Заказ выполнен только на <font color=red><b>{value} %</b></font> от заявленного объема.<br>Уверены, что хотите закрыть заказ и начать новый?<br>",
                                           title=self.ui.extr_tabs.tabText(self.tab_id))
            if dialog.exec_() == QDialog.Accepted:
                new_order = dialog.order_to_start
                db.extr_end_order(self.current_order_no)
                self.start_new_order(new_order)

    def refill_multi_order_fields(self, order):
        id = self.tab_id
        # self.fill_order_fields(order['order_no'], order['name'])
        if isinstance(order['fold'], float):
            pass
        elif isinstance(order['fold'], str):
            order['fold'] = 0
        if order['fold'] != 0:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText(f"2 × {order['fold']}")
        else:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText('без фальцев')
        self.ui.extr_tabs.widget(id).hose_type_lineEdit.setText(order['hose_type'])
        self.ui.extr_tabs.widget(id).quantity_label.setText(f"<u>{order['quantity']} {order['meas_unit']}</u>")
        self.ui.extr_tabs.widget(id).width_lineEdit.setText(str("%g" % order['width']))
        if order['fold'] != 0 and order['fold'] is not None:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText(f"""2 × {"%g" % order['fold']}""")
        else:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText('без фальцев')
        self.ui.extr_tabs.widget(id).thickness_lineEdit.setText(str(order['thickness']))
        self.ui.extr_tabs.widget(id).color_lineEdit.setText(order['color'].lower())
        self.ui.extr_tabs.widget(id).color_lineEdit.setToolTip(order['color'].lower())
        self.ui.extr_tabs.widget(id).material_lineEdit.setText(order['material'])
        self.ui.extr_tabs.widget(id).corona_lineEdit.setText(order['corona'])
        self.ui.extr_tabs.widget(id).emboss_lineEdit.setText(order['emboss'])
        self.ui.extr_tabs.widget(id).weight_1m_lineEdit.setText(str(round(calc.weight_1m(order['width'], order['fold'], order['thickness'], order['density_factor']), 3)))
        self.ui.extr_tabs.widget(id).roll_lenght_lineEdit.setText(str(order['roll_lenght']) if order['roll_lenght'] else '[не указан]')
        if order['roll_lenght']:
            self.ui.extr_tabs.widget(id).roll_weight_lineEdit.setText(
                str(round(order['roll_lenght'] * calc.weight_1m(order['width'], order['fold'], order['thickness'], order['density_factor']) / 1000, 2)))
        else:
            self.ui.extr_tabs.widget(id).roll_weight_lineEdit.setText('0')
        self.update_weight_meterage(order, id, True)
        # комментарий
        self.ui.extr_tabs.widget(id).comment_label.setText('')
        comment = order['position_description'] + '\\n' + order['order_description']
        comment = comment.split('\\n')
        comment = list(filter(lambda x: len(x) > 0, comment))
        for line in comment:
            if line != '':
                self.ui.extr_tabs.widget(id).comment_label.append(line)
        self.ui.extr_tabs.widget(id).waste_lineEdit.setText(f'{db.get_waste(order["order_no"], order["name"])} / {db.get_scrap(order["order_no"], order["name"])}')
        self.ui.extr_tabs.widget(id).edge_lineEdit.setText(f'{db.get_scrap(order["order_no"], order["name"])} кг')
        self.ui.extr_tabs.widget(id).tableWidget.setSelectionBehavior(QTableView.SelectRows)

    def multi_order_changed(self):
        order_no = self.ui.extr_tabs.widget(self.tab_id).order_no_label.text().split()[0]
        new_pos = self.ui.extr_tabs.widget(self.tab_id).name_comboBox.currentText()
        params = db.get_order_params_by_no_and_name(order_no, new_pos)
        self.update_current_orders_data(params, self.tab_id)
        self.refill_multi_order_fields(params)

    def extr_get_state(self):
        if CONNECT_1C is False:
            with open("zakaz.json", "r", encoding='utf-8') as f:
                orders = json.load(f)
            db.write_orders(orders)
            repetition_list = []
            for order in db.get_extr_orders():
                if order[0] not in repetition_list:
                    self.fill_order_fields(order[0], order[1])
                    self.extr_fill_table(order[0], order[2])
                    repetition_list.append(order[0])
                    self.first_run = False
        else:
            for order in db.get_extr_orders_guids():
                if order[1]:
                    self.fill_order_fields(order[0], order[1])
                    self.extr_fill_table(db.get_order_no_by_guid(order[1]), order[0])
            self.first_run = False

    def switch_view_mode(self, state: bool, disable_all: bool):
        self.view_mode = state
        self.setWindowTitle("Экструзия (режим просмотра)" if state else 'Экструзия')
        ids = db.get_extr_ids_list()
        for id in ids:
            self.ui.extr_tabs.widget(id).setEnabled(not disable_all)
            self.ui.extr_tabs.widget(id).order_groupBox.setEnabled(not state)
            self.ui.extr_tabs.widget(id).film_params_groupBox.setEnabled(not state)
            self.ui.extr_tabs.widget(id).groupBox.setEnabled(not state)
            self.ui.extr_tabs.widget(id).roll_pushButton.setEnabled(not state)
            self.ui.extr_tabs.widget(id).mat_balance_pushButton.setEnabled(not state)
            self.ui.extr_tabs.widget(id).stopstart_pushButton.setEnabled(not state)
            self.ui.extr_tabs.widget(id).mat_request_pushButton.setEnabled(not state)
            self.ui.extr_tabs.widget(id).end_order_pushButton.setEnabled(not state)

    def extr_fill_table(self, order_no, id):
        rows = db.get_rolls_for_table(order_no)
        row = 0
        if rows:
            self.ui.extr_tabs.widget(id).tableWidget.setRowCount(0)
            for x in rows:
                deviation = x[15] if x[15] is not None else 0
                self.ui.extr_tabs.widget(id).tableWidget.insertRow(row)
                # вывод значений в таблицу
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 0, QTableWidgetItem(str(x[0])))  # roll_id
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 1, QTableWidgetItem(x[7]))  # date
                pos_object = QTableWidgetItem(x[2])
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 2, pos_object)  # position
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 3, QTableWidgetItem(str(x[4]) if x[4] is not None and x[4] > 0 else ''))  # lenght
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 4, QTableWidgetItem(str(x[3]) if x[3] is not None and x[3] > 0 else ''))  # weight
                # ставим жирный шрифт при выходе за пределы желтой зоны
                deviation_ = QTableWidgetItem(str('{:+}'.format(deviation)))
                # проверка на допуски по весу и окраска отклонения в цвета
                if MIN_YELLOW[0] <= deviation <= MIN_YELLOW[1] or MAX_YELLOW[0] <= deviation <= MAX_YELLOW[1]:
                    deviation_.setForeground(QBrush(QColor(158, 65, 4)))
                elif deviation > MAX_RED or deviation < MIN_RED:
                    deviation_.setForeground(QBrush(QColor(158, 4, 4)))
                font = QFont()
                bold = deviation <= MIN_YELLOW[1] or deviation >= MAX_YELLOW[1]
                font.setBold(bold)
                deviation_.setFont(font)
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 5, QTableWidgetItem(deviation_ if deviation != 0 else ''))
                # print(x[5], x[6], x[16], x[17], x[21], x[22])
                mark_object = QTableWidgetItem(f'{x[5] * "брак"}{x[6] * "контроль"}{x[16] * "кромка"}{x[17] * "облой"}{x[21]*"остановка"}{x[22]*"запуск"}')
                mark_object.setForeground(QBrush(QColor(255, 170, 4)))
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 7, mark_object)
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 6, QTableWidgetItem(self.users[x[8]]))
                comment = QTableWidgetItem(x[9])
                if x[9] != '':
                    comment.setToolTip(x[9])
                self.ui.extr_tabs.widget(id).tableWidget.setItem(row, 8, comment)
                row += 1
            self.ui.extr_tabs.widget(id).tableWidget.scrollToBottom()
        # else:
        #     stime = db.extr_get_start_time(order_no)
        #     if not stime:
        #         stime = db.extr_start_order(order_no)
        #         self.ui.extr_tabs.widget(id).start_time_lineEdit.setText(datetime.strftime(stime, '%d.%m.%Y %H:%M'))

    def update_idles(self, order_no, id):
        idle_time_order = db.extr_get_order_idle_time(order_no)
        idle_time_shift = db.extr_get_shift_idle_time(order_no, self.shift_id)
        self.ui.extr_tabs.widget(id).idle_time_all_lineEdit.setText(str(idle_time_order))
        self.ui.extr_tabs.widget(id).idle_time_shift_lineEdit.setText(str(idle_time_shift))

    def update_weight_meterage(self, order, id, multi_order=False):
        self.update_summary()
        self.update_idles(order['order_no'], id)
        current_meterage = db.get_meterage(order['order_no'], order['name'])
        current_meterage_total = db.get_total_meterage(order['order_no'])
        order_meterage = calc.order_meterage(order)
        order_weight = calc.order_weight(order)
        current_weight = db.get_weight(order['order_no'], order['name'])
        waste = db.get_waste(order['order_no'], order["name"])
        scrap = db.get_scrap(order['order_no'], order["name"])
        try:
            waste_percent = round((waste/(current_weight+waste+scrap))*100, 1)
        except ZeroDivisionError:
            waste_percent = 0
        self.ui.extr_tabs.widget(id).current_lenght_lineEdit.setText(f"{str(current_meterage)} из {str(order_meterage)} м")
        self.ui.extr_tabs.widget(id).current_weight_lineEdit.setText(f'{str(round(current_weight, 2))} из {str(int(order_weight))} кг')
        self.ui.extr_tabs.widget(id).waste_lineEdit.setText(f'{waste}/{scrap} ({"%g" % waste_percent} %)')
        self.ui.extr_tabs.widget(id).edge_lineEdit.setText(f'{db.get_edge(order["order_no"], order["name"])} кг')
        # update progressBar
        # TODO покрасить progressBar если value > 100
        if not multi_order:  # обработка singleorder
            meas_unit = order['meas_unit']
            if meas_unit == 'кг':
                value = ((current_weight / order_weight) * 100) if current_meterage != 0 else 0
            elif meas_unit == 'шт' or meas_unit == 'м' or meas_unit == 'пог.м':
                value = ((current_meterage / order_meterage) * 100) if current_meterage != 0 else 0
            # value1 = "QProgressBar::chunk {background: hsva(" + str(int(value)) + ", 255, 255, 60%);}"
            # self.ui.extr_tabs.widget(id).progressBar.setStyleSheet(value1);
            self.ui.extr_tabs.widget(id).progressBar.setValue(int(value if value <= 100 else 100))
            if value > 100:
                if not self.first_run:
                    title = self.ui.extr_tabs.tabText(self.tab_id)
                    dialog = NewOrderRequestDialog(self, f'Заказ закончен. Перекат составил {round(value-100, 1)} %\nЗакрыть заказ и начать новый?\n', title)
                    if dialog.exec_() == QDialog.Accepted:
                        db.extr_end_order(self.current_order_no)
                        self.start_new_order(dialog.order_to_start)
                        return
        else:  # обработка multiorder
            # TODO в мултиордере проверять попозиционно метраж/вес добавленного рулона, не полагаться на общий объем в progressBar
            multi_order_weight = calc.multi_order_weight(order['order_no'])
            multi_order_meterage = calc.multi_order_meterage(order['order_no'])
            meas_unit = order['meas_unit']
            if meas_unit == 'кг':
                value = ((current_weight / multi_order_weight) * 100) if current_meterage != 0 else 0
                self.ui.extr_tabs.widget(id).progressBar.setValue(int(value if value <= 100 else 100))
                return
            elif meas_unit == 'шт' or meas_unit == 'м' or meas_unit == 'пог.м':
                value = ((current_meterage_total / multi_order_meterage) * 100) if current_meterage_total != 0 else 0
                self.ui.extr_tabs.widget(id).progressBar.setValue(int(value if value <= 100 else 100))
                return

    def fill_order_fields(self, order_no, position):
        if CONNECT_1C:
            order = db.get_order_fields_1s(position)
            id = order_no
        else:
            order = db.get_order_fields(order_no, position)
            id = order['extr_id']
        self.tab_id = id
        self.current_order_no = order_no
        self.update_current_orders_data(order, id)
        width = float(order['width'])
        thickness = order['thickness']
        fold = order['fold']
        order_weight = round(order['quantity'] * order['weight_1_pc'] / 1000, 1)
        multi_order = db.is_multi_order(order['order_no'])
        self.ui.extr_tabs.widget(id).tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # макс 1 строка выбирается
        self.ui.extr_tabs.widget(id).tableWidget.setColumnHidden(0, False)  # скрываем roll_id
        self.ui.extr_tabs.widget(id).tableWidget.setColumnHidden(2, not multi_order)
        if not multi_order:
            self.ui.extr_tabs.widget(id).stackedWidget.setCurrentIndex(0)
            self.ui.extr_tabs.widget(id).order_name_label.setText(order['name'])
            self.ui.extr_tabs.widget(id).order_weight_label.setText(str(order_weight) + ' кг')
            self.ui.extr_tabs.widget(id).quantity_label.mousePressEvent = None
            self.ui.extr_tabs.widget(id).label_4.mousePressEvent = None
        else:
            self.ui.extr_tabs.widget(id).stackedWidget.setCurrentIndex(1)
            orders = [x[0] for x in db.get_position_names(order['order_no'])]
            self.ui.extr_tabs.widget(id).name_comboBox.clear()
            self.ui.extr_tabs.widget(id).name_comboBox.addItems(orders)
            self.ui.extr_tabs.widget(id).name_comboBox.setCurrentIndex(orders.index(order['name']))
            self.ui.extr_tabs.widget(id).name_comboBox.activated.connect(self.multi_order_changed)
            self.ui.extr_tabs.widget(id).quantity_label.mousePressEvent = self.show_pos_list
            self.ui.extr_tabs.widget(id).label_4.mousePressEvent = self.show_pos_list
            # считаем вес мультиордера
            multi_order_weight = calc.multi_order_weight(order['order_no'])
            self.ui.extr_tabs.widget(id).order_weight_label.setText(str(round(multi_order_weight, 2)))
        if isinstance(fold, float):
            pass
        elif isinstance(fold, str) or fold is None:
            fold = 0
        roll_lenght = order['roll_lenght'] if order['roll_lenght'] else '[не указана]'
        k = order['density_factor']
        self.ui.extr_tabs.widget(id).order_no_label.setText(f"{order['order_no']} от {readable_datetime(order['doc_date'])} ")
        self.ui.extr_tabs.widget(id).quantity_label.setText(f"{order['quantity']} {order['meas_unit']}" if not multi_order else
                                                            f"<u>{order['quantity']} {order['meas_unit']}</u>")
        self.ui.extr_tabs.widget(id).hose_type_lineEdit.setText(order['hose_type'])
        self.ui.extr_tabs.widget(id).hose_type_lineEdit.setToolTip(order['hose_type'])
        self.ui.extr_tabs.widget(id).width_lineEdit.setText(str("%g" % (width)))
        if fold != 0:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText(f"2 × {'%g' % fold}")
        else:
            self.ui.extr_tabs.widget(id).fold_lineEdit.setText('без фальцев')
        self.ui.extr_tabs.widget(id).thickness_lineEdit.setText(str(thickness))
        self.ui.extr_tabs.widget(id).color_lineEdit.setText(order['color'].lower())
        self.ui.extr_tabs.widget(id).color_lineEdit.setToolTip(order['color'].lower())
        self.ui.extr_tabs.widget(id).material_lineEdit.setText(order['material'])
        self.ui.extr_tabs.widget(id).corona_lineEdit.setText(order['corona'])
        self.ui.extr_tabs.widget(id).emboss_lineEdit.setText(order['emboss'])
        start_time = db.extr_get_start_time(order['order_no'])
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        self.ui.extr_tabs.widget(id).start_time_lineEdit.setText(readable_datetime(str(start_time)))
        avg_prod = db.extr_get_avg_prod(id)
        hrs = order_weight/avg_prod if not multi_order else multi_order_weight/avg_prod
        end_time = start_time + timedelta(hours=hrs)
        end_time = end_time.replace(microsecond=0)
        self.ui.extr_tabs.widget(id).end_time_lineEdit.setText(readable_datetime(str(end_time)))
        self.ui.extr_tabs.widget(id).weight_1m_lineEdit.setText(str(round(calc.weight_1m(width, fold, thickness, k), 3)))
        self.ui.extr_tabs.widget(id).roll_lenght_lineEdit.setText(str(roll_lenght))
        self.ui.extr_tabs.widget(id).roll_weight_lineEdit.setText(str(round(roll_lenght * calc.weight_1m(width, fold, thickness, k) / 1000, 2)))
        self.ui.extr_tabs.widget(id).tableWidget.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)  # обработка клика по шапке таблицы
        # скрываем Общий вес заказа, если заказ в кг
        if order['meas_unit'] == 'кг':
            self.ui.extr_tabs.widget(id).label_6.setVisible(False)
            self.ui.extr_tabs.widget(id).order_weight_label.setVisible(False)
        # обновляем метраж/вес
        self.update_weight_meterage(order, id, multi_order)
        # комментарий
        self.ui.extr_tabs.widget(id).comment_label.setText('')
        comment = order['position_description'] + '\\n' + order['order_description']
        comment = comment.split('\\n')
        for line in comment:
            self.ui.extr_tabs.widget(id).comment_label.append(line)
        self.ui.extr_tabs.widget(id).tableWidget.setSelectionBehavior(QTableView.SelectRows)  # выбор строки целиком при клике на нее
        # как определяется ширина колонок таблицы
        header = self.ui.extr_tabs.widget(id).tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)

    def table_context(self, pos):
        menu = QMenu()
        index = self.ui.extr_tabs.widget(self.tab_id).tableWidget.indexAt(pos)
        # print(index.row())
        # TODO index.row() возвращает None в режиме просмотра
        roll_id = self.ui.extr_tabs.widget(self.tab_id).tableWidget.item(index.row(), 0).text()
        worker = self.ui.extr_tabs.widget(self.tab_id).tableWidget.item(index.row(), 6).text()
        is_waste = db.is_roll_waste(roll_id)
        is_scrap = db.is_roll_scrap(roll_id)
        is_edge = db.is_roll_edge(roll_id)
        control = db.is_roll_control(roll_id)
        is_start = db.is_roll_idle_start(roll_id)
        is_stop = db.is_roll_idle_stop(roll_id)
        startstop = True if is_start or is_stop else False
        waste = not(not is_waste and not is_edge and not is_scrap)
        mark_control = None
        row_index = self.ui.extr_tabs.widget(self.tab_id).tableWidget.currentRow()
        # print(waste)
        if index.isValid() and self.worker_id == db.get_user_id_by_name(worker):  # проверка свой-чужой рулон
            # print('is start', is_start, 'is stop', is_stop, waste, mark_control)
            add_comment = menu.addAction('Добавить комментарий')
            if not waste and not startstop:
                mark_as_waste = menu.addAction('Отметить как брак')
            if not startstop and not control and not waste:
                mark_control = menu.addAction('Пометка доп. контроля')
            action = menu.exec_(self.ui.extr_tabs.widget(self.tab_id).tableWidget.viewport().mapToGlobal(pos))
            if action == add_comment:
                new_comment = self.extr_add_comment(roll_id)
                if new_comment is not False:
                    new_comment_object = QTableWidgetItem(new_comment)
                    new_comment_object.setToolTip(new_comment)
                    self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row_index, 8, new_comment_object)
                    return
                else:
                    return
            elif not startstop and not waste and action == mark_as_waste:
                new_comment = self.extr_mark_as_waste(roll_id)
                if new_comment is False:
                    return
                else:
                    mark_object = QTableWidgetItem('брак')
                    self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row_index, 7, mark_object)
                    new_comment_object = QTableWidgetItem(new_comment)
                    new_comment_object.setToolTip(new_comment)
                    self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row_index, 8, new_comment_object)
                    self.update_weight_meterage(self.current_orders_data[self.tab_id], self.tab_id)
            elif not startstop and not waste and control is False and action == mark_control:
                new_comment = self.add_control_mark(roll_id)
                if new_comment is False:
                    return
                else:
                    mark_object = QTableWidgetItem('контроль')
                    self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row_index, 7, mark_object)
                    new_comment_object = QTableWidgetItem(new_comment)
                    new_comment_object.setToolTip(new_comment)
                    self.ui.extr_tabs.widget(self.tab_id).tableWidget.setItem(row_index, 8, new_comment_object)

    def show_pos_list(self, event):
        order_no = self.current_order_no
        PosList(self, order_no)

    def add_control_mark(self, roll_id):
        old_comment = db.get_comment(roll_id)
        dialog = TextInputDialog(self, 'Укажите причину доп. контроля', True, CONTROL_REASONS_LIST)
        if dialog.exec_() == QDialog.Accepted:
            new_comment = dialog.new_comment
            time = datetime.now().strftime('%d.%m.%Y в %H:%M')
            if old_comment != '':
                final_comment = f'{old_comment}\n\n{self.users[self.worker_id]} поставил пометку доп. контроль {time}. Причина:\n{new_comment}'
            else:
                final_comment = f'{self.users[self.worker_id]} поставил пометку доп. контроль {time}. Причина:\n{new_comment}'
            db.add_control_mark(roll_id)
            db.update_comment(roll_id, final_comment)
            threading.Thread(tg.control_notification(roll_id)).start()
            return final_comment
        else:
            return False

    def extr_add_comment(self, roll_id):
        old_comment = (db.get_comment(roll_id))
        dialog = TextInputDialog(self, 'Введите комментарий', False)
        if dialog.exec_() == QDialog.Accepted:
            new_comment = dialog.new_comment
            time = datetime.now().strftime('%d.%m.%Y в %H:%M')
            if old_comment != '':
                final_comment = f'{old_comment}\n\n{self.users[self.worker_id]} добавил {time}:\n{new_comment}'
            else:
                final_comment = f'{self.users[self.worker_id]} добавил {time}\n{new_comment}'
            if new_comment != '':
                db.update_comment(roll_id, final_comment)
        else:
            return False
        return final_comment

    def extr_mark_as_waste(self, roll_id):
        old_comment = db.get_comment(roll_id)
        dialog = TextInputDialog(self, 'Укажите причину отбраковки', True, CONTROL_REASONS_LIST)
        if dialog.exec_() == QDialog.Accepted:
            new_comment = dialog.new_comment
            time = datetime.now().strftime('%d.%m.%Y в %H:%M')
            if old_comment != '':
                final_comment = f'{old_comment}\n\n{self.users[self.worker_id]} отметил рулон как брак {time}. Причина отбраковки:\n{new_comment}'
            else:
                final_comment = f'{self.users[self.worker_id]} отметил рулон как брак {time}. Причина отбраковки:\n{new_comment}'
            db.set_roll_as_waste(roll_id)
            db.update_comment(roll_id, final_comment)
            return final_comment
        else:
            return False

    def check_shift(self):
        last_shift = db.extr_get_last_shift()
        if self.worker_id == last_shift['worker_id'] and last_shift['end_time'] == '':
            self.shift_id = last_shift['shift_id']
            self.ui.shift_no_label.setText(f'Смена № {self.shift_id}')
            self.update_summary()
            self.switch_view_mode(False, False)
            self.ui.actionStartShift.setEnabled(False)
            self.ui.actionEndShift.setEnabled(True)
        else:
            self.shift_id = None
            self.ui.shift_no_label.setText(f'Смена не начата')
            self.switch_view_mode(True, False)
            self.ui.actionStartShift.setEnabled(True)
            self.ui.actionEndShift.setEnabled(False)

    def update_summary(self):
        self.update_productivity()
        summary = db.extr_get_shift_summary(self.shift_id)
        self.ui.total_output_label.setText(f'Выработка: {round(summary["weight"], 2)} кг')
        waste = summary['waste'] + summary['scrap']
        try:
            waste_percent = (waste / (summary['weight'] + waste)) * 100
        except ZeroDivisionError:
            waste_percent = 0
        self.ui.total_waste_label.setText(f'Брак: {round(waste, 2)} кг ({round(waste_percent, 2)} %)')
        idle_time_shift = db.extr_get_shift_idle_time(self.current_orders_data[self.tab_id]['order_no'], self.shift_id)
        self.ui.extr_tabs.widget(self.tab_id).idle_time_shift_lineEdit.setText(str(idle_time_shift))

    def update_productivity(self):  # TODO сделать обновление пр-сти спразу после открытия приложения
        shift_avg_prod = db.extr_shift_avg_output(self.shift_id, self.current_orders_data[self.tab_id]['order_no'])
        if shift_avg_prod:
            self.ui.extr_tabs.widget(self.tab_id).average_speed_lineEdit.setText(str(round(shift_avg_prod, 1))+' кг/ч')

    def repair_service(self):
        RepairServiceClient(self.worker_id, self.user_role)

    def close_app(self):
        if self.shift_id:
            dialog = RequestDialog(self, 'Закрыть смену и выйти из программы?', 'Выход')
            if dialog.exec_() == QDialog.Accepted:
                self.extr_shift_end(self.shift_id)
                sys.exit()
        else:
            sys.exit()


def clear_temp_files():
    try:
        rem('temp/current_orders.json')
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    import sys

    atexit.register(clear_temp_files)
    app = QApplication(sys.argv)
    if FUSION_THEME:
        app.setStyle('Fusion')
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(46, 47, 48))
    # dark_palette.setColor(QPalette.Window, QColor(81, 82, 84))
    dark_palette.setColor(QPalette.WindowText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Light, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Midlight, QColor(227, 227, 227))
    dark_palette.setColor(QPalette.Dark, QColor(64, 66, 68))
    dark_palette.setColor(QPalette.Mid, QColor(160, 160, 160))
    dark_palette.setColor(QPalette.Text, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 51, 51))
    dark_palette.setColor(QPalette.Button, QColor(64, 66, 68))
    dark_palette.setColor(QPalette.ButtonText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Base, QColor(46, 47, 48))
    dark_palette.setColor(QPalette.Shadow, QColor(105, 105, 105))
    dark_palette.setColor(QPalette.Highlight, QColor(10, 10, 10, 150))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Link, QColor(0, 122, 244))
    dark_palette.setColor(QPalette.LinkVisited, QColor(165, 122, 255))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 54, 55))
    dark_palette.setColor(QPalette.NoRole, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0, 102))
    dark_palette.setColor(QPalette.ToolTipText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Disabled, QPalette.Window, QColor(68, 68, 68, 255))
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(164, 166, 168, 96))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(164, 166, 168, 96))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(164, 166, 168, 96))
    dark_palette.setColor(QPalette.Disabled, QPalette.Base, QColor(68, 68, 68, 255))
    dark_palette.setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
    dark_palette.setCurrentColorGroup(QPalette.Normal)
    if DARK_THEME:
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #58595b; border: 1px solid grey; font-size: 10pt; font-family: Amazon Ember Display;}")
        app.setPalette(dark_palette)

    start = LoginWindow()

    if start.exec_() == QDialog.Accepted:
        sp = SplashScreen()
        sp.start()
        if CONNECT_1C:
            if REFILL_STATES:
                odata.get_order_states(sp)
            if REFILL_MEAS_UNITS:
                odata.get_meas_units(sp)
            if REFILL_PROPERTIES:
                odata.get_properties_values(sp)
            if REFILL_NOMENCLATURE:
                odata.get_nomenclature(sp)
            if REFILL_ORDERS:
                odata.get_orders(sp)
        sp.ui.splash_label.setText('Подготовка к запуску...')
        QApplication.processEvents()
        username = start.ui.comboBox.currentText()
        # TODO здесь проверка на роль юзера и открытие соотвествующего его роли интерфейса
        worker_id = db.get_user_id_by_name(username)
        # window = ExtrusionWindow(worker_id=worker_id)
        # Calculator()
        sys.exit(app.exec_())
