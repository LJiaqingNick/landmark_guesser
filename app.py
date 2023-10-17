import streamlit as st
from PIL import Image

landmarks = [
    {"name": "CN Tower", 
     "hints": [
         "It was once the world's tallest freestanding structure.",
         "Located in Canada's largest city.",
         "Features a glass floor and a revolving restaurant."
     ],
     "image": "images/cn_tower.jpg"
    },
    # Add more landmarks as needed
]

def main():
    st.title("Guess the Landmark")

    if 'current_landmark' not in st.session_state:
        st.session_state.current_landmark = 0
    if 'hint_index' not in st.session_state:
        st.session_state.hint_index = 0

    hint = landmarks[st.session_state.current_landmark]['hints'][st.session_state.hint_index]
    st.write(f"Hint: {hint}")

    guess = st.text_input("Your Guess:")

    landmark = landmarks[st.session_state.current_landmark]

    if st.button("Submit"):
        if guess.strip().lower() == landmarks[st.session_state.current_landmark]["name"].lower():
            st.success("That's the right answer!")
            move_to_next_landmark()
        else:
            st.error("Try again or ask for another hint!")

    if st.button("Next Hint"):
        if 'hint_index' in st.session_state:
            st.session_state.hint_index += 1
            if st.session_state.hint_index >= len(landmarks[st.session_state.current_landmark]["hints"]):
                st.warning("No more hints for this landmark!")
                st.session_state.hint_index -= 1  # Stay on the last hint
    # Display the image
    image = Image.open(landmark["image"])
    st.image(image, use_column_width=True)

def move_to_next_landmark():
    if 'current_landmark' in st.session_state:
        st.session_state.current_landmark += 1
        st.session_state.hint_index = 0
        if st.session_state.current_landmark >= len(landmarks):
            st.session_state.current_landmark = 0  # Start over or end the game
            st.balloons()
            st.write("Congratulations! You've completed the game!")

if __name__ == "__main__":
    main()
