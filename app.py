import streamlit as st
from support import delete_entry, edit_entry, init_db, add_entry, get_entries
from streamlit_calendar import calendar

# Simple CRUD app.
st.set_page_config(page_title="My Daily Soundtrack", page_icon=":musical_note:", layout="wide")

# set up db so it wont mess up when we run the app for the first time, becasue first impeersion is the best impreression.
init_db()

st.title("My Daily Soundtrack")

st.sidebar.header("Mode")
mode = st.sidebar.selectbox("Mode", ["Home","Journal a Song", "My Journal", "Calendar View"])

# Home, dont know what to add here, maybe some instructions or something, but for now it will just be a welcome message. I will add more later if I get inspiration.
if mode == "Home":
    st.header("Welcome to My Daily Soundtrack")
    st.subheader("A quiet place for the songs that stayed with you.")  

# Journal (Create)
elif mode == "Journal a Song":
    st.header("Journal Entry")
    st.subheader("Add today's soundtrack")
    st.caption("Save the song that matched your day.")
    song_name = st.text_input("What song stayed with you today?")
    artist_name = st.text_input("Who made it?")
    opinion = st.text_area("Why did this song matter today?")
    mood = st.selectbox("What was your mood?", ["Happy", "Heavy", "Hopeful", "Calm", "Lonely", "Nostalgic", "Restless"])
    reminds_me_of = st.text_input("Who does this song remind you of? (optional)")
    note = st.text_area("Something I want to remember (optional)")
    is_favorite = st.checkbox("Star this song")
    if st.button("Add to Journal"):
        if song_name and artist_name and opinion:
            st.success(f"Added '{song_name}' by {artist_name} to your journal!")
            add_entry(song_name, artist_name, opinion, mood, note, reminds_me_of, int(is_favorite))
        else:
            st.error("Please fill in all fields before adding to the journal.")

# View/Edit/Delete (Read/Update/Delete)
elif mode == "My Journal":
    st.header("My Journal")
    st.subheader("Songs I lived with")
    entries = get_entries()
    show_favorites = st.checkbox("Show favorites only")
    if show_favorites:
        entries = [entry for entry in entries if entry[7]]
    if not entries:
        st.info("No journal entries yet.")
    else:
        for entry in entries:
            entry_id, song, artist, opinion, mood, note, reminds_me_of, is_favorite, created_at = entry
            st.caption(created_at)
            star = "★ " if is_favorite else ""
            st.markdown(f"### {star}{song} by {artist}")
            if mood:
                st.markdown(f"**Mood:** {mood}")
            st.markdown("**Why it mattered:**")
            st.markdown(f"> {opinion}")
            if reminds_me_of:
                st.markdown(f"_Reminds me of: {reminds_me_of}_")
            if note:
                st.markdown(f"**Memory:** {note}")
            st.markdown("---")
    
            
    
    st.subheader("Edit an Entry")
    edit_id = st.number_input("Enter the ID of the entry to edit", min_value=1, step=1)
    edit_song = st.text_input("New song")
    edit_artist = st.text_input("New artist")
    edit_opinion = st.text_area("Why did this song matter?")
    edit_mood = st.selectbox("New mood", ["Happy", "Heavy", "Hopeful", "Calm", "Lonely", "Nostalgic", "Restless"])
    edit_reminds_me_of = st.text_input("New person this song reminds you of (optional)")
    edit_note = st.text_area("New memory (optional)")
    edit_is_favorite = st.checkbox("Star this song")

    if st.button("Update Entry"):
        if edit_song and edit_artist and edit_opinion:
            edit_entry(edit_id, edit_song, edit_artist, edit_opinion, edit_mood, edit_note, edit_reminds_me_of, int(edit_is_favorite))
            st.success(f"Updated entry with ID {edit_id}.")
        else:
            st.error("Please fill in all fields before updating.")
    
    delete_id = st.number_input("Enter the ID of the entry to delete", min_value=1, step=1)
    if st.button("Delete Entry"):
        delete_entry(delete_id)
        st.success(f"Deleted entry with ID {delete_id} from your journal.")

    if st.button("Delete All Entries"):
        delete_entry(None)
        st.success("Deleted all journal entries.")

# Calendar View (Read)
elif mode == "Calendar View":
    # add a streak counter, that counts how many days in a row the user has journaled, and display it on the home page, maybe with a little confetti animation when they reach a new streak record. I will need to store the last journal date and the current streak count in the database, and update it whenever a new entry is added.   
    streak = 0
    st.write("Current Streak: " + str(streak))



    st.header("Calendar View")
    # cannot be edited (that is a feature and it would be a nightmare to implement it, so I will just make it non editable)
    calender_options = {
        "editable": "false",
        "selectable": "true",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek,dayGridDay",
        },
        "initialView": "dayGridMonth",
    }
    mood_colors = {
        "Happy": "#facc15",
        "Heavy": "#64748b",
        "Hopeful": "#22c55e",
        "Calm": "#38bdf8",
        "Lonely": "#818cf8",
        "Nostalgic": "#f59e0b",
        "Restless": "#ef4444",
    }
    entries = get_entries()
    calendar_events = []
    for entry in entries:
        entry_id, song, artist, opinion, mood, note, reminds_me_of, is_favorite, created_at = entry
        calendar_events.append({
            "id": entry_id,
            "title": f"{'★ ' if is_favorite else ''}{mood}: {song}" if mood else f"{'★ ' if is_favorite else ''}{song}",
            "start": created_at,
            "description": opinion,
            "color": mood_colors.get(mood, "#a78bfa"),
        })


    state = calendar(
    options=calender_options,
    events=calendar_events,
    key="my_calendar",
    )

    # make it appearr
    st.write(state)
