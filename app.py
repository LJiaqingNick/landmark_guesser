import streamlit as st
from PIL import Image
import json

# Load landmarks data from JSON
@st.cache_data
def load_landmarks():
    with open("data/landmarks.json", "r") as f:
        return json.load(f)

# Initialize the game session state
def initialize_session():
    st.session_state.current_landmark_index = 0
    st.session_state.hint_index = 0
    st.session_state.landmarks = load_landmarks()
    st.session_state.score = 0
    st.session_state.current_landmark_success = False

# Handle the Submit button
def handle_submit(selected_landmark, score_placeholder):
    if not st.session_state.current_landmark_success:
        if selected_landmark.lower() == st.session_state.landmarks[st.session_state.current_landmark_index]["name"].lower():
            st.success("That's the right answer!")
            st.session_state.score += (3 - st.session_state.hint_index)
            st.session_state.current_landmark_success = True
            score_placeholder.write(f"Score: {st.session_state.score}")
        else:
            st.error("Try again or ask for another hint!")

# Handle the Next Hint button
def handle_next_hint():
    if 'hint_index' in st.session_state:
        st.session_state.hint_index += 1
        if st.session_state.hint_index >= len(st.session_state.landmarks[st.session_state.current_landmark_index]["hints"]):
            st.warning("No more hints for this landmark!")
            st.session_state.hint_index -= 1  # Stay on the last hint

# Handle the Next Landmark button
def handle_next_landmark():
    if 'current_landmark_index' in st.session_state:
        st.session_state.current_landmark_index += 1
        st.session_state.hint_index = 0
        if st.session_state.current_landmark_index >= len(st.session_state.landmarks):
            st.session_state.current_landmark_index = len(st.session_state.landmarks) - 1
            st.balloons()
            st.write("Congratulations! You've completed the game!")
        st.session_state.current_landmark_success = False
        st.rerun()

# Display the game UI
def display_game():
    st.title("Guess the Landmark")
    score_placeholder = st.empty()

    score_placeholder.write(f"Score: {st.session_state.score}")
    
    # Create a dropdown for landmark selection
    selected_landmark = st.selectbox("Select a Landmark:", st.session_state.landmarks[st.session_state.current_landmark_index]["options"])

    if st.button("Submit"):
        handle_submit(selected_landmark, score_placeholder)

    if st.button("Next Hint"):
        handle_next_hint()

    if st.button("Next Landmark"):
        handle_next_landmark()

    # Now display the hint and image
    hint = st.session_state.landmarks[st.session_state.current_landmark_index]['hints'][st.session_state.hint_index]
    st.write(f"Hint: {hint}")
    landmark = st.session_state.landmarks[st.session_state.current_landmark_index]
    image = Image.open(landmark["image"])
    st.image(image, use_column_width=True)

def main():
    if 'current_landmark_index' not in st.session_state:
        initialize_session()

    display_game()

if __name__ == "__main__":
    main()