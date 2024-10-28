import streamlit as st 
st.set_page_config(layout="wide")

import requests 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px



st.title(" English Premier League Passing Stats")

url = "https://fbref.com/en/comps/9/passing/Premier-League-Stats#all_stats_passing"

pd.set_option('display.max_columns', None)

#Loading Data from the url
html = pd.read_html(url, header=1)

df = html[0]

#raw dataframe
#st.dataframe(df)



#Rename Columns for Readability 
df.rename(columns = {
    "# Pl": "no_players",
    "90s": "no_matches",
    "Cmp": "passes_Cmp",
    "Att": "passes_Att",
    "Cmp.1": "s_passes_Cmp",    #Short passes completed
    "Att.1" : "s_passes_Att",   #Short passes attempted
    "Cmp%.1" : "s_passes_Cmp%", #Short passes completion %
    "Cmp.2": "m_passes_Cmp",    #Medium passes completed
    "Att.2" : "m_passes_Att",   #Medium passes attempted
    "Cmp%.2" : "m_passes_Cmp%", # Medium passes completion %
    "Cmp.3" : "l_passes_Cmp",   # Long passes completed
    "Att.3" : "l_passes_Att",   # Long passes attempted
    "Cmp%.3" : "l_passes_Cmp%", # Long passes completion %
    }, inplace=True)

# Display Dataframe in an interactive table....Clean dataframe
st.dataframe(df)

st.markdown("---")


st.header('Completed vs Attempted Passes')

# Group by 'Squad' and calculate the sum for 'passes_Cmp' and 'passes_Att'
team_passes = df[['Squad', 'passes_Cmp', 'passes_Att']].copy()

team_passes = team_passes.sort_values( by='passes_Att', ascending=False)
                                       
fig, ax = plt.subplots(figsize = (10, 6))

team_passes.plot(kind="bar", x='Squad', y=['passes_Cmp', 'passes_Att'], ax =ax , color=['#1f77b4', '#ff7f0e'])

ax.set_title('Completed vs. Attempted Passes by Team')
ax.set_ylabel('Number of Passes')

ax.set_xticklabels(team_passes['Squad'], rotation=45, ha='right')

fig.tight_layout()
st.pyplot(fig)


st.markdown("---")


# bar chart
st.header('Missed Passes by Team')

# Calculate passes missed
team_passes['passes_Missed'] = team_passes['passes_Att'] - team_passes['passes_Cmp']

# Sort by total passes attempted
team_passes = team_passes.sort_values(by='passes_Missed', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
team_passes.set_index('Squad')[['passes_Missed']].plot(kind='bar', color=['#ff0000'], ax=ax)

ax.set_title('Missed Passes by Team')
ax.set_ylabel('Number of Missed Passes')
ax.set_xticklabels(team_passes['Squad'], rotation=45, ha='right')

for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 8), 
                textcoords='offset points')
    
st.pyplot(fig)


st.markdown("---")


st.header('Completed Passes: Short/Medium/Long Pass by Team')

sorted_df = df.sort_values(by='s_passes_Cmp', ascending=False)

fig, ax = plt.subplots(figsize = (10,6))

sorted_df.plot(kind="bar", x='Squad', y=['s_passes_Cmp', 'm_passes_Cmp', 'l_passes_Cmp'], ax =ax , color=['#1f77b4', '#ff7f0e', '#2ca02c'], width=0.8)

ax.set_title('Short, Medium, Long Passes by Team')
ax.set_ylabel('Number of Passes')

ax.set_xticklabels(sorted_df['Squad'], rotation=45, ha='right')

st.pyplot(fig)


st.markdown("---")


st.header('Progressive Passes by Team')

