# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:37:01 2019

@author: sunmeet
"""

# this file contains common function for the application

# importing necessary modules
from gui_controller import GUIController

# return a gui controller instance whenever needed by other classes
def get_guicontroller_instance():
    gui_controller = GUIController.getInstance()
    return gui_controller