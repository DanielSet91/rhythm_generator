from music21 import *

def print_note_info(note):
    print(f"Duration: {note.duration.quarterLength}")
    print(f"Offset: {note.offset}")
    print()

def print_musicxml_info(file_path):
    # Load the MusicXML file
    score = converter.parse(file_path)

    # Iterate through all elements in the score
    for element in score.recurse():
        if 'Note' in element.classes:
            print_note_info(element)

# Replace 'your_file.musicxml' with the path to your MusicXML file
file_path = 'C:\\Users\\USER\\VsCode\\rhythm_generator\\legit.musicxml'
print_musicxml_info(file_path)
