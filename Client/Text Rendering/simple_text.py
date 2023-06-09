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

import socket
import sys
import struct
import time

from dotFont import *

maestro_server_ip, maestro_server_port = "localhost", 44000

opcode_display_light_pixel, opcode_display_dark_pixel, opcode_display_transparent_pixel = 0x0, 0x1, 0x2
opcode_display_pixel_with_colour, opcode_display_frame, opcode_send_uid, opcode_get_resolution = 0x3, 0x4, 0x5, 0x6

colour_code_dark, colour_code_light, colour_code_transparent = 0x0, 0x1, 0x2

connected_panel_width, connected_panel_height = 0, 0

comms_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_packed_opcode(opcode):
    return struct.pack('>b', opcode)

def connect_to_panel():

    global comms_socket, maestro_server_ip, maestro_server_port
    comms_socket.connect((maestro_server_ip, maestro_server_port))

def get_panel_resolution():

    global comms_socket, connected_panel_width, connected_panel_height
    comms_socket.sendall(get_packed_opcode(opcode_get_resolution))
    
    resolution_raw_data = str(comms_socket.recv(1024), "utf-8")
            
    connected_panel_width = int(''.join(map(str, struct.unpack('>bbbb', bytes(resolution_raw_data[0:4], 'utf-8')))))
    connected_panel_height = int(''.join(map(str, struct.unpack('>bbbb', bytes(resolution_raw_data[4:8], 'utf-8')))))
    
def draw_frame(frame_data):
    global comms_socket

    #print("Frame Data: " + str(frame_data))

    request_data = get_packed_opcode(opcode_display_frame) + frame_data
    comms_socket.sendall(request_data)

def draw_light_pixel(at_x, at_y):

    global comms_socket
    
    coords_packed = struct.pack('>ll', at_x, at_y)
    
    request_data = get_packed_opcode(opcode_display_light_pixel) + coords_packed
    
    comms_socket.sendall(request_data)

def draw_dark_pixel(at_x, at_y):

    global comms_socket
    
    coords_packed = struct.pack('>ll', at_x, at_y)
    
    request_data = get_packed_opcode(opcode_display_dark_pixel) + coords_packed
    
    comms_socket.sendall(request_data)

def draw_transparent_pixel(at_x, at_y):

    global comms_socket
    
    coords_packed = struct.pack('>ll', at_x, at_y)
    
    request_data = get_packed_opcode(opcode_display_transparent_pixel) + coords_packed
    
    comms_socket.sendall(request_data)

def draw_pixel(at_x, at_y, colour):
    
    global comms_socket
    
    coords_packed = struct.pack('>ll', at_x, at_y)
    
    request_data = get_packed_opcode(opcode_display_pixel_with_colour) + get_packed_opcode(colour) + coords_packed
    
    comms_socket.sendall(request_data)
    
def clear_screen():
    global connected_panel_width, connected_panel_height
    
    total_pixels = connected_panel_width * connected_panel_height
    clear_bytes = [0x0] * total_pixels
    clear_bytes = bytes(clear_bytes);
    draw_frame(clear_bytes)

def new_frame():
    
    new_frame = [0x0] * (connected_panel_width*connected_panel_height)
    return new_frame

def get_x_y_frame_index(x, y):

    global connected_panel_width, connected_panel_height
    return(y * connected_panel_width + x)

def add_to_frame(frame, x, y, pixel_colour):
    frame[get_x_y_frame_index(x,y)] = pixel_colour

def add_character_to_frame(frame, start_x, start_y, font, character):

    #  screen 10x10
    #  char 5x7
    #  start 3,3

    #   0 1 2 3 4 5 6 7 8 9
    #   # # # # # # # # # #
    # 0         o o o
    # 1       o       o 
    # 2       o       o
    # 3       o       o
    # 4       o o o o o
    # 5       o       o 
    # 6       o       o
    # 7
    # 8
    # 9

    font_data = font.get_char_bitmap(character)
    
    char_width = font.get_char_width(character)
    char_height = font.get_char_height(character)
    
    global connected_panel_width, connected_panel_height
    
    # so we know screen width
    
    # draw the first line of the bitmap at start_x, start_y
    
    cur_x = start_x 
    cur_y = start_y
    
    cur_data_line = 0
    cur_data_col = 0
    
    for y in range(char_height):
        for x in range(char_width):
            
            if(font_data[cur_data_line][cur_data_col] == 0x0):
                #print(" Drawing dark pixel at " + str(cur_x) + "," + str(cur_y))
                #draw_dark_pixel(cur_x, cur_y)
                #time.sleep(33/1000)
                add_to_frame(frame, cur_x, cur_y, colour_code_dark)
            
            if(font_data[cur_data_line][cur_data_col] == 0x1):
                add_to_frame(frame, cur_x, cur_y, colour_code_light)
                #print(" Drawing light pixel at " + str(cur_x) + "," + str(cur_y))
                #draw_light_pixel(cur_x, cur_y)
                #time.sleep(33/1000)
            
            cur_x += 1
            cur_data_col += 1
        
        # done a row, now we have to CR and LF (cr to start_x)
        cur_data_line += 1
        cur_data_col = 0
        cur_x = start_x
        cur_y += 1



