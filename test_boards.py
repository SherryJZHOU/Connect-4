"""Test boards for Connect

Place test boards in this module to help test your code.  Note that since connect.GameState
stores board contents as a 0-based list of lists, these boards are reversed to they can be written
right side up here.

"""

# dictionary with label, test board key-value pairs
boards = {}  

# For testing vanilla minimax
boards['choose_middle'] = reversed([
    [ -1, -1,  1,  0,  1, -1,  0 ],  
    [ -1,  1, -1,  0, -1,  1,  0 ],
    [ -1, -1,  1,  0,  1, -1, -1 ],
    [  1,  1,  1,  0,  1,  1, -1 ],
    [  1, -1,  1,  1,  1, -1, -1 ],
    [  1,  1, -1, -1, -1,  1, -1 ] ])

boards['choose_middle_2'] = reversed([
    [ -1,  0,  0,  -1, -1],
    [ -1,   1, -1,  1,  1],
    [  1,  -1,  1, -1,  1],
    [  1,   1, -1,  1, -1]])

boards['small_right'] = reversed([
    [  0,  0],  
    [ -1,  1],
    [ -1,  1] ])

boards['test_4x4'] = reversed([
    [ 0, -1,  0,  0],
    [-1, -1,  0,  1],
    [-1, -1,  1,  1],
    [ 1,  1, -1,  1]      
]) 

boards['your_test'] = reversed([
    [ 0, 0,  0,  0],
    [ 0, 0,  0,  0],
    [ 0, 0,  0,  0],
    [ 0,  0, 0,  0]
]) 

