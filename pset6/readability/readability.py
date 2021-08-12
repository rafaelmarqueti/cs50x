def main():
    text = input("text: ")
    letters, words, sentences = get_text_stats(text)
    coleman_index = calculate_coleman(letters, words, sentences)
    print_grade(coleman_index)
    
    
def get_text_stats(text):
    letters = 0
    words = 1
    sentences = 0
    
    for letter in text:
        if letter.isalpha():
            letters += 1
        elif letter == " ":
            words += 1
        elif letter in [".", "!", "?"]:
            sentences += 1
            
    print(f"{letters} letter(s)")
    print(f"{words} word(s)")
    print(f"{sentences} sentence(s)")
    
    return letters, words, sentences
    
    
def calculate_coleman(letters, words, sentences):
    coleman_L = letters * 100 / words
    coleman_S = sentences * 100 / words
    return round(0.0588 * coleman_L - 0.296 * coleman_S - 15.8)
     
     
def print_grade(coleman_index):
    if coleman_index >= 16:
        print("Grade 16+")
    elif coleman_index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {coleman_index}")
        
        
main()
