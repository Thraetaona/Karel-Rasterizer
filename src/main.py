# Karel Rasterizer: An image rasterizer written in Python using CodeHS' Karel API.
# Copyright (C) 2020  Fereydoun Memarzanjany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
The general idea in here is to have a one-to-one representation
of our canvas (Which is similar to ASCII Art.) to the actual grid
that karel is going to paint for us later.
This would significantly shorten the resulting code, so that instead
of having to hardcode each step in order to draw a complicated shape,
we instead "write" it down here and have Karel interpret it for us.

Also another thing to note is that each element in said array
uniquely identifies a color in UltraKarel's painting API, we opted
in to use numeric values instead of strings to simplify the canvas and
make it easier to add more colors in the future, or in other words,
make the project easier to maintain.
The above logic is done using a python "dictionary" (Similar
to a hash table.) inside of the render_frame() function.
"""

# Global variables (These are "Supposed" to be constant and immutable.)
frame_buffer = list([])
"""
# Since the colors in UltraKarel API are defined as strings,
# (i.e., 'Red' and 'Blue' as opposed to numeric identifiers),
# we instead use some sort of if-else (Or switch-case) to
# match the numeric color values of our canvas array with
# their string counterparts.
"""
color_map = dict({})

# Mutable global variables
BUFFER_INDEX = int(0) # Arrays are indexed from 0, not 1.
# This first has to be initialized using populate_world_info() before usage.
WORLD_LENGTH = int(0)
# Indicates whether we are drawing a row from right-to-left or not.
# -1 for if true, +1 otherwise. (We do not use the bool type.)
#
# This greatly improves the overall rendering performacne.
REVERSED = int(1)



"""
Disclaimer: We have no choice but to define our large array like this, because
in real Python, you could use concepts like line continuation or line breaking
in order to span a large formula or elements of array onto several lines (i.e.,
Manually wrapping the code to make it more legible.), but here in karel, it is
basically impossible.

For example this code:

    array = [
    1, 2, 3,
    4, 5 ,6,
    7, 8, 9
    ]

Would work just fine in Python, but in Karel it would result in an invalid
input error from the validator, and if we remove all the newlines so that
the new code becomes:

    array = [1, 2, 3, 4, 5, 6, 7, 8, 9]

Then our code would work just fine!

But the problem here is that when we have a very large array with more than
hundreds of elements, this would mean that defining said array on a single
line is going to be very ugly and impossible to easily search for the rows
and columns as a human reader.
(Quicknote: For very large arrays it is better to allocate memory on the heap 
instead of the stack anyway, but this holds true for languages like C or C++ 
where you have much more control about what is going on, not for Python.)

So, I have tried everything I could think of to work around this issue in Karel,
from using back-slashes \, curly or square brackets {} [], parentheses (),
commas, semi-colons ;, etc, but at the end I was not able to get it to work,
no matter what I tried.
I spent hours searching the Internet, Karel documentations, CodeHS' Karel
source codes, python documentations and similar errors, and still had no luck.

So the only choice i was left with was to either:
a) Instead of having a 20x20 array I would have 20 arrays of length 20 each,
but this meant that I would now have to interpret each array (canvas), so
the solution was not really good

b) I could manually "construct" (Concatenate) the arrays mentioned above into
a single one, this has the disadvantage of having to write an initializer which
has to run at the start of the program, but at the end of the day we are coding
in Python on web which is slow by nature, so micro-optimizing is not worth it.

Below here, method b) can be seen in action.

