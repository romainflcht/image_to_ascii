from time import time
from platform import system
from os import get_terminal_size
from PIL import Image, ImageFile
# pip install Pillow

ImageFile.LOAD_TRUNCATED_IMAGES = True


class BColors:
    """
    Bcolors : 
        - Set text style when printing something.
    """
    if system() in ('Linux', 'Darwin'):
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    else:
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''


def translate(value, left_min, left_max, right_min, right_max):
    """
    :param value: Value (int) to translate.
    :param left_min: Minimum value for the first interval mapping.
    :param left_max: Maximum value for the first interval mapping.
    :param right_min: Minimum value for the second interval mapping.
    :param right_max: Maximum value for the second interval mapping.
    :return: Return mapped value.
    """
    value_scaled = float(value - left_min) / float(left_max - left_min)
    return right_min + (value_scaled * right_max - right_min)


if __name__ == '__main__':
    # Initialise char_list (every char needed to draw an image) and converted_img (list with converted pixel into char).
    char_list = [" ", ".", ":", "-", "=", "+", "#", "%", "@"]
    converted_img = []

    try:
        get_terminal_size()
    except OSError:
        raise Exception(f"{BColors.BOLD}Please use this program in a terminal window...")

    # Ask the user the path of the image and the size of his terminal.
    path = input(f"Put image {BColors.BOLD}path{BColors.ENDC} here : ")

    # Start a timer to see how much time the program takes to run.
    start = time()

    # Open the image and convert it to grayscale.
    terminal_size = get_terminal_size()
    try:
        img = Image.open(path).convert('L')
    except FileNotFoundError:
        raise Exception(f'\n\n{path} - File not found, abort...')

    width, height = img.size

    # Calculate new width and height to fit into the terminal window.
    new_height = terminal_size.lines
    new_width = int(((width / height) * new_height) / 0.55)

    # If the width is too high, recalculate the height with the terminal width to fit into it.
    if new_width <= terminal_size.columns:
        aspect_ratio_size = (new_width, new_height)
    else:
        aspect_ratio_size = (terminal_size.columns, int(terminal_size.columns * (new_height / new_width)))

    # Resize the image to the terminal size (keep the aspect ratio).
    img = img.resize(aspect_ratio_size)
    size_y, size_x = img.size

    # Load img pixel into 'pix'.
    pix = img.load()

    # Append char into converted_img in use of the value of the pixel.
    for x in range(size_x):
        x_line = []
        for y in range(size_y):
            x_line.append(char_list[int(translate(pix[y, x], 0, 255, 0, len(char_list) - 1))])
        converted_img.append(x_line)

    # Print the image from converted_img.
    for elt in converted_img:
        for char in elt:
            print(char, end="")
        print()

    # Stop the timer.
    end = time()

    # Print the end text (size of the image, path and time).
    print(f"\n{BColors.BOLD}image size :{BColors.ENDC} x = {BColors.BOLD}{size_x}{BColors.ENDC},"
          f" y = {BColors.BOLD}{size_y}{BColors.ENDC}, "
          f"{BColors.BOLD}terminal size :{BColors.ENDC} columns : {terminal_size.columns}, "
          f"lines : {terminal_size.lines}, aspect ratio : {aspect_ratio_size}, "
          f" file {BColors.BOLD}path :{BColors.ENDC} {path}, "
          f"{BColors.BOLD}time :{BColors.ENDC} program ended in {BColors.BOLD}{end - start}{BColors.ENDC} "
          f"second{'s' if end - start > 2 else ''}. ")
