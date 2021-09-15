# -*- coding: utf-8 -*-
import sys
import json 
import xmltodict

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap,  QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from requests.models import Response

import simple_converter_layout

from cbr_api import api_request
import datetime


class MainApp(QMainWindow, simple_converter_layout.Ui_MainWindow):
    __slots__ = []
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Центробанк РФ")
        self.rub_result.setValidator( QDoubleValidator())
        self.euro_result.setValidator( QDoubleValidator())
        self.usd_result.setValidator( QDoubleValidator())
        self.zlt_result.setValidator( QDoubleValidator())
        self.rub_result.setText('0')
        self.euro_result.setText('0')
        self.usd_result.setText('0')
        self.zlt_result.setText('0')
        
        
        self.euro: float = None 
        self.usd:float = None 
        self.zlt:float = None 
        max_date = datetime.date.today()

        self.statusbar.showMessage("Валюты не загружены")
        self.request_btn.clicked.connect(self.request_cbr)
        self.calendarWidget.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.show()
        self.disable_converter_input(True)

        self.rub_result.textEdited.connect(self.input_rub)
        self.euro_result.textEdited.connect(self.input_eur)
        self.usd_result.textEdited.connect(self.input_usd)
        self.zlt_result.textEdited.connect(self.input_zlt)

    def input_rub(self, sender):

        s = sender.replace(",", '.')

        try:
            float_sender = float(s)
            self.euro_result.setText(str(round(float_sender / self.euro, 2)))
            self.usd_result.setText(str(round(float_sender / self.usd, 2)))
            self.zlt_result.setText(str(round(float_sender / self.zlt, 2)))
        except ValueError:
            self.euro_result.setText("0")
            self.usd_result.setText("0")
            self.zlt_result.setText("0")

        
    
    def input_eur(self, sender):
        s = sender.replace(",", '.')

        try:
            float_sender = float(s)
            float_rub = float_sender * self.euro
            self.rub_result.setText(str(round(float_rub, 2)))
            self.usd_result.setText(str(round(float_rub / self.usd, 2)))
            self.zlt_result.setText(str(round(float_rub / self.zlt, 2)))
        except ValueError:
            self.rub_result.setText("0")
            self.usd_result.setText("0")
            self.zlt_result.setText("0") 

    def input_usd(self, sender):
        s = sender.replace(",", '.')

        try:
            float_sender = float(s)
            float_rub = float_sender * self.usd
            self.rub_result.setText(str(round(float_rub, 2)))
            self.euro_result.setText(str(round(float_rub / self.euro, 2)))
            self.zlt_result.setText(str(round(float_rub / self.zlt, 2)))
        except ValueError:
            self.rub_result.setText("0")
            self.euro_result.setText("0")
            self.zlt_result.setText("0") 

    def input_zlt(self, sender):
        s = sender.replace(",", '.')

        try:
            float_sender = float(s)
            float_rub = float_sender * self.zlt
            self.rub_result.setText(str(round(float_rub, 2)))
            self.euro_result.setText(str(round(float_rub / self.euro, 2)))
            self.usd_result.setText(str(round(float_rub / self.usd, 2)))
        except ValueError:
            self.rub_result.setText("0")
            self.euro_result.setText("0")
            self.usd_result.setText("0")  
        
    def disable_converter_input(self, disable):
        self.rub_result.setReadOnly(disable)
        self.euro_result.setReadOnly(disable)
        self.usd_result.setReadOnly(disable)
        self.zlt_result.setReadOnly(disable)


    def is_loaded(self):
        return self.euro is not None and self.usd is not None 

    def set_currency(self, euro: float=None, usd: float =None, zlt:float=None):
        if euro:
            print(euro)
            self.euro = euro 
            self.lcd_euro.display(self.euro)
        if usd:
            print(usd)
            self.usd = usd
            self.lcd_usd.display(self.usd)
        if zlt:
            print(zlt)
            self.zlt = zlt
            self.lcd_zlt.display(self.zlt)

    def request_cbr(self):
        self.request_btn.hide()
        print ("Запрашиваем ЦБ РФ...")
        self.statusbar.showMessage("Запрашиваем ЦБ РФ...")
        dt = self.calendarWidget.selectedDate().toPyDate().strftime('%d/%m/%Y')
        print (dt)
        api_data = api_request(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={dt}")
        result = json.loads(json.dumps(xmltodict.parse(api_data)))

        for cur in result['ValCurs']['Valute']:

            if cur['NumCode'] == "978":
                self.set_currency(euro=float(cur['Value'].replace(",", '.')))

            if cur['NumCode'] == "985":
                self.set_currency(zlt=float(cur['Value'].replace(",", '.')))
            
            if cur['NumCode'] == "840":
                self.set_currency(usd=float(cur['Value'].replace(",", '.')))

        if self.is_loaded():
            self.statusbar.showMessage(f" На {dt} данные успешно загружены")
        
        self.request_btn.show()
        self.disable_converter_input(False)

        
        


app = QApplication(sys.argv)
window = MainApp()
sys.exit(app.exec_())