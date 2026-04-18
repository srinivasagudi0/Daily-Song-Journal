# Simple little game hub for Streamlit.
# I’ll probably reorganize this later once more games are added.

import streamlit as st
from support import (
    get_fill_blank_round,
    get_song_round,
    is_correct_guess,
    is_correct_word_guess,
)

st.title("Game Library")
st.write("Pick a game from the sidebar to get started.")

# Sidebar selector
st.sidebar.title("What game are you looking for?")
game_choice = st.sidebar.selectbox(
    "Select a game",
    ["Guess the Song", "Lyric Fill-in-the-Blank"]
)

# -----------------------------
# Guess the Song
# -----------------------------
if game_choice == "Guess the Song":
    st.header("Guess the Song")
    st.write("Read the clues and try to guess the song title.")

    # Session state init
    if "song_round" not in st.session_state:
        st.session_state.song_round = get_song_round()
        st.session_state.revealed = False
        st.session_state.correct_this_round = False

    if "score" not in st.session_state:
        st.session_state.score = 0

    def new_round():
        # Reset everything for a fresh song
        st.session_state.song_round = get_song_round()
        st.session_state.revealed = False
        st.session_state.correct_this_round = False
        st.session_state.guess = ""

    # Controls + score
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.button("New Song", on_click=new_round)
    with col_b:
        st.caption(f"Score: {st.session_state.score}")

    # Show the clue
    st.write(st.session_state.song_round["clue"])

    # Input for guess
    st.text_input(
        "Your guess (song title)",
        key="guess",
        placeholder="Type the song title…"
    )

    # Buttons
    check_col, reveal_col = st.columns(2)

    with check_col:
        if st.button("Check Guess"):
            answer_title = st.session_state.song_round["answer_title"]
            if is_correct_guess(st.session_state.guess, answer_title):
                if not st.session_state.correct_this_round:
                    st.session_state.score += 1
                    st.session_state.correct_this_round = True
                st.success("Correct!")
            else:
                st.error("Not quite. Try again or reveal the answer.")

    with reveal_col:
        if st.button("Reveal Answer"):
            st.session_state.revealed = True

    # Reveal section
    if st.session_state.revealed:
        title = st.session_state.song_round["answer_title"]
        artist = st.session_state.song_round["answer_artist"]
        st.info(f"Answer: {title} - {artist}")

# -----------------------------
# Lyric Fill-in-the-Blank
# -----------------------------
if game_choice == "Lyric Fill-in-the-Blank":
    st.header("Song Lyric Fill-in-the-Blank")
    st.write("One word is missing - type it or pick from the choices.")
    st.caption("Demo uses public-domain lines. Add more in support.py → FILL_BLANK_ITEMS.")

    # Init state for this game
    if "fib_round" not in st.session_state:
        st.session_state.fib_round = get_fill_blank_round()
        st.session_state.fib_revealed = False
        st.session_state.fib_correct_this_round = False

    if "fib_score" not in st.session_state:
        st.session_state.fib_score = 0

    if "fib_method" not in st.session_state:
        st.session_state.fib_method = "Type it"

    def new_fib_round():
        st.session_state.fib_round = get_fill_blank_round()
        st.session_state.fib_revealed = False
        st.session_state.fib_correct_this_round = False
        # Clear previous guesses
        st.session_state.pop("fib_guess", None)
        st.session_state.pop("fib_choice", None)

    # Controls + score
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.button("New Lyric", on_click=new_fib_round)
    with col_b:
        st.caption(f"Score: {st.session_state.fib_score}")

    # Show the lyric prompt
    st.subheader("Lyric")
    st.write(st.session_state.fib_round["prompt_line"])

    # Answer method
    st.radio(
        "Answer method",
        ["Type it", "Pick from choices"],
        key="fib_method",
        horizontal=True
    )

    # Input depending on method
    guess_value = ""
    if st.session_state.fib_method == "Pick from choices":
        choices = st.session_state.fib_round.get("choices", [])
        if choices:
            guess_value = st.selectbox(
                "Pick the missing word",
                choices,
                key="fib_choice"
            )
        else:
            st.warning("No choices available for this lyric. Try typing instead.")
    else:
        guess_value = st.text_input(
            "Type the missing word",
            key="fib_guess"
        )

    # Buttons
    check_col, reveal_col = st.columns(2)

    with check_col:
        if st.button("Check"):
            answer_word = st.session_state.fib_round.get("answer_word", "")
            if not answer_word:
                st.error("This lyric didn't generate a blank. Try a new one.")
            elif is_correct_word_guess(guess_value, answer_word):
                if not st.session_state.fib_correct_this_round:
                    st.session_state.fib_score += 1
                    st.session_state.fib_correct_this_round = True
                st.success("Correct!")
            else:
                st.error("Not quite. Try again or reveal the answer.")

    with reveal_col:
        if st.button("Reveal"):
            st.session_state.fib_revealed = True

    # Reveal section
    if st.session_state.fib_revealed:
        ans = st.session_state.fib_round["answer_word"]
        title = st.session_state.fib_round["title"]
        artist = st.session_state.fib_round["artist"]
        full_line = st.session_state.fib_round["full_line"]

        st.info(f"Missing word: {ans}")
        st.write(full_line)
        st.caption(f"{title} - {artist}")
