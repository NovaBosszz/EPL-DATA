import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from adjustText import adjust_text

# Sidebar Setup
st.sidebar.title("Explore Analysis")
st.sidebar.write("Select a project to explore.")

# --- Navigation ---
# Create a dictionary mapping project names to file paths for easier management
pages = {
    "League Passing Profiles": "views/passing_stats.py",
    "League Shooting Profiles": "views/shooting_stats.py",
    "Goals":"views/goals.py",
    "Club Profiles": "views/player_profiles.py"
}

# Sidebar selection for pages
selected_page = st.sidebar.selectbox("Choose a Project", list(pages.keys()))



# --- Run Selected Page ---
# Dynamically load and execute the selected page
if selected_page in pages:
    with open(pages[selected_page]) as f:
        code = f.read()
        exec(code)



# Display footer
st.sidebar.text("Made by November")