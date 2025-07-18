# Y-Notes

Y-Notes is a simple Streamlit app for organizing notes by subject. Notes are stored locally in a text file (`notes.txt`). You can add, edit, and delete notes for different subjects.

## Features

- Add new subjects
- Create, edit, and delete notes for each subject
- Notes are saved locally and persist between sessions
- Simple, clean interface

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)

## Installation

1. Clone this repository or download the files.
2. Install dependencies:

    ```bash
    pip install streamlit
    ```

## Usage

Run the app with:

```bash
streamlit run app.py
```

## File Structure

- `app.py` — Main Streamlit application
- `notes.txt` — Local storage for notes (created automatically)

## How It Works

- Subjects are managed in the sidebar.
- Notes are created and edited in the main area.
- All notes are saved to `notes.txt` in