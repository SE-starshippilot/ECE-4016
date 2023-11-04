#Written by Nathan A-M =^)
#Buffer-based implementation using 
#A Buffer-based approach as a reference 
import numpy as np
from functools import partial

bitrate = 0 #used to save previous bitrate

def student_entrypoint(Measured_Bandwidth, prev_throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate):
    #student can do whatever they want from here going forward
    global bitrate
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True) # a list of tuples of (bitrate, size), sorted by size, largest to smallest
    bitrate = BOLA_finite(Buffer_Occupancy, R_i, Chunk, bitrate, prev_throughput) 
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

def util_func(chunk_size, visual_util, buffer_size, V, gamma_p):
    return (V*visual_util + V*gamma_p - buffer_size) / chunk_size

def get_prev_index(bitrates, target):
    indices = np.where(bitrates == target)[0]
    return indices[0] if indices.size>0 else len(bitrates)

def BOLA_finite(buf_now, R_i, Chunk, prev_rate, prev_throughput, gamma_p=5):
    '''
    Input: 
    buf_now: The current buffer occupancy 
    R_i: Array of bitrates of videos, key will be bitrate, and value will be the byte size of the chunk
    Chunk: Meta info regarding chunk duration, time left, and current chunk
    prev_rate: The previously used video rate
    
    Output: 
    next_rate: The next video rate
    '''
    chunk_sizes = np.array([R[1] for R in R_i])
    visual_utils = np.log(chunk_sizes / chunk_sizes[-1])
    chunk_left, chunk_current, chunk_duration = int(Chunk['left']), int(Chunk['current']), int(Chunk['time'])  
    buffer_max = buf_now['size'] / int(R_i[-1][0])
    t = min(chunk_left, chunk_current) * chunk_duration
    t_prime = max(t/2, chunk_duration*3)
    buffer_d_max = min(buffer_max, t_prime / chunk_duration)
    V_d = (buffer_d_max - 1) / (visual_utils[0] - 1)
    curr_util_func = np.vectorize(util_func)
    curr_util_scores = curr_util_func(chunk_sizes, visual_utils, buf_now['size'] / int(R_i[0][0]), V_d, gamma_p)
    next_rate_index = np.argmax(curr_util_scores)
    prev_rate_index = get_prev_index(chunk_sizes, int(prev_rate))
    next_rate, prev_rate = int(R_i[next_rate_index][0]), int(prev_rate)
    if next_rate_index < prev_rate_index:
        _throughput = max(prev_throughput, chunk_sizes[-1]/chunk_duration) * chunk_duration
        _rate_index = np.argmin(chunk_sizes <= _throughput)
        if _rate_index <= next_rate_index:
            _rate_index = next_rate_index
        elif _rate_index > prev_rate_index:
            _rate_index = prev_rate
        else:
            _rate_index = _rate_index - 1
        next_rate_index = _rate_index
    next_rate = R_i[next_rate_index][0]
    return next_rate