def draw_character(start_x, start_y, font, character):

    #  screen 10x10
    #  char 5x7
    #  start 3,3

    #   0 1 2 3 4 5 6 7 8 9
    #   # # # # # # # # # #
    # 0         o o o
    # 1       o       o 
    # 2       o       o
    # 3       o       o
    # 4       o o o o o
    # 5       o       o 
    # 6       o       o
    # 7
    # 8
    # 9

    font_data = font.get_char_bitmap(character)
    
    char_width = font.get_char_width(character)
    char_height = font.get_char_height(character)
        
    global connected_panel_width, connected_panel_height
    
    # so we know screen width
    
    # draw the first line of the bitmap at start_x, start_y
    
    cur_x = start_x 
    cur_y = start_y
    
    cur_data_line = 0
    cur_data_col = 0
    
    for y in range(char_height):
        for x in range(char_width):
            
            if(font_data[cur_data_line][cur_data_col] == 0x0):
                print(" Drawing dark pixel at " + str(cur_x) + "," + str(cur_y))
                draw_dark_pixel(cur_x, cur_y)
                time.sleep(33/1000)
            
            if(font_data[cur_data_line][cur_data_col] == 0x1):
                print(" Drawing light pixel at " + str(cur_x) + "," + str(cur_y))
                draw_light_pixel(cur_x, cur_y)
                time.sleep(33/1000)
            
            cur_x += 1
            cur_data_col += 1
        
        # done a row, now we have to CR and LF (cr to start_x)
        cur_data_line += 1
        cur_data_col = 0
        cur_x = start_x
        cur_y += 1
            

print("Connecting to maestro driver at: " + maestro_server_ip + ":" + str(maestro_server_port))
connect_to_panel()

print("Requesting panel resolution: .. ")
get_panel_resolution()

print("Connected panel resolution: " + str(connected_panel_width) + "x" + str(connected_panel_height))

# load test font
test_font = dotFont("dots_all_for_now")

# clear the screen
clear_screen()

# create new empty frame
test_frame = new_frame()

# add characters to frame
add_character_to_frame(test_frame, 0, 1, test_font, "A")
add_character_to_frame(test_frame, 6, 1, test_font, "B")
add_character_to_frame(test_frame, 12, 1, test_font, "C")
add_character_to_frame(test_frame, 18, 1, test_font, "D")
add_character_to_frame(test_frame, 24, 1, test_font, "E")
add_character_to_frame(test_frame, 30, 1, test_font, "F")
add_character_to_frame(test_frame, 36, 1, test_font, "G")
add_character_to_frame(test_frame, 42, 1, test_font, "H")

add_character_to_frame(test_frame, 0, 9, test_font, "I")
add_character_to_frame(test_frame, 2, 9, test_font, "J")
add_character_to_frame(test_frame, 8, 9, test_font, "K")
add_character_to_frame(test_frame, 14, 9, test_font, "L")
add_character_to_frame(test_frame, 20, 9, test_font, "M")
add_character_to_frame(test_frame, 28, 9, test_font, "N")
add_character_to_frame(test_frame, 34, 9, test_font, "O")
add_character_to_frame(test_frame, 40, 9, test_font, "P")

add_character_to_frame(test_frame, 0, 17, test_font, "Q")
add_character_to_frame(test_frame, 6, 17, test_font, "R")
add_character_to_frame(test_frame, 12, 17, test_font, "S")
add_character_to_frame(test_frame, 18, 17, test_font, "T")
add_character_to_frame(test_frame, 24, 17, test_font, "U")
add_character_to_frame(test_frame, 30, 17, test_font, "V")
add_character_to_frame(test_frame, 36, 17, test_font, "W")

add_character_to_frame(test_frame, 0, 26, test_font, "X")
add_character_to_frame(test_frame, 6, 26, test_font, "Y")
add_character_to_frame(test_frame, 12, 26, test_font, "Z")

add_character_to_frame(test_frame, 20, 26, test_font, "1")
add_character_to_frame(test_frame, 23, 26, test_font, "2")
add_character_to_frame(test_frame, 29, 26, test_font, "3")
add_character_to_frame(test_frame, 35, 26, test_font, "4")
add_character_to_frame(test_frame, 41, 26, test_font, "5")

add_character_to_frame(test_frame, 0, 34, test_font, "6")
add_character_to_frame(test_frame, 6, 34, test_font, "7")
add_character_to_frame(test_frame, 12, 34, test_font, "8")
add_character_to_frame(test_frame, 18, 34, test_font, "9")
add_character_to_frame(test_frame, 24, 34, test_font, "0")

add_character_to_frame(test_frame, 30, 34, test_font, ".")
add_character_to_frame(test_frame, 32, 34, test_font, ":")
add_character_to_frame(test_frame, 34, 34, test_font, ",")
add_character_to_frame(test_frame, 36, 34, test_font, ";")
add_character_to_frame(test_frame, 38, 34, test_font, "'")
add_character_to_frame(test_frame, 40, 34, test_font, "\"")
add_character_to_frame(test_frame, 43, 34, test_font, "(")

add_character_to_frame(test_frame, 0, 43, test_font, ")")
add_character_to_frame(test_frame, 4, 43, test_font, "!")
add_character_to_frame(test_frame, 6, 43, test_font, "?")
add_character_to_frame(test_frame, 12, 43, test_font, "+")
add_character_to_frame(test_frame, 18, 43, test_font, "-")
add_character_to_frame(test_frame, 22, 43, test_font, "*")
add_character_to_frame(test_frame, 31, 43, test_font, "/")
add_character_to_frame(test_frame, 39, 43, test_font, "=")


# draw frame
draw_frame(bytes(test_frame))

