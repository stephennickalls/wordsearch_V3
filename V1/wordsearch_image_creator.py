import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
from wordsearch_generator import WordSearchGenerator
from PIL import Image, ImageDraw, ImageFont

def generate_puzzle(words, wsg):
    # wsg = WordSearchGenerator(30, 30, words)
    grid = wsg.generate(words)
    return grid

def plot_puzzle(grid, words, wsg, solution=False, filename='puzzle.png'):
    # Create a blank image for the puzzle
    image_size = (1000, 1200)
    puzzle_image = Image.new('RGB', image_size, 'white')
    draw = ImageDraw.Draw(puzzle_image)

    # Choose a font
    fnt = ImageFont.truetype('arial.ttf', 15)

    # Draw the grid
    grid_size = (900, 900)
    start = (50, 50)
    step = (grid_size[0] // len(grid[0]), grid_size[1] // len(grid))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pos = (start[0] + step[0] * i, start[1] + step[1] * j)
            centered_pos = (pos[0] + step[0] / 2, pos[1] + step[1] / 2)
            draw.text(centered_pos, grid[j][i], font=fnt, fill=(0, 0, 0), anchor="mm")

    # If solution, highlight words
    if solution:
        for word in words:
            path = wsg.find_word(word)
            for pos in path:
                draw.rectangle([(pos[1]*step[0]+start[0], pos[0]*step[1]+start[1]), 
                                ((pos[1]+1)*step[0]+start[0], (pos[0]+1)*step[1]+start[1])], 
                                outline="grey", width=3)

    # Create word list
    words_split = np.array_split(words, 4)
    word_spacing = 30
    for i, word_list in enumerate(words_split):
        max_word_width = max([fnt.getsize(word)[0] for word in word_list])
        start_pos_x = start[0] + i*image_size[0]//4 + (image_size[0]//4 - max_word_width) / 2  # Center the column
        for j, word in enumerate(word_list):
            pos = (start_pos_x, start[1] + grid_size[1] + 50 + j*word_spacing)
            draw.text(pos, word, font=fnt, fill=(0, 0, 0))

    # Save the image
    puzzle_image.save(filename)









# Convert images to PDF
# images_to_pdf(['puzzle.png', 'solution.png'], 'puzzle.pdf')


# Function to handle button click
def generate_wordsearch():
    try:
        #get title
        # title = entry_title.get().strip()
        # get grid size
        size = int(entry_gridsize.get())
        # get words, split by comma and strip spaces
        words = [word.strip() for word in entry_words.get().split(',')]

        # Check if size is valid and there are not more than 20 words
        if size <= 0 or len(words) > 20 or any(len(word) > size for word in words):
            raise ValueError

        # Create instance
        wsg = WordSearchGenerator(size, size, words)

        # Generate puzzle and solution
        puzzle = wsg.generate(words)

        # Plot and save images
        plot_puzzle(puzzle, words, wsg, filename='puzzle.png')
        plot_puzzle(puzzle, words, wsg, solution=True, filename='solution.png')

        # Inform user of successful generation
        messagebox.showinfo("Success", "Wordsearch generated successfully!")
    except ValueError:
        # Show error message
        messagebox.showerror("Invalid input", "Please input a positive number for size, no more than 20 words, and make sure words fit within the grid.")

# Create Tkinter window
root = Tk()
root.geometry('550x400')  # Window size
root.title("Pudding Hill - Word Search Generator")  # Window title

# Create instructions
label_instructions = Label(root, text="\n\nEnter the grid size by entering a number such as 20.\n This will create a square grid that is 20x20 letters.\n\n"
                                      "Enter a comma separated list of up to 20 words.\n The words must be able to fit within the grid or an error will occur.")
label_instructions.pack(padx=10, pady=10)  # Add padding

# Create title entry field
# label_title = Label(root, text="Title (optional):")
# label_title.pack(padx=10, pady=0)  # Add padding
# entry_title = Entry(root)
# entry_title.pack(padx=10, pady=5)  # Add padding

# Create grid size entry field
label_gridsize = Label(root, text="Grid Size:")
label_gridsize.pack(padx=10, pady=0)  # Add padding
entry_gridsize = Entry(root)
entry_gridsize.pack(padx=10, pady=5)  # Add padding

# Create words entry field
label_words = Label(root, text="Words:")
label_words.pack(padx=10, pady=0)  # Add padding
entry_words = Entry(root, width=80)
entry_words.pack(padx=10, pady=5)  # Add padding

# Create generate button
generate_button = Button(root, text="Generate wordsearch", command=generate_wordsearch)
generate_button.pack(padx=10, pady=10)  # Add padding

root.mainloop()