(This also initializes the dictionary color_map, as it 
also suffers from the exact same issue as the frame_buffer.)
"""
def initialize_frame(): 
    # This is a temporary array that we use to construct a final "canvas"
    # out of a number of arrays (Rows of the canvas).
    # It starts empty and progressively fills up each time.
    #
    # We could also write to the global array (frame_buffer) directly, but
    # it is often not a good practice to write to a global so many times
    # especially without a guard or mutex lock, in real programming.
    t = list([])
    
    # Although not perfect, we can now get nearly the same legibility as we
    # previously could in Python, so now we are able to preserve the canvas
    # just as we preserve the grid world karel is in.
    #
    # We could also use a 2D array, but that has no benefits for this task
    # and would complicate things by having 2 different indices.
    #
    # Construction 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19 X / Y #
    t.extend(list([2, 2, 2, 2, 2, 2,18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 00
    t.extend(list([2, 2,18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,18, 2, 2, 2, 2])) # 01
    t.extend(list([2, 2, 2, 2,18, 2, 2, 2, 2, 2,18, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 02
    t.extend(list([2, 2, 2, 2, 2, 2, 2,18, 2, 2, 2, 2, 2, 2, 2,18, 2, 2, 2, 2])) # 03
    t.extend(list([2, 2,18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 04
    t.extend(list([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 05
    t.extend(list([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 06
    t.extend(list([2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 07
    t.extend(list([2, 0, 8, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 08
    t.extend(list([0, 8, 8, 8, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])) # 09
    t.extend(list([0, 8, 8, 8, 8, 0, 2, 2, 2, 2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 2])) # 10
    t.extend(list([8, 8, 8, 8, 8, 0, 2, 2, 2, 2, 2, 2, 8, 8, 2, 2, 2, 2, 2, 2])) # 11
    t.extend(list([8, 8, 7, 8, 8, 8, 8, 5, 2, 2, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2])) # 12
    t.extend(list([8, 7, 7, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 2, 3, 3, 3])) # 13
    t.extend(list([8, 8, 8, 8, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3])) # 14
    t.extend(list([3, 3, 8, 3, 3, 3, 3, 3, 5, 5, 3, 3, 3, 3, 3, 3, 9, 9, 9, 3])) # 15
    t.extend(list([3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 3, 3, 3, 3, 3, 9, 9, 9, 3])) # 16
    t.extend(list([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 6, 3, 3])) # 17
    t.extend(list([3,19, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 3, 3, 3, 1, 3, 6, 1, 3])) # 18
    t.extend(list([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 3, 3, 3, 3, 6, 3, 3])) # 19

    # Now that we are done with constructing our temporary array, we finish by
    # writing that into the actual frame_buffer.
    frame_buffer.extend(t[:])
    
    # Now we re-use t as a temporary _dictionary_ constructor for color_map.
    del t
    t = dict({})
    
    # Now we begin the construction with the same logic as above,
    # update() is to dict what extend() is to list.
    # 
    # the prefix 0b is used to represent binary values in their original format.

    """
    It is important to notice that although the white color looks no different
    from the uncolored blocks of our grid, they are actually not treated the
    same way!  For example if we put a check like:
    
        if color_is(color['white']):
    
    Then it would return false on uncolored grids, but if we paint a tile white:
    
        paint(color['white'])
        
    and then run the if condition again then it retruns true, even though that
    tile visually look the same as any other uncolored tile!
    
    
    So in conculusion, a white-colored tile is not the same as an uncolored tile.
    Also there are 23 colors in the color[] array from UltraKarel, but since
    we do not know their keys (string name), we have to use the standard ones
    only.  Also since we do not know the key for the"blank" color, we have to
    resort to using white.
    """
    t.update(dict({0b0000: 'white'})) # white != blank (Uncolored)
    t.update(dict({0b0001: 'red'}))
    t.update(dict({0b0010: 'blue'}))
    t.update(dict({0b0011: 'green'}))
    t.update(dict({0b0100: 'yellow'}))
    t.update(dict({0b0101: 'cyan'}))
    t.update(dict({0b0110: 'orange'}))
    t.update(dict({0b0111: 'black'}))
    t.update(dict({0b1000: 'gray'}))
    t.update(dict({0b1001: 'purple'}))
    
    # the 1 in 0b10000 is a special "Bit flag" that will make the renderer
    # place down a tennis ball in addition to coloring the tile.
    t.update(dict({0b10000: 'white'}))
    t.update(dict({0b10001: 'red'}))
    t.update(dict({0b10010: 'blue'}))
    t.update(dict({0b10011: 'green'}))
    t.update(dict({0b10100: 'yellow'}))
    t.update(dict({0b10101: 'cyan'}))
    t.update(dict({0b10110: 'orange'}))
    t.update(dict({0b10111: 'black'}))
    t.update(dict({0b11000: 'gray'}))
    t.update(dict({0b11001: 'purple'}))
    
    # Write the entire temporary dictionary into the actual color_map dict.
    color_map.update(t)
    
    # Just to be sure, we manually free the temporary array object.
    # But normally it would be out of scope anyhow.
    del t

def upscale_frame_4x():
    global frame_buffer;
    #upscaled_frame = list([0] * (WORLD_LENGTH*WORLD_LENGTH))
    upscaled_frame = list([])
    original_length = WORLD_LENGTH/2
    
    """
    The below code was hastily-written and could later be expanded or 
    optimized for more generic cases.
    """
    # Height
    for j in range(0, original_length):
        # Width
        for i in range(j*original_length, (j+1)*original_length):
            upscaled_frame.append(frame_buffer[i])
            upscaled_frame.append(frame_buffer[i])
    
    for j in range(0, WORLD_LENGTH, 2):
        #upscaled_frame.insert(j+1, upscaled_frame[j*40:(j+1)*40])
        #upscaled_frame[(j+1)*40:(j+2)*40].extend(upscaled_frame[j*40:(j+1)*40])
        for i in range(0, WORLD_LENGTH):
            upscaled_frame.insert(((j+1)*WORLD_LENGTH)+i, upscaled_frame[(j*WORLD_LENGTH)+i])


    del frame_buffer[:] # This clears the contents only, not the object itself.
    frame_buffer.extend(upscaled_frame[:])
    
    
# Safe (Checked) move function, never crashes.
def move_s():
    if front_is_clear():
        move()


# Because we do not have access to the World() object's width and height,
# we have to manually get this information by counting the number of steps
# it takes to reach the end of a row.
#
# Assuming that the world is square and not a rectangle, of course.
#
# It also positions karel from (0, 0) to the first column of the last row.
def populate_world_info_and_prepare():
    steps = 1
    
    turn_left()
    
    while front_is_clear():
        steps += 1
        move()
    
    turn_right()

    global WORLD_LENGTH; WORLD_LENGTH = steps


def render_frame():
    global BUFFER_INDEX, REVERSED;
    
    # Traverse and paint the first row we are in, until we reach it's end.
    render_row() # For parity
    # While we have not reached the end (bottom-left or bottom-right) yet.
    while not ((facing_east() and right_is_blocked()) or (facing_west() and left_is_blocked())):
        # We rotate to left or right depending on the direction we face.
        if facing_east():
            turn_right()
            move_s()
            turn_right()
            
            # Because we are now facing west, we can not draw as we would
            # before, otherwise we would be drawing the row in reverse.
            # So we add the number of blocks in the row to the buffer index and
            # we later count that amount back downwards inside of render_row();
            # in this way we won't have to begin at the first column each time
            # to draw and we will have a faster renderer in general.
            REVERSED = -1
        else:
            turn_left()
            move_s()
            turn_left()
            
            REVERSED = +1
        
        BUFFER_INDEX += WORLD_LENGTH
        # And then we traverse and paint the next rows.
        render_row()



def render_row():
    # Paint the first pixel that we are standing on.
    render_pixel() # For parity
    while front_is_clear():
        move()
        
        global BUFFER_INDEX; BUFFER_INDEX += REVERSED
        render_pixel()
        

# Paints a single pixel, meaning spot or block in the grid.
def render_pixel():
    color_num = frame_buffer[BUFFER_INDEX]
    color_str = color_map[color_num]
    
    # Check the bit flag on whether to also place down a tennis ball or not.
    # 
    # Maybe it would be faster to move this logic to the dictionary and
    # call put_ball() inside of there, but that would enlarge the size by a bit.
    if (color_num & 0b10000):
        put_ball()
    
    paint(color[color_str])
    

def rasterize():
    # This only requires a run-time initialization because of Karel's
    # interpreter's own problems, but let's pretend that we are loading an
    # image from the disk to justify this startup delay.
    initialize_frame()

    # If the world size is different from our kernel (framebuffer size, 20x20),
    # We will have to "upscale" it first. (To 40x40 in this case.)
    if not (WORLD_LENGTH == 20):
        upscale_frame_4x()

    # Now we "Render" the global frame_buffer onto the screen
    render_frame()

"""
# DEBUG: For finding out the value of variables, as we do not have print().
def _dbg_var_dump():
    var = BUFFER_INDEX # Value to test against
    
    # Assuming that we start at point (0, 0).
    turn_around(); move()
    
    # Remove any existing tennis balls.
    while balls_present():
        take_ball()
    
    # Place down an amount of tennis balls equal to that of the variable's value.
    while not (var == 0):
        put_ball()
        var -= 1
    
    # Move back so that the tennis balls are visible.
    turn_around(); move()
"""

    
""" Main harness function for driving the code. """
if (__name__ == "__main__"):
    populate_world_info_and_prepare()

    rasterize()
