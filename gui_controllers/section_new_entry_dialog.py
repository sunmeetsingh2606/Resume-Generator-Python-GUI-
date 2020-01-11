# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:10:09 2019

@author: sunmeet
"""

# gui controller for the section dialog window

# importing necessary modules
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5 import uic
from functools import partial
import json
import common

class SectionNewEntryDialog(QDialog):
    
    # class initializer
    def __init__(self, section_id, web_view, json_fields):
        super(SectionNewEntryDialog, self).__init__()    # call the inherited class __init__ method
        self.__gui_controller = common.get_guicontroller_instance()
        self.__save_content = False
        self.__section_id = section_id
        self.__web_view = web_view
        self.__json_fields = json_fields

        self.__temp_dict = {}
        
        self.__initUI()
        
    # initialize setup for the ui
    def __initUI(self):
        uic.loadUi("ui/section_dialog.ui", self)
        self.__web_view.page().runJavaScript("addListItem(\"{}\")".format(self.__section_id))
        
        self.__fields_container = self.findChild(QVBoxLayout, "valuesContainer")
        self.__done_button = self.findChild(QPushButton, "doneButton")
        self.__done_button.clicked.connect(self.__save_entry)
        self.__canel_button = self.findChild(QPushButton, "canelButton")
        self.__canel_button.clicked.connect(self.close)
        
        self.__generate_values_fields()
        
        self.exec()

    # override function for closing window
    def closeEvent(self, event):
        if (self.__save_content == False):
            self.__web_view.page().runJavaScript("removeListItem(\"{}\", \"{}\")".format(self.__section_id + ' .single-item', -1))
        
    # generate values fields according to json fields data
    def __generate_values_fields(self):
        stylesheet = """
            QLabel {
                color: white;
                font-size: 12px;
            }
            
            QLineEdit {
                border: none;
                background-color: white;
                border-radius: 5px;
                height: 15px;
                padding: 5px;
            }
            
            QPushButton {
                background: #74b9ff;
                color: white;
                height: 15px;
                padding: 5px 0px;
                border-radius: 5px;
            }
                
            QPushButton:hover {
                background: #41bee7;
            }

            QListWidget::item {
                background: #000;
            }
        """
        
        for key in self.__json_fields:
            self.__temp_dict[key] = ""

            label = QLabel(self.__json_fields[key]["placeholder"])
            label.setMaximumHeight(10)
            label.setStyleSheet(stylesheet)
            self.__fields_container.addWidget(label)
            
            if (self.__json_fields[key]["type"] == "text"):
                lineEdit = QLineEdit()
                lineEdit.setPlaceholderText(self.__json_fields[key]["placeholder"])
                lineEdit.setStyleSheet(stylesheet)
                lineEdit.textChanged.connect(partial(self.__text_changed, self.__section_id, key))
                self.__fields_container.addWidget(lineEdit)
            elif (self.__json_fields[key]["type"] == "array"):
                button = QPushButton("Change")
                button.setStyleSheet(stylesheet)
                self.__fields_container.addWidget(button)
                
        self.__fields_container.addStretch(1)

    def __save_entry(self):
        self.__save_content = True
        self.close()
        
    def __text_changed(self, field, json_key, value):
        self.__temp_dict[json_key] = value
        #self.__array[-1][json_key] = value
        #index = len(self.__array) - 1
        self.__web_view.page().runJavaScript("updateArray(\"{}\", \'{}\')".format(field, json.dumps(self.__temp_dict)))

    def get_array(self):
        if (self.__save_content):
            return self.__temp_dict
        
        
        
        
        
        
        