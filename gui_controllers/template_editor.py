# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:45:39 2019

@author: sunmeet
"""

# gui controller for the template editor window

# importing necessary modules
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QAction, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPainter, QImage
from PyQt5 import uic
from functools import partial
from PIL import Image
import json
import os
import common

class TemplateEditor(QMainWindow):
    
    # class initializer
    def __init__(self, template_folder):
        super(TemplateEditor, self).__init__()    # call the inherited class __init__ method
        self.__gui_controller = common.get_guicontroller_instance()
        self.__template_folder = template_folder
        self.__arrays = {}
        
        self.__load_values_file()
        
        self.__initUI()
        
    # initialize setup for the ui
    def __initUI(self):
        uic.loadUi("ui/template_editor.ui", self)
        
        self.__export_template_menu = self.findChild(QAction, "exportTemplate")
        self.__export_template_menu.triggered.connect(self.__export_template)
        
        self.__fields_container = self.findChild(QVBoxLayout, "valuesContainer")
        self.__web_view_container = self.findChild(QVBoxLayout, "webViewContainer")
        
        self.__web_view = QWebEngineView()
        self.__web_view.setAttribute(Qt.WA_DontShowOnScreen)
        self.__web_view.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        local_url = QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resume_templates/" + self.__template_folder + "/index.html")))
        self.__web_view.load(local_url)
        
        self.__web_view_container.addWidget(self.__web_view)
        
        self.__generate_values_fields()
        
        self.show()
        
    # function to load the values.json
    def __load_values_file(self):            
        read_values = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resume_templates/" + self.__template_folder + "/values.json")), "r")
        self.__data = json.load(read_values)
        read_values.close()
        
    def __write_values_file(self):
        write_values = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resume_templates/career/values.json")), "w")
        write_values.write(json.dumps(self.__data))
        write_values.close()
        
        #QTimer.singleShot(5000, self.test)

    def __web_view_snapshot(self, path):
        self.__web_view.grab().save(path, b'PNG')
        self.__export_pdf(path)
        
    def __export_png(self, path):
        size = self.__web_view.page().contentsSize().toSize()
        self.__web_view.resize(size)
        QTimer.singleShot(2000, partial(self.__web_view_snapshot, path))

    def __export_pdf(self, path):
        im = Image.open(path)
        if (im.mode == "RGBA"):
            im = im.convert("RGB")
        path = path[:-3] + "pdf"
        im.save(path, "PDF", resolution=100.0)

    def __export_template(self):
        path = self.__save_file_dialog()
        self.__export_png(path)
        
        
    # def test(self):
    #     im = Image.open("screenshot.png")
    #     if (im.mode == "RGBA"):
    #         im = im.convert("RGB")
    #     im.save("screenshot.pdf", "PDF", resolution=100.0)
    #     print("Done")
            
    # generate values fields according to values.json data
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
        """
        
        for key in self.__data:            
            label = QLabel(self.__data[key]["placeholder"])
            label.setMaximumHeight(10)
            label.setStyleSheet(stylesheet)
            self.__fields_container.addWidget(label)
            
            if (self.__data[key]["type"] == "text"):
                lineEdit = QLineEdit()
                lineEdit.setPlaceholderText(self.__data[key]["placeholder"])
                lineEdit.setStyleSheet(stylesheet)
                lineEdit.textChanged.connect(partial(self.__text_changed, key))
                self.__fields_container.addWidget(lineEdit)
            elif (self.__data[key]["type"] == "array"):
                self.__arrays[key] = []
                button = QPushButton("Change")
                button.setStyleSheet(stylesheet)
                button.clicked.connect(partial(self.__open_section_dialog, key, self.__web_view, self.__data[key]["fields"]))
                self.__fields_container.addWidget(button)
            elif (self.__data[key]["type"] == "image"):
                button = QPushButton("Select Image")
                button.setStyleSheet(stylesheet)
                button.clicked.connect(self.__open_file_dialog)
                self.__fields_container.addWidget(button)
                
        self.__fields_container.addStretch(1)
    
    # callback event for text fields
    def __text_changed(self, field, value):
        self.__web_view.page().runJavaScript("updateTextValue('{}', '{}')".format(field, value))
        
    # callback function for section buttons dialog
    def __open_section_dialog(self, section_id, web_view, json_fields):
        self.__gui_controller.showSectionEntriesDialog(self.__arrays[section_id], section_id, web_view, json_fields)

    # callback function for selecting file with file dialog
    def __open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png)", options=options)
        if filename:
            self.__web_view.page().runJavaScript("updateImage('{}')".format(filename[0]))

    # function to open save file dialog
    def __save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save Template", "", "Image (*.png)")
        if filename:
            return filename
                
                
                
                
                
                
                
                
                
                
                
                
                