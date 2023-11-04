#Written by Nathan A-M =^)
#Buffer-based implementation using 
#A Buffer-based approach as a reference 
import numpy as np
from functools import partial

bitrate = 0 #used to save previous bitrate

def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate):
    #student can do whatever they want from here going forward
    global bitrate
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True) # a list of tuples of (bitrate, size), sorted by size, largest to smallest
    bitrate = BOLA_bufferbased(buf_now= Buffer_Occupancy, R_i= R_i) 
    return bitrate

#helper function, to find the corresponding size of previous bitrate
def match(value, list_of_list): 
    for e in list_of_list:
        if value == e[1]:
            return e
            
#helper function, to find the corresponding size of previous bitrate
#if there's was no previous assume that it was the highest possible value
def prevmatch(value, list_of_list): 
    for e in list_of_list:
        if value == e[1]:
            return e
    value = max(i[1] for i in list_of_list)
    for e in list_of_list:
        if value == e[1]:
            return e

def util_func(chunk_size, min_size, buffer_size, V, gamma_p):
    return (V*np.log(chunk_size/min_size, 2) + V*gamma_p - buffer_size) / chunk_size

def BOLA_bufferbased(buf_now, R_i, V=0.93, gamma_p=5):
    '''
    Input: 
    rate_prev: The previously used video rate
    Buf_now: The current buffer occupancy 
    r: The size of reservoir  //At least greater than Chunk Time
    cu: The size of cushion //between 90 to 216, paper used 126
    R_i: Array of bitrates of videos, key will be bitrate, and value will be the byte size of the chunk
    
    Output: 
    Rate_next: The next video rate
    '''
    bit_rates, chunk_sizes = np.array(R_i).T
    curr_util_func = partial(util_func, min_size=chunk_sizes[-1], buffer_size=buf_now, V=V, gamma_p=gamma_p)
    # calculate the utility function for each bit rate
    util_funcs = np.vectorize(curr_util_func)(chunk_sizes)
    # find the bit rate that maximizes the utility function
    rate_next = bit_rates[np.argmax(util_funcs)]
    return rate_next