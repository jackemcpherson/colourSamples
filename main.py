from PIL import Image

def create_image(width, height, color):
    # Create an image with the given color
    img = Image.new('RGB', (width, height), color=color)
    
    # Save the image
    img.save(f'output_files/{color}.jpg')

if __name__ == '__main__':
    width = int(input('Enter the width of the image: '))
    height = int(input('Enter the height of the image: '))
    color = input('Enter the color code (in HTML format): ')
    
    # Remove '#' from the start of the color code if it exists
    if color.startswith('#'):
        color = color[1:]

    # Convert the color code to RGB
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    create_image(width, height, color)