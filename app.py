import streamlit as st
from PIL import Image
import json

@st.cache_data
def load_landmarks():
    with open("data/landmarks.json", "r") as f:
        return json.load(f)

def main():
    st.title("Guess the Landmark")

    if 'current_landmark_index' not in st.session_state:
        st.session_state.current_landmark_index = 0
    if 'hint_index' not in st.session_state:
        st.session_state.hint_index = 0
    if "landmarks" not in st.session_state:
        st.session_state.landmarks = load_landmarks()


    guess = st.text_input("Your Guess:")

    if st.button("Submit"):
        if guess.strip().lower() == st.session_state.landmarks[st.session_state.current_landmark_index]["name"].lower():
            st.success("That's the right answer!")
        else:
            st.error("Try again or ask for another hint!")

    if st.button("Next Hint"):
        if 'hint_index' in st.session_state:
            st.session_state.hint_index += 1
            if st.session_state.hint_index >= len(st.session_state.landmarks[st.session_state.current_landmark_index]["hints"]):
                st.warning("No more hints for this landmark!")
                st.session_state.hint_index -= 1  # Stay on the last hint

    if st.button("Next Landmark"):
        move_to_next_landmark()
    # Now display the hint and image
    hint = st.session_state.landmarks[st.session_state.current_landmark_index]['hints'][st.session_state.hint_index]
    st.write(f"Hint: {hint}")
    landmark = st.session_state.landmarks[st.session_state.current_landmark_index]
    image = Image.open(landmark["image"])
    st.image(image, use_column_width=True)

def move_to_next_landmark():
    if 'current_landmark_index' in st.session_state:
        st.session_state.current_landmark_index += 1
        st.session_state.hint_index = 0
        if st.session_state.current_landmark_index >= len(st.session_state.landmarks):
            # st.session_state.current_landmark_index = 0  # Start over or end the game
            st.session_state.current_landmark_index = len(st.session_state.landmarks) - 1  # Stay on the last landmark
            st.balloons()
            st.write("Congratulations! You've completed the game!")

if __name__ == "__main__":
    main()
