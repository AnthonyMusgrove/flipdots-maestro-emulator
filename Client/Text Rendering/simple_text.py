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
    
    char_width = font.get_char_width()
    char_height = font.get_char_height()
    
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
            

        
# draw_light_pixel(at_x, at_y):


print("Connecting to maestro driver at: " + maestro_server_ip + ":" + str(maestro_server_port))
connect_to_panel()

print("Requesting panel resolution: .. ")
get_panel_resolution()

print("Connected panel resolution: " + str(connected_panel_width) + "x" + str(connected_panel_height))

clear_screen()

test_font = dotFont("dots_all_for_now")

draw_character(3, 3, test_font, "A")
draw_character(10, 10, test_font, "B")
