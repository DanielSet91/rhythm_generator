import unittest
from tkinter import Tk
from fractions import Fraction
from rhythm_generator import RhythmGeneratorApp

class RhythmGeneratorAppTest(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = RhythmGeneratorApp(self.root)

        self.app.selected_patterns = {"sixteenth-Triplet": Fraction(1, 6)}

        self.app.update_selected_triplets()
        self.app.update_selected_sixteenth_triplets()

    # Destroy the Tkinter instance after the test
    def tearDown(self):
        self.root.destroy()

    # Check if the total duration is equal to one eighth note
    def test_generate_sixteen_triplets(self):
        triplets_notes = self.app.generate_sixteen_triplets()

        total_duration = sum(note[1] for note in triplets_notes)

        self.assertEqual(total_duration, Fraction(1, 2))

    # Test with a valid normal time signature
    def test_valid_custom_time_signature_normal(self):
        self.app.custom_time_signature_entry.delete(0, "end") 
        self.app.custom_time_signature_entry.insert(0, "15/16")

        try:
            self.app.valid_custom_time_signature()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

    # Tests the generate one bar
    def test_generate_oneBar(self):
        self.app.selected_patterns = {"Quarter": 0.25, "Eighth": 0.125}
        self.app.selected_regular = {"Quarter": 0.25, "Eighth": 0.125}
        self.app.time_signature_combobox.set("4/4")

        generated_rhythm = self.app.generate_oneBar()

        total_duration = sum(note[1] for note in generated_rhythm)

        self.assertIsInstance(generated_rhythm, list, "Generated rhythm should be a list")
        self.assertGreater(len(generated_rhythm), 0, "Generated rhythm should not be empty")

        total_duration = sum(note[1] for note in generated_rhythm)
        self.assertAlmostEqual(total_duration, 4.0, delta=0.01, msg="Total duration should be approximately one bar")

    def test_toggle_pattern(self):
        pattern = {"name": "Quarter", "image": "quarter_note.png", "value": Fraction(1, 1)}
        button = MockButton()

        self.app.toggle_pattern(pattern, button)

        self.assertIn("Quarter", self.app.selected_patterns, "Quarter note should be in selected patterns")
        self.assertEqual(button.instate(['pressed']), True, "Button should be in pressed state")

class MockButton:
    def __init__(self):
        self.state_info = []

    def state(self, new_state=None):
        if new_state:
            self.state_info = new_state
        return self.state_info

    def instate(self, states):
        return all(state in self.state_info for state in states)

if __name__ == '__main__':
    unittest.main()
