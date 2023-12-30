from music21 import *

note1 = note.Note('C4')
note1.quarterLength = 0.5
note2 = note.Note('F#4')
note3 = note.Note('F#4')
note4 = note.Note('F#4')
note5 = note.Note('F#4')

bar1 =stream.Part()
bar1.insert(0, meter.TimeSignature('8/4'))

stream1 = stream.Stream()
stream1.append(note1)
stream1.append(note2)
stream1.append(note3)
stream1.append(note4)
stream1.append(note5)

stream1.show()