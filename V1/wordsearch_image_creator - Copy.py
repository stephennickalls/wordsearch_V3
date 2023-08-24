import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from fpdf import FPDF
from wordsearch_generator import WordSearchGenerator

def generate_puzzle(words, wsg):
    # wsg = WordSearchGenerator(30, 30, words)
    grid = wsg.generate(words)
    return grid

def plot_puzzle(grid, words, solution=False, filename='puzzle.png'):
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

# Read the CSV file

df = pd.read_csv('words.csv')
print(type(df))
words = df.values.tolist()

# create instance
wsg = WordSearchGenerator(30, 30, words)

# Generate puzzle and solution
puzzle = generate_puzzle(words, wsg)

# Plot and save images
plot_puzzle(puzzle, words, filename='puzzle.png')
plot_puzzle(puzzle, words, solution=True, filename='solution.png')

# Convert images to PDF
# images_to_pdf(['puzzle.png', 'solution.png'], 'puzzle.pdf')
