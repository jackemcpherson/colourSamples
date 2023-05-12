from PIL import Image

def create_image(width, height, color_code):
    # Create an image with the given color
    img = Image.new('RGB', (width, height), color=color_code)
    
    # Remove '#' from the start of the color code for the filename if it exists
    if color_code.startswith('#'):
        color_code = color_code[1:]
    
    # Save the image
    img.save(f'output_files/{color_code}.jpg')

if __name__ == '__main__':
    width = int(input('Enter the width of the image: '))
    height = int(input('Enter the height of the image: '))
    color = input('Enter the color code (in HTML format): ')
    
    create_image(width, height, color)
