import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
from wordsearch_generator import WordSearchGenerator
from wordsearch_generator import WordSearchGenerator

def generate_puzzle(words, wsg):
    # wsg = WordSearchGenerator(30, 30, words)
    grid = wsg.generate(words)
    return grid

def plot_puzzle(grid, words, wsg, solution=False, filename='puzzle.png'):
    fig, ax = plt.subplots(figsize=(10,10))

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            c = grid[j][i]
            ax.text(i+0.5, j+0.5, str(c), va='center', ha='center')

    if solution:
        for word in words:
            path = wsg.find_word(word)
            for pos in path:
                ax.add_patch(Rectangle((pos[1], pos[0]), 1, 1, fill=None, edgecolor='red', lw=3))

    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, len(grid))
    ax.set_xticks(range(len(grid[0])+1))
    ax.set_yticks(range(len(grid)+1))
    ax.grid(True)

    plt.axis('off')
    plt.savefig(filename, dpi=300)
    plt.close(fig)

def images_to_pdf(image_list, pdf_filename):
    pdf = FPDF()
    for image in image_list:
        pdf.add_page()
        pdf.image(image, x = 0, y = 0, w = 210)
    pdf.output(pdf_filename, "F")

# Convert images to PDF
# images_to_pdf(['puzzle.png', 'solution.png'], 'puzzle.pdf')


# Function to handle button click
def generate_wordsearch():
    try:
        # get grid size
        size = int(entry_gridsize.get())
        # get words, split by comma and strip spaces
        words = [word.strip() for word in entry_words.get().split(',')]

        # Check if size is valid and there are not more than 20 words
        if size <= 0 or len(words) > 20:
            raise ValueError

        # Create instance
        wsg = WordSearchGenerator(size, size, words)

        # Generate puzzle and solution
        puzzle = wsg.generate(words)

        # Plot and save images
        plot_puzzle(puzzle, words, wsg, filename='puzzle.png',)
        plot_puzzle(puzzle, words, wsg, solution=True, filename='solution.png')

        # Inform user of successful generation
        messagebox.showinfo("Success", "Wordsearch generated successfully!")
    except ValueError:
        # Show error message
        messagebox.showerror("Invalid input", "Please input a positive number for size and no more than 20 words.")

# Create Tkinter window
root = Tk()

root.title("Pudding Hill - Word Search Generator")
root.geometry("500x500")

# Create grid size entry field
label_gridsize = Label(root, text="Enter grid size:")
label_gridsize.pack()
entry_gridsize = Entry(root)
entry_gridsize.pack()

# Create words entry field
label_words = Label(root, text="Enter words (comma separated):")
label_words.pack()
entry_words = Entry(root)
entry_words.pack()

# Create generate button
generate_button = Button(root, text="Generate wordsearch", command=generate_wordsearch)
generate_button.pack()

root.mainloop()