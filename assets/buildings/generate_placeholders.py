from PIL import Image, ImageDraw, ImageFont

from config.defines import *

def generate_placeholder(grid_width, grid_height, text, output_file):
    # Create a new image with white background
    width = grid_width * GRID_SIZE
    height = grid_height * GRID_SIZE
    image = Image.new('RGB', (width, height), color='white')
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)
    
    # Load a font
    try:
        font = ImageFont.truetype("assets/fonts/Oldenburg-Regular.ttf", 102)
    except IOError:
        print("Font not found, using default font")
        font = ImageFont.load_default(size=32)
    
    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Draw the text on the image
    draw.text((text_x, text_y), text, fill="black", font=font)
    
    # Save the image
    output_dir = "assets/buildings/"
    image.save(output_dir + output_file)

# Generate each building

generate_placeholder(3, 3, "Grain Field", "grain_field.png")
generate_placeholder(1, 1, "Mine", "mine.png")
generate_placeholder(3, 2, "Lumber Mill", "lumber_mill.png")

generate_placeholder(2, 2, "Blacksmith", "blacksmith.png")
generate_placeholder(4, 2, "Shipwright", "shipwright.png") 

