import cv2
from time import time
from platform import system
from os import get_terminal_size
# pip install opencv-python / pip3 install opencv-python


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


def main():
    """
    Open the webcam put it in parameter of the fonction 'image_to_ascii'.
    :return: None
    """
    try:
        get_terminal_size()
    except OSError:
        raise Exception(f"{BColors.BOLD}Please use this program in a terminal window...")

    camera = cv2.VideoCapture(0)

    # If a webcam is opened, the program continue, else, it stop.
    if camera.isOpened():
        rval, frame = camera.read()
    else:
        rval = False
        raise Exception('\n\nNo webcam detected...')

    while rval:
        rval, frame = camera.read()
        frame = cv2.flip(frame, 1)
        converted_data = image_to_ascii(frame)

        # Print converted image.
        print(f"{converted_data[1]}\n{converted_data[0]}")

        # 50ms pause -> ~20fps
        key = cv2.waitKey(50)
        # Press echap to end
        if key == 27:
            break


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


def image_to_ascii(img):
    """
    :param img: Image from the webcam.
    :return: Information and converted image.
    """
    # Initialise converted_img (string with converted pixel into char).
    converted_img = ""

    # Initialise char_list (every char needed to draw an image)
    char_list = [" ", ".", ":", "-", "=", "+", "#", "%", "@"]

    # Start a timer.
    start = time()

    # Calculate new dimension for the image to fit into the terminal window.
    height, width, color = img.shape
    terminal_size = get_terminal_size()

    new_height = terminal_size.lines
    new_width = int(((width / height) * new_height) / 0.55)

    # If the width is too high, recalculate the height with the terminal width to fit into it.
    if new_width <= terminal_size.columns:
        aspect_ratio_size = (new_width, new_height)
    else:
        aspect_ratio_size = (terminal_size.columns, int(terminal_size.columns * (new_height / new_width)))

    # Put the image into grayscaled mode.
    grayscaled_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    grayscaled_img = cv2.resize(grayscaled_img, aspect_ratio_size)

    size_y, size_x = grayscaled_img.shape

    # Convert every pixel of the image into chars.
    for y in range(size_y - 1):
        y_line = ""
        for x in range(size_x - 1):
            y_line += char_list[int(translate(grayscaled_img[y, x], 0, 255, 0, len(char_list) - 1))]
        converted_img += y_line + "\n"

    # End the timer.
    end = time()

    # Return some info (time, size of the image.) and the converted image.
    return (f"\n{BColors.BOLD}image size :{BColors.ENDC} x = {BColors.BOLD}{size_x}{BColors.ENDC},"
            f" y = {BColors.BOLD}{size_y}{BColors.ENDC}, "
            f"{BColors.BOLD}terminal size :{BColors.ENDC} columns : {terminal_size.columns}, "
            f"lines : {terminal_size.lines}, aspect ratio : {aspect_ratio_size}, "
            f"{BColors.BOLD}time :{BColors.ENDC} render ended in {BColors.BOLD}{end - start}{BColors.ENDC} "
            f"second{'s' if end - start > 2 else ''}. ", converted_img + "\n")


if __name__ == "__main__":
    main()  # Run the main function.
