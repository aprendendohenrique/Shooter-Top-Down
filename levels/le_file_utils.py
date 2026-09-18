import tkinter as tk
from tkinter import filedialog
from pathlib import Path


class FileUtils:

    @staticmethod
    def choose_image():
        root = tk.Tk()
        root.withdraw()

        path = Path(filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")]))
        root.destroy()

        return path