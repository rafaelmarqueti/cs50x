def main():
    height = get_height()
    print_pyramid(height)
    
    
def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if height > 0 and height <= 8:
                return height
        except ValueError:
            continue
        
        
def print_pyramid(height):
    for i in range(height):
        blocks_num = i + 1
        spaces_num = height - blocks_num
        print(" " * spaces_num, end="")
        print("#" * blocks_num)
        
        
main()
