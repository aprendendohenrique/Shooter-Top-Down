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

    @staticmethod
    def choose_dir():
        root = tk.Tk()
        root.withdraw()

        path = Path(filedialog.askdirectory())
        root.destroy()

        return path

    @staticmethod
    def save_json():
        root = tk.Tk()
        root.withdraw()

        path = Path(filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")]))
        root.destroy()

        return path