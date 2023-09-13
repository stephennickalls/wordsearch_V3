import random
import string

class WordSearchGenerator:
    def __init__(self, width, height, words):
        self.width = width
        self.height = height
        self.words = words
        self.grid = [['' for _ in range(width)] for _ in range(height)]
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]  # right, down, diagonal down-right, diagonal down-left
        self.placements = {}  # record placements for solution

    def generate(self, words):
        for word in words:
            word = word.upper()
            if random.choice([True, False]):  # randomly reverse the word
                word = word[::-1]
            if not self.place_word(word):
                raise Exception('Could not place all words into grid, please try generating again. Also the grid may be too small or some words may be too long')

        # fill in empty spaces with random letters
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == '':
                    self.grid[i][j] = random.choice(string.ascii_uppercase)

        return self.grid

    def place_word(self, word):
        for _ in range(2000):  # attempt to place the word 100 times
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            dx, dy = random.choice(self.directions)
            if self.can_place_word(word, start_x, start_y, dx, dy):
                self.do_place_word(word, start_x, start_y, dx, dy)
                return True
        return False

    def can_place_word(self, word, start_x, start_y, dx, dy):
        x, y = start_x, start_y
        for letter in word:
            if not (0 <= x < self.width and 0 <= y < self.height):  # out of bounds
                return False
            if self.grid[y][x] != '' and self.grid[y][x] != letter:  # cell already filled with a different letter
                return False
            x += dx
            y += dy
        return True
    
    def do_place_word(self, word, start_x, start_y, dx, dy):
        x, y = start_x, start_y
        path = []  # record path of word
        for letter in word:
            self.grid[y][x] = letter
            path.append((y, x))  # add position to path
            x += dx
            y += dy
        self.placements[word] = path  # add path to placements

    def find_word(self, word):
        return self.placements.get(word.upper(), []) or self.placements.get(word.upper()[::-1], [])

