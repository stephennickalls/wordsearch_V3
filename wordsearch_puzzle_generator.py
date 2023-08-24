import os 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
from tkinter import IntVar, StringVar, Checkbutton, OptionMenu
from PIL import Image, ImageDraw, ImageFont
from wordsearch_generator import WordSearchGenerator

# Defaults
DEFAULT_GRID_SIZE = 22
DEFAULT_OUTPUT_WORDS = True
DEFAULT_NUM_COLUMNS = 4
DEFAULT_FONT = "Open Sans"

def generate_puzzle(words, wsg):
    grid = wsg.generate(words)
    return grid

import os
import matplotlib.pyplot as plt

def plot_puzzle(grid, words, wsg, solution=False, filename='puzzle.png'):
    fig, ax = plt.subplots(figsize=(10,10))

    # Draw each letter of the grid on the plot
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            c = grid[j][i]
            ax.text(i + 0.5, j + 0.5, str(c), va='center', ha='center', fontsize=15)

    if solution:
        for word in words:
            path = wsg.find_word(word)
            start = path[0]
            end = path[-1]
            
            # Get the middle point of the start and end coordinates
            mid_start = (start[1] + 0.5, start[0] + 0.5)
            mid_end = (end[1] + 0.5, end[0] + 0.5)

            # Draw the line through the center of the word
            line = plt.Line2D([mid_start[0], mid_end[0]], [mid_start[1], mid_end[1]], color='grey', lw=13, alpha=0.6, solid_capstyle='round')
            ax.add_line(line)

    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, len(grid))
    ax.set_xticks(range(len(grid[0]) + 1))
    ax.set_yticks(range(len(grid) + 1))
    ax.grid(True)

    # Check if "Puzzles" directory exists and create it if not
    if not os.path.exists("Puzzles"):
        os.makedirs("Puzzles")

    # Adjust the filename to include "Puzzles" directory
    filename = os.path.join("Puzzles", filename)

    plt.axis('off')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)



def generate_wordsearch():
    try:
        size = int(entry_gridsize.get())
        words = [word.strip() for word in entry_words.get().split(',')]
        filename = entry_filename.get().strip()

        # Check the words input
        if not check_input(words):
            return

        if size <= 0 or len(words) > 20 or any(len(word) > size for word in words):
            raise ValueError

        wsg = WordSearchGenerator(size, size, words)

        puzzle = wsg.generate(words)

        plot_puzzle(puzzle, words, wsg, filename=f'{filename}_puzzle.png')
        plot_puzzle(puzzle, words, wsg, solution=True, filename=f'{filename}_solution.png')

        if output_words_var.get() == 1:
            columns = int(entry_columns.get())
            font_path = fonts[selected_font_var.get()]
            output_words_to_png(words, f"{filename}_words.png", columns, font_path)


        messagebox.showinfo("Success", "Wordsearch generated successfully!")
    except ValueError:
        messagebox.showerror("Invalid input", "Please input a positive number for size, no more than 20 words, and make sure words fit within the grid.")

def check_input(word_list):
    for word in word_list:
        if not word.isalpha():
            messagebox.showerror("Invalid input", "Please make sure your words contain only alphabetic characters. Special characters and numbers are not allowed.")
            return False
    return True



def output_words_to_png(words, filename, columns, font_path):
    # Calculate image size (this can be adjusted)
    padding = 20  # Added padding
    img_width = 1300
    column_width = (img_width - (columns - 1) * padding) // columns
    # img_height = 40 * len(words)
    img_height = 285

    x_padding = (img_width-(column_width*4))-15

    # Step 2: Check if "Puzzles" directory exists and create it if not
    if not os.path.exists("Puzzles"):
        os.makedirs("Puzzles")

    # Step 3: Adjust the filename to include "Puzzles" directory
    filename = os.path.join("Puzzles", filename)

    # Create an image
    img = Image.new('RGB', (img_width, img_height), color='white')
    d = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, 35)
    y_offset = 25
    for i, word in enumerate(words):
        col_index = i % columns
        
        # Adjust for padding and skip padding for the last column
        x_offset = x_padding + col_index * column_width + min(col_index, columns - 1) * padding
        
        d.text((x_offset + 10, y_offset), word, fill='black', font=font)
        
        if (i + 1) % columns == 0:
            y_offset += 45
    
    img.save(filename)


print("\n\nThis window is supposed to open first.")
print("The Word Search Generator user interface will start shortly\.")

root = Tk()
root.geometry('500x500')  

try:
    root.iconbitmap("wordsearch.ico")
except Exception as e:
    pass  # Do nothing if the icon file is not found

root.title("Word Search Generator")

label_instructions = Label(root, text="\n\nEnter the grid size by entering a number such as 20.\n This will create a square grid that is 20x20 letters.\n\n"
                                      "Enter a comma separated list of up to 20 words.\n The words must be able to fit within the grid. \n A 20x20 grid can only accept words upto 20 characters long")
label_instructions.pack(padx=10, pady=10)

# Set default for grid size
label_gridsize = Label(root, text="Grid Size:")
label_gridsize.pack(padx=10, pady=0)
entry_gridsize = Entry(root)
entry_gridsize.insert(0, DEFAULT_GRID_SIZE)  # Populate the default value
entry_gridsize.pack(padx=10, pady=5)

label_words = Label(root, text="Words:")
label_words.pack(padx=10, pady=0)
entry_words = Entry(root, width=80)
entry_words.pack(padx=10, pady=5)

# Create filename entry field
label_filename = Label(root, text="Filename:")
label_filename.pack(padx=10, pady=0)
entry_filename = Entry(root)
entry_filename.pack(padx=10, pady=5)

# Set default for outputting words to PNG
output_words_var = IntVar(value=1 if DEFAULT_OUTPUT_WORDS else 0)
output_words_checkbutton = Checkbutton(root, text="Output words to a .png file?", variable=output_words_var)
output_words_checkbutton.pack(padx=10, pady=5)

# Set default for number of columns
label_columns = Label(root, text="Number of columns for words (if outputting):")
label_columns.pack(padx=10, pady=0)
entry_columns = Entry(root)
entry_columns.insert(0, DEFAULT_NUM_COLUMNS)  # Populate the default value
entry_columns.pack(padx=10, pady=5)

fonts = {
    "Open Sans": "OpenSans.ttf",
    "Arial": "arial.ttf",
    "EB Garamond" : "EBGaramond.ttf",
    "Times New Roman": "times.ttf",
    "Verdana": "verdana.ttf"
}

# Set default for fonts
label_instructions = Label(root, text="Font")
label_instructions.pack(padx=10, pady=0)
selected_font_var = StringVar(root)
selected_font_var.set(DEFAULT_FONT)  # Set the default font
font_option_menu = OptionMenu(root, selected_font_var, *fonts.keys())
font_option_menu.pack(padx=10, pady=5)

generate_button = Button(root, text="Generate wordsearch", command=generate_wordsearch)
generate_button.pack(padx=10, pady=10)

root.mainloop()




generate_button = Button(root, text="Generate wordsearch", command=generate_wordsearch)
generate_button.pack(padx=10, pady=10)

root.mainloop()
