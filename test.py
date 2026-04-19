import streamlit as st
from streamlit_calendar import calendar

# Define calendar options
calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,dayGridWeek,dayGridDay",
    },
    "initialView": "dayGridMonth",
}

# Define events
calendar_events = [
    {
        "title": "Meeting with Team",
        "start": "2026-04-20T10:00:00",
        "end": "2026-04-20T12:00:00",
    },
    {
        "title": "Project Launch",
        "start": "2026-04-25",
        "allDay": "true",
    }
]

# Render the calendar
state = calendar(
    events=calendar_events,
    options=calendar_options,
    key="my_calendar",
)

# Access calendar state (e.g., when an event is clicked)
st.write(state)