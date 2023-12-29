from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # Make sure to install the Pillow library for working with images
import os
import random

rhythm_patterns = [
    {"name": "Quarter", "image": "quarter_note.png", "value": 0.25},
    {"name": "Eighth", "image": "eighth_note.jpg", "value": 0.125},
    {"name": "Half", "image": "half_note.jpeg", "value": 0.5},
    {"name": "Whole", "image": "whole_note.jpg", "value": 1}
]

BARS_IN_PAGE = 32

class RhythmGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rhythm Generator")

        # Create a variable to store the selected rhythm patterns
        self.selected_patterns = {}

        # Create GUI elements
        self.create_gui_elements()

    def create_gui_elements(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        # Time Signature Label and Entry
        ttk.Label(frm, text="Time Signature:").grid(column=0, row=0)
        time_signature_entry = ttk.Entry(frm)
        time_signature_entry.grid(column=1, row=0)

        generate_button = ttk.Button(frm, text="Generate Rhythm", command= self.generate_rhythm)
        generate_button.grid(column=1, row=3)

        # Create buttons for each rhythm pattern

        images_directory = os.path.join(os.path.dirname(__file__), "images")

        for i, pattern in enumerate(rhythm_patterns):
            image_path = os.path.join(images_directory, pattern["image"])
            print(f"Checking image path: {image_path}")  # Debugging line
            image = Image.open(image_path).resize((50, 50), resample=Image.HAMMING)
            photo = ImageTk.PhotoImage(image)
            
            button = ttk.Checkbutton(frm, text=pattern["name"], image=photo, compound="top", command=lambda p=pattern: self.toggle_pattern(p, button))
            button.image = photo  # Keep a reference to avoid garbage collection
            button.grid(column=i, row=1, padx=5, pady=5)

    def toggle_pattern(self, pattern, button):
        # Toggle the state of the button (pressed or not pressed)
        button.state(['pressed'] if pattern["name"] not in self.selected_patterns else [])

        # Toggle the pattern in the list of selected patterns
        if pattern["name"] in self.selected_patterns:
            del self.selected_patterns[pattern["name"]]
        else:
            self.selected_patterns[pattern["name"]] = float(pattern["value"])

        print("Selected Rhythm Patterns:", self.selected_patterns)

    def generate_oneBar(self):
        bar_length = 1
        bar = 0
        selected_rhythm = []
        
        while bar < bar_length:
            selected_note_name = random.choice(list(self.selected_patterns))
            selected_note = self.selected_patterns[selected_note_name]

            print(selected_note, selected_note_name)
            
            if bar + selected_note <= bar_length:
                bar += selected_note
                selected_rhythm.append((selected_note_name, selected_note))

        print(selected_rhythm)
        return bar
            
    def generate_rhythm(self):
        for bar in BARS_IN_PAGE:
            rhythm = self.generate_oneBar
            yield rhythm



if __name__ == "__main__":
    root = Tk()
    app = RhythmGeneratorApp(root)
    root.mainloop()
