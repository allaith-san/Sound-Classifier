import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import librosa
import numpy as np
import os
import threading
import platform
import subprocess
from PIL import Image, ImageTk

def play_sound(file_path, play_audio):
    if not play_audio:
        return

    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", file_path])
        else:
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        print(f"An error occurred while playing the audio: {e}")

def analyze_audio(file_path, play_audio):
    result_label.config(text="Processing...", fg="white")
    debug_label.config(text="")

    y, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    debug_info = f"Audio duration: {duration:.2f} seconds\n"

    result = is_melodic(y, sr)
    result_label.config(text=result[0], fg=result[1])  # Set result color
    debug_info += result[2]
    debug_label.config(text=debug_info)

    threading.Thread(target=play_sound, args=(file_path, play_audio)).start()

def is_harmonic_interval(interval, tolerance=2):
    harmonic_intervals = [2, 4, 5, 7, 9, 11, 12]
    return any(abs(interval - h) <= tolerance for h in harmonic_intervals)

def pitch_to_note(pitch):
    if pitch <= 0:
        return None
    midi_number = 69 + 12 * np.log2(pitch / 440.0)
    return round(midi_number)

def is_melodic(y, sr):
    max_note_shifts = max_note_shifts_slider.get()
    pitch_threshold = pitch_threshold_slider.get()
    min_note_duration = min_note_duration_slider.get()
    harmony_threshold = harmony_slider.get()

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    pitch_values = []
    for magnitude, pitch in zip(magnitudes.T, pitches.T):
        max_idx = magnitude.argmax()
        if magnitude[max_idx] > pitch_threshold:
            pitch_val = pitch[max_idx]
            if pitch_val > pitch_threshold:
                pitch_values.append(pitch_val)
    
    pitch_values = np.array(pitch_values)
    
    if len(pitch_values) == 0:
        return "Non-melodic Sound ❌", "red", ""

    time_frames = np.linspace(0, len(y) / sr, len(pitch_values))
    intervals = np.diff(time_frames, prepend=0)
    note_durations = np.cumsum(intervals)
    
    valid_notes = [pitch for pitch, duration in zip(pitch_values, note_durations) if duration > min_note_duration]
    
    if len(valid_notes) < 2:
        return "Non-melodic Sound ❌", "red", ""

    notes = [pitch_to_note(pitch) for pitch in valid_notes if pitch_to_note(pitch) is not None]

    if len(notes) < 2:
        return "Non-melodic Sound ❌", "red", ""

    note_changes = 0
    harmonic_changes = 0

    for i in range(1, len(notes)):
        prev_note = notes[i - 1]
        curr_note = notes[i]

        pitch_change = np.abs(valid_notes[i] - valid_notes[i - 1])
        if pitch_change > pitch_threshold:
            note_changes += 1

            interval = np.abs(curr_note - prev_note)
            if is_harmonic_interval(interval):
                harmonic_changes += 1

    if note_changes > 0:
        harmonic_ratio = harmonic_changes / note_changes
    else:
        harmonic_ratio = 0

    debug_info = (
        f"Number of valid note shifts = {note_changes}\n"
        f"Number of harmonic changes = {harmonic_changes}\n"
        f"Harmonic ratio = {harmonic_ratio:.2f}\n"
    )
    
    result_text = "Melodic Sound ✅" if note_changes >= max_note_shifts and harmonic_ratio > harmony_threshold else "Non-melodic Sound ❌"
    result_color = "green" if "✅" in result_text else "red"
    
    return result_text, result_color, debug_info

def on_drop(event):
    file_path = event.data.strip('{}')
    print(f"File dropped: {file_path}")

    play_audio = play_audio_var.get()

    threading.Thread(target=analyze_audio, args=(file_path, play_audio)).start()

def main():
    global play_audio_var, result_label, max_note_shifts_slider, pitch_threshold_slider, harmony_slider, min_note_duration_slider, debug_label

    root = TkinterDnD.Tk()
    root.title("Sound Classifier")
    root.geometry("700x600")
    root.resizable(False, False)
    root.configure(bg="#1E1E1E")

    # Drag and drop area with icon
    drag_drop_icon = Image.open("assets/drag_drop_icon.png")
    drag_drop_icon = drag_drop_icon.resize((50, 50), Image.Resampling.LANCZOS)
    drag_drop_icon = ImageTk.PhotoImage(drag_drop_icon)

    lb = tk.Label(root, text="Drag & Drop an audio file here", padx=10, pady=10, bg="#2C2C2C", fg="white", relief=tk.RAISED, font=("Helvetica", 12, "bold"))
    lb.config(image=drag_drop_icon, compound=tk.LEFT)
    lb.pack(pady=20, fill=tk.BOTH, expand=True)
    lb.drop_target_register(DND_FILES)
    lb.dnd_bind('<<Drop>>', on_drop)

    play_audio_var = tk.BooleanVar(value=True)
    play_audio_checkbox = tk.Checkbutton(root, text="Play audio file", variable=play_audio_var, bg="#1E1E1E", fg="white", selectcolor="#333333", font=("Helvetica", 10))
    play_audio_checkbox.pack(pady=5)

    tk.Label(root, text="Max Note Shifts", bg="#1E1E1E", fg="white", font=("Helvetica", 10)).pack()
    max_note_shifts_slider = tk.Scale(root, from_=0, to=20, orient=tk.HORIZONTAL, bg="#2C2C2C", fg="white", troughcolor="#444444", sliderrelief=tk.FLAT, font=("Helvetica", 10))
    max_note_shifts_slider.set(10)
    max_note_shifts_slider.pack(fill=tk.X, padx=20, pady=5)

    tk.Label(root, text="Pitch Threshold (Hz)", bg="#1E1E1E", fg="white", font=("Helvetica", 10)).pack()
    pitch_threshold_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, bg="#2C2C2C", fg="white", troughcolor="#444444", sliderrelief=tk.FLAT, font=("Helvetica", 10))
    pitch_threshold_slider.set(25)
    pitch_threshold_slider.pack(fill=tk.X, padx=20, pady=5)

    tk.Label(root, text="Min Note Duration (s)", bg="#1E1E1E", fg="white", font=("Helvetica", 10)).pack()
    min_note_duration_slider = tk.Scale(root, from_=0, to=2, resolution=0.01, orient=tk.HORIZONTAL, bg="#2C2C2C", fg="white", troughcolor="#444444", sliderrelief=tk.FLAT, font=("Helvetica", 10))
    min_note_duration_slider.set(0.25)
    min_note_duration_slider.pack(fill=tk.X, padx=20, pady=5)

    tk.Label(root, text="Harmony Threshold", bg="#1E1E1E", fg="white", font=("Helvetica", 10)).pack()
    harmony_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, bg="#2C2C2C", fg="white", troughcolor="#444444", sliderrelief=tk.FLAT, font=("Helvetica", 10))
    harmony_slider.set(0.5)
    harmony_slider.pack(fill=tk.X, padx=20, pady=5)

    result_label = tk.Label(root, text="", pady=20, font=("Helvetica", 16, "bold"), bg="#1E1E1E", fg="white")
    result_label.pack()

    debug_label = tk.Label(root, text="", pady=20, fg="lightgray", bg="#1E1E1E", font=("Helvetica", 10))
    debug_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
