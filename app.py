import streamlit as st
from support import init_db, add_entry
import sqlite3

init_db()

st.title("Daily Song Journal")

st.set_page_config(page_title="Daily Song Journal", page_icon=":musical_note:", layout="wide")

st.sidebar.header("Mode")
mode = st.sidebar.selectbox("Mode", ["Journal a Song"])

if mode == "Journal a Song":
    st.header("Journal Entry")
    st.subheader("Add a new song to your journal")
    song_name = st.text_input("Song Name")
    artist_name = st.text_input("Artist Name")
    opinion = st.text_area("Your Opinion")
    if st.button("Add to Journal"):
        if song_name and artist_name and opinion:
            st.success(f"Added '{song_name}' by {artist_name} to your journal!")
            add_entry(song_name, artist_name, opinion)
        else:
            st.error("Please fill in all fields before adding to the journal.")
        
