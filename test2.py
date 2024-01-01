from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from music21 import stream, meter, note
import os
import random
import time
import threading
from fractions import Fraction

rhythm_patterns = [
    {"name": "sixteenth", "image": "sixteenth_note.png", "value": 0.25},
    {"name": "Eighth", "image": "eighth_note.jpg", "value": 0.5},
    {"name": "dotted-Eighth", "image": "dotted_eighth_note.png", "value": 0.75},
    {"name": "Quarter", "image": "quarter_note.png", "value": 1.0},
    {"name": "dotted-quarter", "image": "dotted-quarter.png", "value": 1.5},
    {"name": "Half", "image": "half_note.jpeg", "value": 2},
    {"name": "dotted-half", "image": "dotted-half.png", "value": 3.0},
    {"name": "Whole", "image": "whole_note.jpg", "value": 4.0},
    {"name": "Triplet-eighth", "image": "triplet-eighth.png", "value": Fraction(1/3)},
    {"name": "Triplet-quarter", "image": "triplet-quarter.png", "value": Fraction(2/3)}
]
BARS_IN_PAGE = 48


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
        time_signature_entry.grid(column=1, row=0, columnspan=3)

        generate_button = ttk.Button(frm, text="Generate Rhythm", command=self.on_generate_button)
        generate_button.grid(column=1, row=3, columnspan=3)

        # Create buttons for each rhythm pattern

        images_directory = os.path.join(os.path.dirname(__file__), "images")

        for i, pattern in enumerate(rhythm_patterns):
            if 'rest' in pattern['image']:
                continue
            image_path = os.path.join(images_directory, pattern["image"])
            image = Image.open(image_path).resize((50, 50), resample=Image.HAMMING)
            photo = ImageTk.PhotoImage(image)

            column = i % 6
            row = i //6 +1

            button = ttk.Checkbutton(frm, text=pattern["name"], image=photo, compound="top", command=lambda p=pattern: self.toggle_pattern(p, button))
            button.image = photo  
            button.grid(column=column, row=row, padx=5, pady=5)


    def toggle_pattern(self, pattern, button):
        # Check if the button is in the "pressed" state
        is_pressed = button.instate(['pressed'])

        # Toggle the state of the button
        if is_pressed:
            button.state(['!pressed'])
        else:
            button.state(['pressed'])

        # Toggle the pattern in the list of selected patterns
        if pattern["name"] in self.selected_patterns:
            del self.selected_patterns[pattern["name"]]
            rest_name = f"rest-{pattern['name']}"
            del self.selected_patterns[rest_name]
        else:
            self.selected_patterns[pattern["name"]] = float(pattern["value"])
            rest_name = f"rest-{pattern['name']}"
            self.selected_patterns[rest_name] = pattern["value"]

        print("Selected Rhythm Patterns:", self.selected_patterns)
            
    def generate_oneBar(self):
        bar_length = Fraction(4)
        bar = Fraction(0)
        tolerance = Fraction(1, 10)
        selected_rhythm = []

        while bar < bar_length and self.selected_patterns:
            selected_note_name = random.choice(list(self.selected_patterns))
            selected_note = Fraction(self.selected_patterns[selected_note_name])

            if selected_note == Fraction(1, 3) or selected_note == Fraction(2, 3):
                if bar + selected_note <= bar_length:
                    bar += selected_note
                    selected_rhythm.append((selected_note_name, selected_note))
            else:
                if bar + selected_note <= bar_length:
                    bar += selected_note
                    selected_rhythm.append((selected_note_name, selected_note))

        # Round the durations for MuseScore
        selected_rhythm_rounded = [(note, round(float(duration), 4)) for note, duration in selected_rhythm]

        return selected_rhythm_rounded
                

    def generate_rhythms(self):
        for bar in range(BARS_IN_PAGE):
            try:
                rhythm = self.generate_oneBar()
                yield rhythm
            except StopIteration:
                print("StopIteration in generate_rhythms")

        print("Generation complete")

    def create_music_stream(self, rhythms):
        music_stream = stream.Stream()
        
        for rhythm in rhythms:
            for note_name, duration in rhythm:
                choices = [note.Note('C4'), note.Rest()]
                probability = [0.8, 0.2]
                n = random.choices(choices, weights= (probability))[0]
                n.quarterLength = duration
                music_stream.append(n)
        return music_stream


    def on_generate_button(self):
        threading.Thread(target=self.generate_and_show_music).start()


    def generate_and_show_music(self):
        try:
            rhythms = list(self.generate_rhythms())
            music_stream = self.create_music_stream(rhythms)
            music_stream.show()
        except StopIteration:
            print("Generation complete")


if __name__ == "__main__":
    root = Tk()
    app = RhythmGeneratorApp(root)
    root.mainloop()
