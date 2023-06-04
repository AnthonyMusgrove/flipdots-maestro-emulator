#!/usr/bin/python

############################################################
##                                                        ##
##                      FlipDots Maestro                  ##
##                    "Set Pixels FlipApp"                ##
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

    print("Frame Data: " + str(frame_data))

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
    

print("Connecting to maestro driver at: " + maestro_server_ip + ":" + str(maestro_server_port))
connect_to_panel()

print("Requesting panel resolution: .. ")
get_panel_resolution()

print("Connected panel resolution: " + str(connected_panel_width) + "x" + str(connected_panel_height))

print("Drawing light coloured pixel at 5,5 ...")
draw_light_pixel(5,5)

print("Drawing dark coloured pixel at 8,2 ...")
draw_dark_pixel(8,2)

print("Drawing transparent pixel at 4,6 ...")
draw_transparent_pixel(4,6)
