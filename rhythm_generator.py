import random

def generate_rhythm_pattern(time_signature, num_beats):
    note_durations = [1, 2, 4, 8]  # Whole, half, quarter, eighth notes
    rhythm_pattern = []

    for _ in range(num_beats):
        duration = random.choice(note_durations)
        rhythm_pattern.append(duration)

    return rhythm_pattern

# Example usage
time_signature = "4/4"
num_beats = 8
generated_pattern = generate_rhythm_pattern(time_signature, num_beats)
print("Generated Rhythm Pattern:", generated_pattern)