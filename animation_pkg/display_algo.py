import curses
import time
import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def gradual_appear_letters(text,speed,acceleration,stdscr):    
    stdscr.clear()
    # Get the height and width of the window
    height, width = stdscr.getmaxyx()
    
    # Calculate the starting position of the text
    start_x = width // 2 - len(text) // 2
    start_y = height // 2
    
    for i, char in enumerate(text):
        # Display character at the specified position
        stdscr.addch(start_y, start_x + i, char)
        stdscr.refresh()
        
        # Wait for a certain amount of time
        time.sleep(speed)
        
        # Decrease the wait time to speed up
        speed = max(0.1, speed - acceleration)

def gradual_appear_words(text, speed, acceleration, stdscr):
    stdscr.clear()
    words = text.split()
    
    height, width = stdscr.getmaxyx()
    current_y = height // 2

    # Calculate the total length of the text to be displayed
    total_length = sum(len(word) + 1 for word in words) - 1

    # Add extra padding to both sides
    padding = 5
    start_x = max(0, (width - total_length) // 2 - padding)
    current_x = start_x

    for word in words:
        # Check if the word fits in the current line
        if current_x + len(word) >= width:
            # Move to the next line
            current_y += 1
            # Recalculate start_x for the new line to center the text
            current_x = start_x
        
        # Ensure the current position is within the window bounds
        if current_y < height:
            try:
                # Display word at the specified position
                stdscr.addstr(current_y, current_x, word)
                stdscr.refresh()
            except curses.error:
                pass  # Handle the error gracefully

        # Wait for a certain amount of time
        time.sleep(speed)
        
        # Move the current_x position for the next word
        current_x += len(word) + 1  # Add 1 for space
        
        # Decrease the wait time to speed up
        speed = max(0.1, speed - acceleration)

def stop_motion(frames,replay_times,speed,stdscr):
    stdscr.clear()
    # Get the height and width of the window
    height, width = stdscr.getmaxyx()
    # replay the animation frame by frame
    for _ in range(replay_times):
        for frame in frames:
            stdscr.clear()
            # calculate the start position of the frame, to display in the center
            frame_height = len(frame)
            frame_width = len(frame[0])
            x = (width - frame_width) // 2
            y = (height - frame_height) // 2

            for i, line in enumerate(frame):
                if 0 <= y + i < height and 0 <= x < width:
                    stdscr.addstr(y + i, x, line)
            stdscr.refresh()
            time.sleep(speed)

def appear(text,stdscr):
    # Clear the screen
    stdscr.clear()
    
    # Split the ASCII art into lines
    lines = text.splitlines()
    
    # Get the height and width of the window
    height, width = stdscr.getmaxyx()
    
    # Calculate the starting position to center the ASCII art
    start_y = height // 2 - len(lines) // 2
    start_x = width // 2 - max(len(line) for line in lines) // 2
    
    # Display each line of the ASCII art
    for i, line in enumerate(lines):
        stdscr.addstr(start_y + i, start_x, line)
    
    # Refresh the screen to show the changes
    stdscr.refresh()