import streamlit as st 
import requests 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px
from adjustText import adjust_text




st.title("Football Shooting Stats")

# Define URLs for different leagues
urls = {
   
    "Belgian Pro League": "https://fbref.com/en/comps/37/shooting/Belgian-Pro-League-Stats#all_stats_shooting",
    "Premier League": "https://fbref.com/en/comps/9/shooting/Premier-League-Stats#all_stats_shooting",

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
    }, inplace=True)

# Display Dataframe in an interactive table....Clean dataframe
st.dataframe(df)
st.markdown("---")

def plot_team_shots(df):
    st.header('Shots Vs Shots On Target')

    # Group by 'Squad' and 'Shots' and 'Shots On Target'

    league_shots = df[['Squad','SoT', 'Sh']].sort_values( by='Sh', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y=['Sh', 'SoT',], ax =ax , color=['#1f77b4', '#ff7f0e'])

    ax.set_title('Shots Vs Shots On Target')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    st.pyplot(fig)

def plot_team_acc(df):
    st.header('Shots On Target Vs Goals')

    league_shots = df[['Squad','Gls', 'SoT']].sort_values(by='SoT',ascending=False)

    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_shots.plot(kind="bar", x='Squad', y=['SoT', 'Gls'], ax =ax , color=['#1f77b4', '#ff7f0e'])

    ax.set_title('Shots On Target Vs Goals')
    ax.set_ylabel('Number of Goals')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_shots['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    st.pyplot(fig)

def plot_shots_per_90_vs_sot_per_90(df):
    st.header('Shots/90 vs Shots On Target/90 by Team')
    league_data = df[['Squad', 'Sh/90', 'SoT/90']].sort_values('Sh/90', ascending=False)

    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(111)
    league_data.plot(kind='bar', x='Squad', y=['Sh/90', 'SoT/90'], ax=ax, color=['#1f77b4', '#ff7f0e'])

    ax.set_title('Shots/90 vs Shots On Target/90')
    ax.set_xlabel('Team')
    ax.set_ylabel('Shots per 90')
    ax.set_xticklabels(league_data['Squad'], rotation=45, ha='right')

    st.pyplot(fig)

def plot_team_sot(df):
    st.header('Shots On Target Percentage (SoT%)')

    # Group by 'Squad' and 'passes_Cmp' and 'passes_Att'

    league_goals = df[['Squad','SoT%']].sort_values( by='SoT%', ascending=False)
                                        
    fig = plt.figure(dpi=150)  # Increase DPI for a larger image display
    ax = fig.add_subplot(111)

    #plot the data
    league_goals.plot(kind="bar", x='Squad', y=['SoT%'], ax =ax , color=['#1f77b4'])

    ax.set_title('Direct measure of accuracy')
    ax.set_ylabel('SoT%')
    ax.set_xlabel('Squad')
    ax.set_xticklabels(league_goals['Squad'], rotation=45, ha='right', fontsize=9)

    fig.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points', fontsize=8)

    st.pyplot(fig)



# Calling functions to generate each plot

if df is not None:
 
    plot_team_shots(df)
    st.markdown("---")
    plot_team_acc(df)
    st.markdown("---")
    plot_shots_per_90_vs_sot_per_90(df)
    st.markdown("---")
    plot_team_sot(df)
    st.markdown("---")
   

