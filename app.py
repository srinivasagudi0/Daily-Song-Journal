import streamlit as st
from support import init_db, add_entry, get_entries, edit_entry
import sqlite3

init_db()

st.title("Daily Song Journal")

st.set_page_config(page_title="Daily Song Journal", page_icon=":musical_note:", layout="wide")

st.sidebar.header("Mode")
mode = st.sidebar.selectbox("Mode", ["Journal a Song", "My Journal"])

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
elif mode == "My Journal":
    st.header("My Journal")
    st.subheader("View your journal entries")
    st.write("Still under development")
    entries = get_entries()
    for entry in entries:
        entry_id, song, artist, opinion, created_at = entry
        st.markdown("---")
        st.markdown(f"**Entry ID: {entry_id}**")
        st.markdown(f"**{song}** by *{artist}*")
        st.markdown(f"> {opinion}")
        st.markdown(f"_Added on {created_at}_")
        st.markdown("---")
    # really hard to edit entries, need to add edit button here in the future
    if st.button("Edit Entry"):
        st.write("Editing entries is still under development.")
    
    if st.button("Delete Entry"):
        st.write("Deleting entries is still under development.")

    # also add delete button here in the future
    # also add delete all button here in the future
