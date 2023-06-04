#!/usr/bin/python

############################################################
##                                                        ##
##                      FlipDots Maestro                  ##
##                  "A Simple Text FlipApp"               ##
##                                                        ##
##                  By Anthony K. Musgrove                ##
##            Senior Engineer of Labworx, Australia       ##
##                   (anthony@labworx.au)                 ##
##                                                        ##
##                  VER 1.0.0  [04/06/2023]               ##
##              RELEASED UNDER LICENCE GPL 3.0            ##
##                                                        ##
############################################################

import yaml
import os


class dotFont():
    
    def __init__(self, font_file):
        
        self.name = ""
        self.char_width = 0
        self.char_height = 0
        self.char_count = 0
        self.font_data = 0
        self.font_file = font_file
        #self.char_bitmaps = [] * self.character_count 
        
        self.load_font_file()

    def load_font_file(self):
        print("Loading instance of font with font file " + self.font_file)
        
        
        font_file_path = './' + self.font_file + '.yaml'
    
        if not os.path.isfile(font_file_path):
            print("Error: font file doesnt exist: " + font_file_path)
            return 0

        with open(font_file_path, "r") as ymlconf:
        
            self.font_data = yaml.load(ymlconf, Loader=yaml.FullLoader)

            self.name = self.font_data["info"]["name"]
            self.char_width = self.font_data["info"]["char_width"]
            self.char_height = self.font_data["info"]["char_height"]
            self.char_count = self.font_data["info"]["char_count"]
            
            print("Loaded font with name " + self.name + ", charsize: " + str(self.char_width) + "x" + str(self.char_height) + ", total_chars: " + str(self.char_count))
    
    def get_char_bitmap(self, _char):
        return self.font_data["bitmaps"][_char]

    def get_char_width(self):
        return self.char_width

    def get_char_height(self):
        return self.char_height

