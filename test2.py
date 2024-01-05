from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from music21 import stream, meter, note
import os
import random
import threading
from fractions import Fraction
import tkinter

rhythm_patterns = [
    {"name": "sixteenth", "image": "sixteenth_note.png", "value": Fraction(1, 4)},
    {"name": "Eighth", "image": "eighth_note.jpg", "value": Fraction(1, 2)},
    {"name": "dotted-Eighth", "image": "dotted_eighth_note.png", "value": Fraction(3, 4)},
    {"name": "Quarter", "image": "quarter_note.png", "value": Fraction(1, 1)},
    {"name": "dotted-quarter", "image": "dotted-quarter.png", "value": Fraction(3, 2)},
    {"name": "Half", "image": "half_note.jpeg", "value": Fraction(2, 1)},
    {"name": "dotted-half", "image": "dotted-half.png", "value": Fraction(3, 1)},
    {"name": "Whole", "image": "whole_note.jpg", "value": Fraction(4, 1)},
    {"name": "Triplet-eighth", "image": "triplet-eighth.png", "value": Fraction(1, 3)},
    {"name": "Triplet-quarter", "image": "triplet-quarter.png", "value": Fraction(2, 3)}
]
BARS_IN_PAGE = 32


class RhythmGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rhythm Generator")

        # Create a variable to store the selected rhythm patterns
        self.selected_patterns = {}

        self.selected_triplets = {}
        self.selected_regular = {}
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

        close_button = Button(frm, text="Close", command=self.on_close_button)
        close_button.grid(column=4, row=4, columnspan=3)

        # Create buttons for each rhythm pattern
        images_directory = os.path.join(os.path.dirname(__file__), "images")

        for i, pattern in enumerate(rhythm_patterns):
            if 'rest' in pattern['image']:
                continue
            image_path = os.path.join(images_directory, pattern["image"])
            image = Image.open(image_path).resize((50, 50), resample=Image.HAMMING)
            photo = ImageTk.PhotoImage(image)

            column = i % 6
            row = i // 6 + 1

            button = ttk.Checkbutton(frm, text=pattern["name"], image=photo, compound="top",
                                     command=lambda p=pattern: self.toggle_pattern(p, button))
            button.image = photo
            button.grid(column=column, row=row, padx=5, pady=5)


    def toggle_pattern(self, pattern, button):
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
            self.selected_patterns[pattern["name"]] = pattern["value"]
            rest_name = f"rest-{pattern['name']}"
            self.selected_patterns[rest_name] = Fraction(1, 3) if pattern["name"] == "Triplet-eighth" else pattern["value"]

        # Update the selected triplets dictionary
        self.update_selected_triplets()
        self.update_selected_regular()

    def update_selected_triplets(self):
        self.selected_triplets = {name: value for name, value in self.selected_patterns.items() if "Triplet" in name}
    
    def update_selected_regular(self):
        self.selected_regular = {name: value for name, value in self.selected_patterns.items() if not "Triplet" in name}  

    def generate_oneBar(self):

        bar_length = Fraction(4, 1)
        bar = Fraction(0, 1)
        selected_rhythm = []
        eighth_triplet = Fraction(1, 3)
        quarter_triplet = Fraction(2, 3)
        quarter = Fraction(1, 1)
        fourth_beat = Fraction(3, 1)
        tries = 0
        max_tries = 20

        while bar < bar_length and self.selected_patterns and (self.selected_regular or self.selected_triplets):
            selected_note_name = random.choice(list(self.selected_patterns))
            selected_note = self.selected_patterns[selected_note_name]
            if tries >= max_tries:
                error_message = "Exceeded maximum number of tries. Unable to generate valid rhythm."
                tkinter.messagebox.showerror("Error", error_message)
                raise ValueError(error_message)
            
            if selected_note + bar > bar_length:
                tries += 1
                continue

            elif bar % quarter == 0 and bar + selected_note <= bar_length and selected_note:
                if selected_note == eighth_triplet:
                    triplet_notes = self.generate_eighth_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))

                elif selected_note == quarter_triplet and bar == fourth_beat:
                    triplet_notes = self.generate_eighth_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))   

                elif selected_note == quarter_triplet:
                    triplet_notes = self.generate_quarter_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))

                elif self.selected_regular:
                    bar += selected_note                    
                    selected_rhythm.append((selected_note_name, selected_note))

            elif bar + selected_note <= bar_length and self.selected_regular:
                selected_note_name = random.choice(list(self.selected_regular))
                selected_note = self.selected_regular[selected_note_name]
                while selected_note + bar > bar_length:
                    selected_note_name = random.choice(list(self.selected_regular))
                    selected_note = self.selected_regular[selected_note_name]
                bar += selected_note
                selected_rhythm.append((selected_note_name, selected_note))

        # print(f"Bar: {selected_rhythm}")
        return selected_rhythm
    
    def generate_eighth_triplets(self):
        triplets_notes = []
        quarter = Fraction(1, 1)
        total = Fraction(0, 1)

        while total < quarter:
            selected_note_name = random.choice(list(self.selected_triplets))
            selected_note = self.selected_triplets[selected_note_name]

            if total + selected_note > quarter:
                continue

            total += selected_note
            triplets_notes.append((selected_note_name, selected_note))

        return triplets_notes
        
    def generate_quarter_triplets(self):
        triplet_notes = []
        half = Fraction(2, 1)
        total = Fraction(0, 1)

        while total < half:
            selected_note_name = random.choice(list(self.selected_triplets))
            selected_note = self.selected_triplets[selected_note_name]
            if total + selected_note > half:
                continue

            if total == Fraction(5, 3):
                while selected_note != Fraction(1, 3):
                    selected_note_name = random.choice(list(self.selected_triplets))
                    selected_note = self.selected_triplets[selected_note_name]
            total += selected_note
            triplet_notes.append((selected_note_name, selected_note))

        return triplet_notes

    def generate_rhythms(self):
        for bar in range(BARS_IN_PAGE):
            try:
                rhythm = self.generate_oneBar()
                yield rhythm
            except StopIteration:
                print("StopIteration in generate_rhythms")


    def create_music_stream(self, rhythms):
        music_stream = stream.Stream()
        music_stream.append(meter.TimeSignature('4/4'))

        for rhythm in rhythms:
            measure = stream.Measure()

            for index, (note_name, duration) in enumerate(rhythm, start=1):
                choices = [note.Note('C4'), note.Rest()]
                probability = [0.8, 0.2]
                n = random.choices(choices, weights=probability)[0]
                # print(f"Iteration {index}: {duration}")
                n.quarterLength = duration
                measure.append(n)

            music_stream.append(measure)

        return music_stream


    def on_generate_button(self):
        threading.Thread(target=self.generate_and_show_music).start()


    def generate_and_show_music(self):
        try:
            rhythms = list(self.generate_rhythms())
            music_stream = self.create_music_stream(rhythms)
            music_stream.show()
            print("Generation complete")

        except StopIteration:
            print("Generation complete")

        except ValueError:
            pass

    def on_close_button(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = RhythmGeneratorApp(root)
    root.mainloop()