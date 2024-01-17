from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from music21 import stream, meter, note
import os
import random
import threading
from fractions import Fraction
import subprocess
import configparser
import logging

rhythm_patterns = [
    {"name": "sixteenth-Triplet", "image": "Sixteenth_Note_Triplet.png", "value": Fraction(1, 6)},
    {"name": "sixteenth", "image": "sixteenth_note.png", "value": Fraction(1, 4)},
    {"name": "Eighth", "image": "eighth_note.png", "value": Fraction(1, 2)},
    {"name": "dotted-Eighth", "image": "dotted_eighth_note.png", "value": Fraction(3, 4)},
    {"name": "Quarter", "image": "quarter_note.png", "value": Fraction(1, 1)},
    {"name": "dotted-quarter", "image": "dotted_quarter.png", "value": Fraction(3, 2)},
    {"name": "Half", "image": "half_note.png", "value": Fraction(2, 1)},
    {"name": "dotted-half", "image": "dotted-half.png", "value": Fraction(3, 1)},
    {"name": "Whole", "image": "whole_note.png", "value": Fraction(4, 1)},
    {"name": "Triplet-eighth", "image": "triplet-eighth.png", "value": Fraction(1, 3)},
    {"name": "Triplet-quarter", "image": "triplet-quarter.png", "value": Fraction(2, 3)}
]
BARS_IN_PAGE = 36


class RhythmGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rhythm Generator")

        # Create a variable to store the selected rhythm patterns
        self.selected_patterns = {}

        self.selected_triplets = {}
        self.selected_regular = {}
        self.selected_sixteenth_triplets = {}

        self.num_bars_var = StringVar(value=str(BARS_IN_PAGE))
        self.output_file_path = "generated_music.xml"
        self.output_file_type = "musicxml"
        self.BARS_IN_PAGE = BARS_IN_PAGE
        self.time_signature = Fraction (4, 4)

        # Initialize variables for program selection
        self.selected_program = StringVar(value="musescore")
        self.config_file_path = os.path.join(os.path.dirname(__file__), "config.ini")
        self.output_file_path = self.load_output_file_path()
        self.musescore_path = self.load_program_path("musescore_path")
        self.sibelius_path = self.load_program_path("sibelius_path")
        self.finale_path = self.load_program_path("finale_path")

        # Configure logging
        logging.basicConfig(filename='rhythm_generator.log', level=logging.DEBUG)

        # Create GUI elements
        self.create_gui_elements()


    def create_gui_elements(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        ttk.Label(frm, text="Select Time Signature:").grid(column=0, row=0)
        time_signature_options = ["4/4", "3/4", "6/8", "2/4", "5/4", "7/8", "9/8", "12/8"] 
        self.time_signature_combobox = ttk.Combobox(frm, values=time_signature_options, state="readonly")
        self.time_signature_combobox.grid(column=1, row=0)

        ttk.Label(frm, text="Custom Time Signature:").grid(column=2, row=0)
        self.custom_time_signature_entry = ttk.Entry(frm, textvariable=self.time_signature)
        self.custom_time_signature_entry.grid(column=3, row=0)

        ttk.Label(frm, text=f"Number of Bars(default is {BARS_IN_PAGE}):").grid(column=4, row=0)
        num_bars_entry = ttk.Entry(frm, textvariable=self.num_bars_var)
        num_bars_entry.grid(column=5, row=0)

        generate_button = ttk.Button(frm, text="Generate Rhythm", command=self.on_generate_button)
        generate_button.grid(column=1, row=8, columnspan=3)

        ttk.Label(frm, text="Choose MuseScore Executable:").grid(column=0, row=6)
        choose_musescore_button = ttk.Button(frm, text="Browse", command=self.on_choose_musescore_button)
        choose_musescore_button.grid(column=1, row=6, columnspan=1)

        ttk.Label(frm, text="Choose Sibelius Executable:").grid(column=0, row=7)
        choose_sibelius_button = ttk.Button(frm, text="Browse", command=self.on_choose_sibelius_button)
        choose_sibelius_button.grid(column=1, row=7, columnspan=1)
        
        ttk.Label(frm, text="Choose Finale Executable:").grid(column=0, row=8)
        choose_finale_button = ttk.Button(frm, text="Browse", command=self.on_choose_finale_button)
        choose_finale_button.grid(column=1, row=8, columnspan=1)

        ttk.Label(frm, text="Select Program:").grid(column=0, row=4)
        musescore_radio = Radiobutton(frm, text="MuseScore", variable=self.selected_program, value="musescore")
        musescore_radio.grid(column=1, row=4, padx=5, pady=5)
        sibelius_radio = Radiobutton(frm, text="Sibelius", variable=self.selected_program, value="sibelius")
        sibelius_radio.grid(column=2, row=4, padx=5, pady=5)
        sibelius_radio = Radiobutton(frm, text="Finale", variable=self.selected_program, value="finale")
        sibelius_radio.grid(column=3, row=4, padx=5, pady=5)

        # Create buttons for each rhythm pattern
        images_directory = os.path.join(os.path.dirname(__file__), "images")

        for i, pattern in enumerate(rhythm_patterns):
            image_path = os.path.join(images_directory, pattern["image"])
            image = Image.open(image_path).resize((50, 50), resample=Image.HAMMING)
            photo = ImageTk.PhotoImage(image)

            column = i % 6
            row = i // 6 + 1

            button = ttk.Checkbutton(frm, text=pattern["name"], image=photo, compound="top",
                                     command=lambda p=pattern: self.toggle_pattern(p, button))
            button.image = photo
            button.grid(column=column, row=row, padx=5, pady=5)
            
        choose_file_button = ttk.Button(frm, text="Choose Output File", command=self.on_choose_file_button)
        choose_file_button.grid(column=1, row=3, columnspan=3)

        ttk.Label(frm, text="Created by Daniel Set").grid(column=5, row=7, columnspan=6, pady=12)
        close_button = Button(frm, text="Close", command=self.on_close_button)
        close_button.grid(column=5, row=8, columnspan=3)

    def load_program_path(self, program):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file_path):
            config.read(self.config_file_path)

        if "Paths" in config and program in config["Paths"]:
            return config["Paths"][program]
        else:
            return ""
        
    def load_output_file_path(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file_path):
            config.read(self.config_file_path)

        if "Paths" in config and "output_file_path" in config["Paths"]:
            return config["Paths"]["output_file_path"]
        else:
            return "generated_music.xml"
        
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
        else:
            self.selected_patterns[pattern["name"]] = pattern["value"]
        # Update the selected triplets dictionary
        self.update_selected_triplets()
        self.update_selected_regular()
        self.update_selected_sixteenth_triplets()

    def update_selected_triplets(self):
        self.selected_triplets = {name: value for name, value in self.selected_patterns.items() if "Triplet" in name}

    def update_selected_regular(self):
        self.selected_regular = {name: value for name, value in self.selected_patterns.items() if not "Triplet" in name}  

    # Updates selected notes so it will contain sixteenth and eighth triplets
    def update_selected_sixteenth_triplets(self):
        self.selected_sixteenth_triplets = {name: value for name, value in self.selected_triplets.items() if "quarter" not in name}

    def generate_oneBar(self):
        
        bar = Fraction(0, 1)
        selected_rhythm = []
        eighth_triplet = Fraction(1, 3)
        quarter_triplet = Fraction(2, 3)
        quarter = Fraction(1, 1)
        sixteenth_triplet = Fraction(1, 6)
        tries = 0
        max_tries = 35
        selected_time_signature = self.time_signature_combobox.get()
        custom_time_signature = self.valid_custom_time_signature()

        logging.debug("Starting rhythm generation")

        if selected_time_signature:
            beats_per_measure, note_value = map(int, selected_time_signature.split('/'))
            bar_length = Fraction(beats_per_measure, 1) * Fraction(4, note_value)


        elif custom_time_signature:
            beats, note_value = map(int, custom_time_signature.split('/'))
            bar_length = Fraction(beats, 1) * Fraction(4, note_value)

        else:
            bar_length = Fraction(4, 1)

        last_beat = bar_length - Fraction(1, 1)  
        last_eighth = bar_length - Fraction(1, 2)
        last_two_beats = bar_length - Fraction(2, 1) 

        while bar < bar_length and self.selected_patterns and (self.selected_regular or self.selected_triplets):
            selected_note_name = random.choice(list(self.selected_patterns))
            selected_note = self.selected_patterns[selected_note_name]

            if tries >= max_tries:
                error_message = "Exceeded maximum number of tries. Unable to generate valid rhythm."
                messagebox.showerror("Error", error_message)
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

                elif selected_note == quarter_triplet and bar == last_beat:
                    triplet_notes = self.generate_eighth_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))   

                elif selected_note == quarter_triplet:
                    triplet_notes = self.generate_quarter_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))

                elif selected_note == sixteenth_triplet:
                    triplet_notes = self.generate_sixteen_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))

                elif self.selected_regular:
                    bar += selected_note                    
                    selected_rhythm.append((selected_note_name, selected_note))

            elif bar% quarter == 0.5 and bar + selected_note <= bar_length and self.selected_sixteenth_triplets and selected_note == sixteenth_triplet:
                if selected_note == sixteenth_triplet:
                    triplet_notes = self.generate_sixteen_triplets()
                    for note_name, duration in triplet_notes:
                        bar += duration
                        selected_rhythm.append((note_name, duration))

            elif bar + selected_note <= bar_length and self.selected_regular:
                selected_note_name = random.choice(list(self.selected_regular))
                selected_note = self.selected_regular[selected_note_name]
                while selected_note + bar > bar_length:
                    selected_note_name = random.choice(list(self.selected_regular))
                    selected_note = self.selected_regular[selected_note_name]
                bar += selected_note
                selected_rhythm.append((selected_note_name, selected_note))

        logging.debug(f"Bar: {bar}, Selected Patterns: {self.selected_patterns}")

        return selected_rhythm


    def generate_sixteen_triplets(self):
        triplets_notes = []
        eighth_note = Fraction(1, 2)
        total = Fraction(0, 1) 


        while total < eighth_note:
            selected_note_name = random.choice(list(self.selected_sixteenth_triplets))
            selected_note = self.selected_triplets[selected_note_name]

            if total + selected_note > eighth_note:
                continue

            total += selected_note
            triplets_notes.append((selected_note_name, selected_note))

        return triplets_notes


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
        for bar in range(self.BARS_IN_PAGE):
            try:
                rhythm = self.generate_oneBar()
                yield rhythm
            except StopIteration:
                print("StopIteration in generate_rhythms")

    def valid_custom_time_signature(self):
        selected_time_signature = self.time_signature_combobox.get()
        custom_time_signature = self.custom_time_signature_entry.get()
        valid_quarter_note = [2, 4, 8, 16, 32]

        if custom_time_signature:
            try:
                beats, quarter_note = custom_time_signature.split("/")
                try:
                    beats, quarter_note = map(int, (beats, quarter_note))
                except ValueError:
                    messagebox.showerror("Can accept only numbers", f"invalid: {beats}, {quarter_note}. Please put only regular numbers in the custom time signature")

                if quarter_note not in valid_quarter_note:
                    raise ValueError
                elif beats <= 0 or beats > 60:
                    raise ValueError
                else:
                    custom_time_signature = f"{beats}/{quarter_note}"

            except ValueError:
                messagebox.showerror("Invalid time signature formant", "Please check the time signature format. example: 4/4, 7/8")
            except TypeError:
                messagebox.showerror("Unexcepted error occured", "Please check the time signature format. example: 4/4, 7/8")

        if selected_time_signature and custom_time_signature:
            messagebox.showerror("Two time signatures", f"Cant make time signature of {selected_time_signature} and {custom_time_signature}")
            raise ValueError
        
        return custom_time_signature
    

    def create_music_stream(self, rhythms):
        music_stream = stream.Stream()
        selected_time_signature = self.time_signature_combobox.get()
        custom_time_signature = self.valid_custom_time_signature()
        

        if selected_time_signature:
            music_stream.append(meter.TimeSignature(self.time_signature_combobox.get()))
        elif custom_time_signature:
            music_stream.append(meter.TimeSignature(custom_time_signature))
        else:
            music_stream.append(meter.TimeSignature('4/4'))

        for rhythm in rhythms:
            measure = stream.Measure()

            for note_name, duration in rhythm:
                choices = [note.Note('C4'), note.Rest()]
                probability = [0.8, 0.2]
                n = random.choices(choices, weights=probability)[0]
                n.quarterLength = duration
                measure.append(n)

            music_stream.append(measure)

        return music_stream


    def on_generate_button(self):
        num_bars_str = self.num_bars_var.get()

        try:
            num_bars = int(num_bars_str)
            if num_bars <= 0:
                raise ValueError
            self.BARS_IN_PAGE = num_bars
        except ValueError:
            messagebox.showinfo("Invalid input", f"invalid input. using default value of {self.BARS_IN_PAGE}.")
            print(f"invalid input: {num_bars_str}. using default value.")
    
        threading.Thread(target=self.generate_and_show_music).start()

    def on_choose_musescore_button(self):
        musescore_path = filedialog.askopenfilename(title="Select MuseScore Executable", filetypes=[("Executable files", "*.exe")])
        if musescore_path:
            self.musescore_path = musescore_path
            self.save_program_path("musescore_path", musescore_path)

    def on_choose_sibelius_button(self):
        sibelius_path = filedialog.askopenfilename(title="Select Sibelius Executable", filetypes=[("Executable files", "*.exe")])
        if sibelius_path:
            self.sibelius_path = sibelius_path
            self.save_program_path("sibelius_path", sibelius_path)

    def on_choose_finale_button(self):
        finale_path = filedialog.askopenfilename(title="Select Finale Executable", filetypes=[("Executable files", "*.exe")])
        if finale_path:
            self.finale_path = finale_path
            self.save_program_path("finale_path", finale_path)

    def save_program_path(self, program, path):
        config = configparser.ConfigParser()

        if os.path.exists(self.config_file_path):
            config.read(self.config_file_path)

        if "Paths" not in config:
            config["Paths"] = {}

        config["Paths"][program] = path
        config["Paths"]["output_file_path"] = self.output_file_path


        with open(self.config_file_path, "w") as config_file:
            config.write(config_file)

    def on_choose_file_button(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("MusicXML files", "*.xml"), ("MIDI files", "*.midi;*.mid"), ("Sibelius/MuseScore files", "*.sib;*.mscz")])
        if file_path:
            self.output_file_path = file_path
            _, file_extension = os.path.splitext(file_path)
            self.output_file_type = file_extension.lstrip(".") if file_extension else "musicxml"

    def generate_and_show_music(self):
        selected_program = self.selected_program.get()

        try:
            rhythms = list(self.generate_rhythms())
            music_stream = self.create_music_stream(rhythms)

            if selected_program == "musescore":
                print(f"Using MuseScore path: {self.musescore_path}")
                music_stream.show("musicxml", options=[self.musescore_path])

            elif selected_program == "sibelius":
                print(f"Using Sibelius path: {self.sibelius_path}")
                subprocess.run([self.sibelius_path, self.output_file_path])

            elif selected_program == "finale":
                print(f"using finale path: {self.finale_path}")
                subprocess.run([self.finale_path, self.output_file_path])

            else:
                music_stream.show()
            try:
                music_stream.write(self.output_file_type, fp=self.output_file_path)
                logging.debug(f"Music saved to: {self.output_file_path}")
                messagebox.showinfo("Generation Complete!", f"Music save to: {self.output_file_path}")
                print(f"Generation complete. Music saved to: {self.output_file_path}")

            except Exception as e:
                print(f"Error while saving the file: {e}")

            messagebox.showinfo("Generation complete", f"generation completed and saved to: {self.output_file_path}")
            logging.debug("Rhythm generation complete")
            print("Generation complete")

        except StopIteration:
            print("Generation complete")
        except Exception as e:
            print(f"Error during rhythm generation: {e}")
            messagebox.showerror("Error", f"Error during rhythm generation: {e}")

    def on_close_button(self):
        self.root.destroy()
