# Sound Classifier

## Overview

The Sound Classifier application is a tool for analyzing audio files to determine if they have a melodic quality. Using the `tkinter` library for the GUI and `librosa` for audio processing, this script provides a user-friendly interface for drag-and-drop audio analysis. Users can adjust various parameters through sliders to influence the analysis results.

![Application Screenshot](assets/screenshot.png)

## Features

- **Drag & Drop**: Easily load audio files by dragging them into the application window.
- **Audio Playback**: Optionally play the audio file after analysis.
- **Adjustable Parameters**: Configure analysis sensitivity and thresholds using sliders.
- **Results Display**: See if the audio is classified as melodic or non-melodic with visual feedback.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/sound-classifier.git
    cd sound-classifier
    ```

2. **Install dependencies:**
    Ensure you have `Python 3.x` installed. Then, install the required packages using pip:
    ```bash
    pip install tkinterdnd2 librosa numpy pillow
    ```
    Note: `tkinter` is usually included with Python installations. If not, you may need to install it separately.

3. **Add Assets:**
    Place your `drag_drop_icon.png` file in an `icons` directory inside the project folder. This image is used in the drag-and-drop area of the GUI.

## Usage

1. **Run the Script:**
    Execute the script using Python:
    ```bash
    python sound_classifier.py
    ```

2. **Drag & Drop an Audio File:**
    Drag an audio file into the designated area in the application window.

3. **Configure Parameters:**
    - **Max Note Shifts**: Set the maximum number of note shifts considered for a melodic classification.
    - **Pitch Threshold (Hz)**: Adjust the minimum pitch magnitude required for a note to be considered.
    - **Min Note Duration (s)**: Set the minimum duration a note must be sustained to be counted.
    - **Harmony Threshold**: Define the ratio of harmonic changes to note changes required for a melodic classification.

4. **View Results:**
    The result will be displayed as "Melodic Sound ✅" or "Non-melodic Sound ❌", with additional debug information shown below.

## Parameters Explained

- **Max Note Shifts**: The number of times the pitch of the sound must change to be considered melodic.
- **Pitch Threshold (Hz)**: The minimum amplitude of the pitch required to be considered a valid note.
- **Min Note Duration (s)**: The shortest duration a note must be present to be included in the analysis.
- **Harmony Threshold**: The minimum ratio of harmonic changes to total note changes for the sound to be classified as melodic.

## Troubleshooting

- **No Sound Playback**: Ensure your system's default audio player is properly configured. Check the console for error messages.
- **Performance Issues**: Large audio files may take longer to process. Ensure your system meets the recommended specifications.

