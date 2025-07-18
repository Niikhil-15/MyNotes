import streamlit as st
import json
import os
from datetime import datetime

# --- FILE STORAGE ---
# The notes will be stored in a local text file named 'notes.txt'.
NOTES_FILE = 'notes.txt'

def load_notes():
    """Loads notes from the local text file."""
    if not os.path.exists(NOTES_FILE):
        return {'subjects': ['English', 'History'], 'notes': []}
    try:
        with open(NOTES_FILE, 'r') as f:
            content = f.read()
            if not content: # Handle empty file
                return {'subjects': ['English', 'History'], 'notes': []}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is corrupted or not found, start fresh
        return {'subjects': ['English', 'History'], 'notes': []}


def save_notes(data):
    """Saves the notes data to the local text file."""
    with open(NOTES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- INITIALIZE APP STATE ---
# Use session_state to hold data while the app is running.
if 'data' not in st.session_state:
    st.session_state.data = load_notes()

if 'editing_note_index' not in st.session_state:
    st.session_state.editing_note_index = None

# --- APP LAYOUT ---
st.set_page_config(layout="wide", page_title="Y-Notes")

st.title("✒️ Y-Notes")
st.write("A simple app to jot down your notes by subject.")

# --- SIDEBAR FOR SUBJECT SELECTION ---
st.sidebar.header("Subjects")

# Let user add a new subject
new_subject = st.sidebar.text_input("Add a new subject")
if st.sidebar.button("Add Subject") and new_subject and new_subject not in st.session_state.data['subjects']:
    st.session_state.data['subjects'].append(new_subject)
    save_notes(st.session_state.data)
    st.sidebar.success(f"Added subject: {new_subject}")

# Dropdown to select a subject
selected_subject = st.sidebar.selectbox(
    "Select a subject to view or add notes",
    options=st.session_state.data['subjects']
)

# --- MAIN AREA ---
col1, col2 = st.columns([0.7, 0.3])

# --- COLUMN 1: Note Creation/Editing Form ---
with col1:
    # Determine if we are editing or adding a new note
    is_editing = st.session_state.editing_note_index is not None
    form_title = "Edit Note" if is_editing else f"Add a New Note to {selected_subject}"
    st.subheader(form_title)

    # Pre-fill form if editing
    default_title = ""
    default_content = ""
    if is_editing:
        note_to_edit = st.session_state.data['notes'][st.session_state.editing_note_index]
        default_title = note_to_edit['title']
        default_content = note_to_edit['content']

    with st.form(key="note_form", clear_on_submit=True):
        title = st.text_input("Title", value=default_title)
        notes_content = st.text_area("Notes", height=200, value=default_content)
        
        # Create two columns for the Save and Cancel buttons
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            submitted = st.form_submit_button("💾 Save")
        
        with form_col2:
            if is_editing:
                cancelled = st.form_submit_button("❌ Cancel Edit")
                if cancelled:
                    st.session_state.editing_note_index = None
                    st.rerun()


        if submitted and title and notes_content:
            if is_editing:
                # Update existing note
                note_index = st.session_state.editing_note_index
                st.session_state.data['notes'][note_index]['title'] = title
                st.session_state.data['notes'][note_index]['content'] = notes_content
                st.session_state.data['notes'][note_index]['last_edited'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.editing_note_index = None # Exit editing mode
                st.success("Note updated successfully!")
            else:
                # Add a new note
                new_note = {
                    'subject': selected_subject,
                    'title': title,
                    'content': notes_content,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.data['notes'].append(new_note)
                st.success("Note saved successfully!")
            
            save_notes(st.session_state.data)
            st.rerun() # Rerun to update the display

# --- COLUMN 2: Displaying Notes ---
with col2:
    st.subheader(f"Notes in {selected_subject}")

    # Filter notes for the selected subject
    notes_in_subject = [
        (note, i) for i, note in enumerate(st.session_state.data['notes']) 
        if note['subject'] == selected_subject
    ]
    
    # Sort notes by date, newest first
    notes_in_subject.sort(key=lambda x: x[0]['date'], reverse=True)


    if not notes_in_subject:
        st.info("No notes found for this subject. Add one using the form on the left.")
    else:
        for note, index in notes_in_subject:
            with st.expander(f"**{note['title']}** - *{note['date']}*"):
                st.write(note['content'])
                
                # Buttons for Edit and Delete
                btn_col1, btn_col2 = st.columns([0.15, 0.15])
                
                if btn_col1.button("✏️ Edit", key=f"edit_{index}"):
                    st.session_state.editing_note_index = index
                    st.rerun()

                if btn_col2.button("🗑️ Delete", key=f"delete_{index}"):
                    # Remove the note by index
                    del st.session_state.data['notes'][index]
                    st.session_state.editing_note_index = None  # Reset editing index
                    save_notes(st.session_state.data)
                    st.rerun()

# --- Style Enhancements ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .stExpander {
        border: 1px solid #e6e6e6;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)
