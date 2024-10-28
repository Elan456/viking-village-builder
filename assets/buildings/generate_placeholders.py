from PIL import Image, ImageDraw, ImageFont

from config.defines import GRID_SIZE
from buildings.building_info import BldInfo

def generate_placeholder(grid_width, grid_height, text, output_file):
    # Create a new image with white background
    width = grid_width * GRID_SIZE
    height = grid_height * GRID_SIZE
    image = Image.new('RGB', (width, height), color='white')
    
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)
    
    # Load a font
    try:
        font = ImageFont.truetype("assets/fonts/Oldenburg-Regular.ttf", 12)
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

all_buildings = BldInfo.get_all_keys()
for building in all_buildings:
    width = BldInfo.get_width(building)
    height = BldInfo.get_height(building)
    name = BldInfo.get_name(building)
    generate_placeholder(width, height, name, f"{building}.png")

