"""
Optimized Python file for image and GIF processing in the ISLify application.
"""

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import string

class ImageLabel(tk.Label):
    """
    A custom Tkinter Label for displaying images and animated GIFs.
    """

    def load(self, im):
        """
        Load an image or animated GIF into the label.

        Args:
            im: Path to the image file or a PIL Image object.
        """
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        self.delay = im.info.get("duration", 100)

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        """Unload the current image from the label."""
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """Display the next frame of an animated GIF."""
        if self.frames:
            self.loc = (self.loc + 1) % len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

def center_window(root):
    """
    Center the Tkinter window on the screen.

    Args:
        root: The Tkinter root window.
    """
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_right = int(screen_width / 2 - window_width / 2)
    position_down = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

def display_isl_gif(phrase):
    """
    Display an ISL gesture GIF for a given phrase.

    Args:
        phrase: The phrase to display as an ISL gesture.
    """
    root = tk.Tk()
    root.title("ISL Gesture")

    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(f"resources/isl_gifs/{phrase.lower()}.gif")

    center_window(root)

    # Close the window after 5 seconds
    root.after(5000, root.destroy)
    root.mainloop()

def display_alphabet_images(text):
    """
    Display ISL alphabet images for each character in the given text.

    Args:
        text: The text to display as ISL alphabet images.
    """
    alphabet_list = set(string.ascii_lowercase)  # Use a set for faster lookup

    root = tk.Tk()
    root.title("ISL Alphabet Images")

    lbl = tk.Label(root)
    lbl.pack()

    def show_image(index):
        if index < len(text):
            char = text[index].lower()
            if char in alphabet_list:
                image_path = f"resources/letters/{char}.jpg"
                try:
                    image = Image.open(image_path).resize((500, 500))
                    photo = ImageTk.PhotoImage(image)
                    lbl.config(image=photo)
                    lbl.image = photo
                    center_window(root)
                except FileNotFoundError:
                    print(f"Image for character '{char}' not found.")

            root.after(800, show_image, index + 1)
        else:
            root.after(800, root.destroy)

    show_image(0)
    root.mainloop()
