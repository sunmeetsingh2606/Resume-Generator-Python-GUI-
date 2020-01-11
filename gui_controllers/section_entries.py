# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:10:09 2019

@author: sunmeet
"""

# gui controller for the section entries dialog

# importing necessary modules
from PyQt5.QtWidgets import QDialog, QPushButton, QListWidget
from PyQt5 import uic
import common

class SectionEntriesDialog(QDialog):

    # class initializer
    def __init__(self, array, section_id, web_view, json_fields):
        super(SectionEntriesDialog, self).__init__()    # call the inherited class __init__ method
        self.__gui_controller = common.get_guicontroller_instance()
        self.__array = array
        self.__section_id = section_id
        self.__web_view = web_view
        self.__json_fields = json_fields
        
        self.__initUI()

    # initialize setup for the ui
    def __initUI(self):
        uic.loadUi("ui/section_entries.ui", self)

        stylesheet = """
            QListWidget::item {
                color: #fff;
            }
        """

        self.__entries_listview = self.findChild(QListWidget, "entriesListView")
        self.__entries_listview.itemSelectionChanged.connect(self.__selection_changed)
        self.__entries_listview.setStyleSheet(stylesheet)
        self.__add_button = self.findChild(QPushButton, "addButton")
        self.__add_button.clicked.connect(self.__open_new_entry_dialog)
        self.__delete_button = self.findChild(QPushButton, "deleteButton")
        self.__delete_button.clicked.connect(self.__delete_entry)
        
        self.exec()

    # function to open new entry dialog
    def __open_new_entry_dialog(self):
        new_entry_dialog_obj = self.__gui_controller.showSectionNewEntryDialog(self.__section_id, self.__web_view, self.__json_fields)
        if (new_entry_dialog_obj.get_array()):
            self.__array.append(new_entry_dialog_obj.get_array())
            self.__update_list_view()

    # function to delete entry
    def __delete_entry(self):
        self.__web_view.page().runJavaScript("removeListItem(\"{}\", \"{}\")".format(self.__section_id, self.__selected_index))

    # callback function for item selection
    def __selection_changed(self):
        self.__selected_index = self.__entries_listview.currentRow() + 1

    # function to update list view if an item is added
    def __update_list_view(self):
        # print(self.__array[-1]["university"])
        obj_to_array = []
        for key, value in (self.__array[-1]).items():
            obj_to_array.append(value)

        self.__entries_listview.addItem(obj_to_array[0] + "\n" + obj_to_array[1])