from PIL import Image

def create_image(width, height, color_code):
    # Remove '#' from the start of the color code if it exists
    if color_code.startswith('#'):
        color_code = color_code[1:]
    
    # Convert the color code to RGB
    color_rgb = tuple(int(color_code[i:i+2], 16) for i in (0, 2, 4))

    # Create an image with the given color
    img = Image.new('RGB', (width, height), color=color_rgb)
    
    # Save the image
    img.save(f'output_files/{color_code}.jpg')

if __name__ == '__main__':
    width = int(input('Enter the width of the image: '))
    height = int(input('Enter the height of the image: '))
    color = input('Enter the color code (in HTML format): ')
    
    create_image(width, height, color)
