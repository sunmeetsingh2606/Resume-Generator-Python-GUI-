# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:22:35 2019

@author: sunmeet
"""

# this file is the starting point of the program

# importing necessary modules
from PyQt5.QtWidgets import QApplication
import sys
import common

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui_controller = common.get_guicontroller_instance()
    gui_controller.showTemplateSelectorWindow()
    sys.exit(app.exec())