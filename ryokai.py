import os
import time
from PIL import Image
import imageio

# ANSI escape codes for color output in terminal
def rgb_to_ansi(r, g, b):
    """Converts RGB values to an ANSI escape code for terminal."""
    return f"\033[38;2;{r};{g};{b}m"

def scale_image(image, new_width=100):
    """Resizes an image while maintaining aspect ratio."""
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def convert_image_to_ascii(image, new_width=100):
    """Convert an image to ASCII art with color."""
    image = scale_image(image, new_width)
    ascii_image = ""

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            brightness = (r + g + b) // 3  # Calculate brightness
            char = get_ascii_char(brightness)
            color = rgb_to_ansi(r, g, b)
            ascii_image += f"{color}{char}\033[0m"  # Reset ANSI color after char
        ascii_image += "\n"

    return ascii_image

def get_ascii_char(brightness):
    """Returns a character based on brightness."""
    ASCII_CHARS = "@%#*+=-:. "  # Adjust to control density
    return ASCII_CHARS[brightness // 32]  # 0-255 brightness -> 10 levels

def gif_to_ascii_frames(gif_path, new_width=100):
    """Converts GIF to a list of colored ASCII frames."""
    frames = imageio.mimread(gif_path)
    ascii_frames = []
    
    for frame in frames:
        pil_image = Image.fromarray(frame)
        ascii_frame = convert_image_to_ascii(pil_image, new_width)
        ascii_frames.append(ascii_frame)
    
    return ascii_frames

def clear_console():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gif_in_terminal(gif_path, new_width=100, delay=0.1):
    """Prints the GIF as colored ASCII art animation in the terminal."""
    ascii_frames = gif_to_ascii_frames(gif_path, new_width)
    
    while True:
        for frame in ascii_frames:
            clear_console()
            print(frame)
            time.sleep(delay)

# Example usage
gif_path = "sogo.gif"  # Path to your GIF file
print_gif_in_terminal(gif_path, new_width=100, delay=0.1)
