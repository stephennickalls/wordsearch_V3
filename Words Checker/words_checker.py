def read_unique_words(filename="unique_words.txt"):
    with open(filename, 'r') as f:
        content = f.read()
        return set(content.split(',')) if content else set()

def read_words_to_check(filename="words_to_check.txt"):
    with open(filename, 'r') as f:
        # Extracting words from the comma separated list and removing leading and trailing whitespaces
        return set(word.strip() for word in f.read().split(','))

def write_unique_words(words, filename="unique_words.txt"):
    with open(filename, 'a') as f:
        # Appending a comma before new words if the file isn't empty
        f.write(',' + ','.join(words) if f.tell() else ','.join(words))
    
    # Return total number of words after the update
    with open(filename, 'r') as f:
        return len(f.read().split(','))

def main():
    unique_words = read_unique_words()
    words_to_check = read_words_to_check()

    common_words = unique_words.intersection(words_to_check)

    if common_words:
        print("Some words in this list were already in unique_words.txt:")
        print(", ".join(common_words))
    else:
        write_unique_words(words_to_check)
        total_words = len(unique_words.union(words_to_check))
        print(f"All words were unique and have been added to the unique_words.txt file. Total number of words: {total_words}.")

if __name__ == "__main__":
    main()
