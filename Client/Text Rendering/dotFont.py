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
        self.font_data = 0
        self.font_file = font_file
                
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
            
            print("Loaded font with name " + self.name + ", character count: " + str(self.get_char_count()))
    
    def get_char_bitmap(self, _char):
        return self.font_data["bitmaps"][_char]

    def get_char_width(self, _char):
        return len(self.font_data["bitmaps"][_char][0])
        
    def get_char_height(self, _char):
        return len(self.font_data["bitmaps"][_char])

    def get_char_count(self):
        return len(self.font_data["bitmaps"])
            