import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import requests
import plotly.express as px
from adjustText import adjust_text




#----Page Setup---
project_1_page = st.Page(
    page="views/passing_stats.py",
    title="Club Passing Profiles",
    icon=":material/bar_chart:",
    
)
project_2_page = st.Page(
    page="views/shooting_stats.py",
    title ="Club Shooting Profiles",
    icon=":material/bar_chart:",
)

# --- Navigation -----
pg = st.navigation(
    {
        
         "Projects": [project_1_page, project_2_page]
    }
         )

st.sidebar.text("Made by ")


# Run Navigation
pg.run()