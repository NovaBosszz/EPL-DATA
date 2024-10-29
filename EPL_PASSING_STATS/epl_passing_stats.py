import streamlit as st 
import requests 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px

#Page Config
st.set_page_config(layout="wide")


#st.title(" English Premier League Passing Stats")

# Define URLs for different leagues
urls = {
    "Premier League": "https://fbref.com/en/comps/9/passing/Premier-League-Stats#all_stats_passing",
    "La Liga": "https://fbref.com/en/comps/12/passing/La-Liga-Stats#all_stats_passing",
    "Belgian Pro League": "https://fbref.com/en/comps/37/passing/Belgian-Pro-League-Stats#all_stats_passing"
}

# Dropdown menu for selecting league
selected_league = st.selectbox("Select a League", list(urls.keys()))

# Load data from the selected URL
url = urls[selected_league]
st.subheader(f"Loading data from: **{selected_league}**")


#Loading Data from the url
pd.set_option('display.max_columns', None)
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


def plot_team_passes(df):
    st.header('Completed vs Attempted Passes')

    # Group by 'Squad' and 'passes_Cmp' and 'passes_Att'

    team_passes = df[['Squad','passes_Cmp','passes_Att']].sort_values( by='passes_Att', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    team_passes.plot(kind="bar", x='Squad', y=['passes_Cmp', 'passes_Att'], ax =ax , color=['#1f77b4', '#ff7f0e'])

    ax.set_title('Completed vs. Attempted Passes by Team')
    ax.set_ylabel('Number of Passes')
    ax.set_xlabel('Teams')
    ax.set_xticklabels(team_passes['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    st.pyplot(fig)


def plot_passing_types(df):
    st.header('Completed Passes: Short/Medium/Long Pass by Team')
    
    sorted_df = df.sort_values(by='s_passes_Cmp', ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    sorted_df.plot(kind="bar", x='Squad', y=['s_passes_Cmp', 'm_passes_Cmp', 'l_passes_Cmp'], ax =ax , color=['#1f77b4', '#ff7f0e', '#2ca02c'], width=0.8)

    ax.set_title('Short, Medium, Long Passes by Team')
    ax.set_ylabel('Number of Passes')

    ax.set_xticklabels(sorted_df['Squad'], rotation=45, ha='right', fontsize=9)

    st.pyplot(fig)


def plot_progressive_passes(df):
    st.header('Progressive Passes by Team')


    # Sort by total passes attempted
    sorted_df = df.sort_values(by='PrgP', ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    sorted_df.set_index('Squad')[['PrgP']].plot(kind='bar', color=['#ff0000'], ax=ax)

    ax.set_title('Progressive Passes by Team')
    ax.set_ylabel('Progressive Passes')
    ax.set_xticklabels(sorted_df['Squad'], rotation=45, ha='right', fontsize=9)

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 8), 
                    textcoords='offset points',fontsize=8)
        
    st.pyplot(fig)



def plot_missed_passes(df):
    st.header('Missed Passes by Team')

   
    team_passes = df.groupby('Squad').agg({'passes_Cmp': 'sum', 'passes_Att': 'sum'})

    # Calculate passes missed
    team_passes['passes_Missed'] = team_passes['passes_Att'] - team_passes['passes_Cmp']

    # Sort by total passes attempted
    team_passes = team_passes.sort_values(by='passes_Missed', ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)
    team_passes['passes_Missed'].plot(kind='bar', color=['#ff0000'], ax=ax)

    ax.set_title('Missed Passes by Team')
    ax.set_ylabel('Number of Missed Passes')
    ax.set_xticklabels(team_passes.index, rotation=45, ha='right', fontsize=9)

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)
        
    st.pyplot(fig)







# Calling functions to generate each plot
if df is not None:
    plot_team_passes(df)        # Matplotlib bar chart for completed vs attempted
    st.markdown("---")

    plot_passing_types(df)
    st.markdown("---")

    plot_progressive_passes(df)
    st.markdown("---")

    plot_missed_passes(df)     # Mathplotlib bar chart for missed passes
    st.markdown("---")
    


