# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:41:42 2019

@author: sunmeet
"""

# this class handles the guis of the program
# this is a controller class of the program

# importing necessary modules
from gui_controllers import template_selector, template_editor, section_entries, section_new_entry_dialog

class GUIController:
    
    __instance = None
    
    # class initializer
    def __init__(self):
        if GUIController.__instance != None:
            raise Exception("GUIController class is singleton!")
        else:
            GUIController.__instance = self
            
    @staticmethod
    def getInstance():
        if GUIController.__instance == None:
            GUIController()
        
        return GUIController.__instance
    
    def showTemplateSelectorWindow(self):
        template_selector_obj = template_selector.TemplateSelector()
        
    def showTemplateEditorWindow(self, template_folder):
        template_editor_obj = template_editor.TemplateEditor(template_folder)

    def showSectionEntriesDialog(self, array, section_id, web_view, json_fields):
        section_entries_dialog_obj = section_entries.SectionEntriesDialog(array, section_id, web_view, json_fields)
        
    def showSectionNewEntryDialog(self, section_id, web_view, json_fields):
        section_new_entry_dialog_obj = section_new_entry_dialog.SectionNewEntryDialog(section_id, web_view, json_fields)
        return section_new_entry_dialog_obj
        
        
        
        
        
        
        