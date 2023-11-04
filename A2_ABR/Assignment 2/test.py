import numpy as np
from functools import partial

def util_func(chunk_size, min_size, buffer_size, V, gamma_p):
    return (V*np.log(chunk_size/min_size) + V*gamma_p - buffer_size) / chunk_size

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

if __name__ == '__main__':
    R_i = [(7000000, 1243825), (1000000, 250784), (500000, 125223)]
    buffer_now = 0
    next_rate = BOLA_bufferbased(buffer_now, R_i)
    print(next_rate)