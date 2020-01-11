# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:50:46 2019

@author: sunmeet
"""

# gui controller for the template selector window

# importing necessary modules
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from functools import partial
import os
import common

class TemplateSelector(QWidget):
    
    # class initializer
    def __init__(self):
        super(TemplateSelector, self).__init__()    # call the inherited class __init__ method
        self.__gui_controller = common.get_guicontroller_instance()
        
        self.__initUI()
        
    # initialize setup for the ui
    def __initUI(self):
        uic.loadUi("ui/template_selector.ui", self)
        
        self.__template_grid = self.findChild(QGridLayout, "templateGrid")
        
        grid_row = 0
        grid_col = -1
        # adding screenshots to grid layout        
        for template_folder in os.listdir("resume_templates"):
            if (grid_col < 2):
                grid_col = grid_col + 1
            elif (grid_col == 2):
                grid_col = 0
                grid_row = grid_row + 1
            
            label = QLabel()
            pixmap = QPixmap(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resume_templates/" + template_folder + "/screenshot.png")))
            label.setPixmap(pixmap)
            label.resize(10, 10)
            label.setScaledContents(True)
            label.mousePressEvent = partial(self.__template_selected, template_folder)
            
            self.__template_grid.addWidget(label, grid_row, grid_col)
        
        self.show()
        
    # function to close the window
    def close_window(self):
        self.close()
        
    # callback function for template selection
    def __template_selected(self, template_folder, event):
        self.close_window()
        self.__gui_controller.showTemplateEditorWindow(template_folder)
        